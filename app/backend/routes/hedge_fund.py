from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
import logging

from app.backend.models.schemas import ErrorResponse, HedgeFundRequest
from app.backend.models.events import StartEvent, ProgressUpdateEvent, ErrorEvent, CompleteEvent
from app.backend.services.graph import create_graph, parse_hedge_fund_response, run_graph_async
from app.backend.services.portfolio import create_portfolio
from app.backend.security import verify_token, RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD
from src.utils.progress import progress
from src.utils.analysts import get_agents_list
from src.llm.models import get_models_list

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/hedge-fund")

@router.post(
    path="/run",
    responses={
        200: {"description": "Successful response with streaming updates"},
        400: {"model": ErrorResponse, "description": "Invalid request parameters"},
        401: {"model": ErrorResponse, "description": "Authentication required"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
@limiter.limit(f"{RATE_LIMIT_CALLS}/{RATE_LIMIT_PERIOD}s")
async def run_hedge_fund(
    req: Request,
    request: HedgeFundRequest, 
    auth_data: dict = Depends(verify_token)
):
    try:
        # Create the portfolio
        portfolio = create_portfolio(request.initial_cash, request.margin_requirement, request.tickers)

        # Construct agent graph
        graph = create_graph(request.selected_agents)
        graph = graph.compile()

        # Log a test progress update for debugging
        progress.update_status("system", None, "Preparing hedge fund run")

        # Convert model_provider to string if it's an enum
        model_provider = request.model_provider
        if hasattr(model_provider, "value"):
            model_provider = model_provider.value

        # Set up streaming response
        async def event_generator():
            # Queue for progress updates
            progress_queue = asyncio.Queue()

            # Simple handler to add updates to the queue
            def progress_handler(agent_name, ticker, status, analysis, timestamp):
                event = ProgressUpdateEvent(agent=agent_name, ticker=ticker, status=status, timestamp=timestamp, analysis=analysis)
                progress_queue.put_nowait(event)

            # Register our handler with the progress tracker
            progress.register_handler(progress_handler)

            try:
                # Start the graph execution in a background task
                run_task = asyncio.create_task(
                    run_graph_async(
                        graph=graph,
                        portfolio=portfolio,
                        tickers=request.tickers,
                        start_date=request.start_date,
                        end_date=request.end_date,
                        model_name=request.model_name,
                        model_provider=model_provider,
                        request=request,  # Pass the full request for agent-specific model access
                    )
                )
                # Send initial message
                yield StartEvent().to_sse()

                # Stream progress updates until run_task completes
                while not run_task.done():
                    # Either get a progress update or wait a bit
                    try:
                        event = await asyncio.wait_for(progress_queue.get(), timeout=1.0)
                        yield event.to_sse()
                    except asyncio.TimeoutError:
                        # Just continue the loop
                        pass

                # Get the final result
                result = run_task.result()

                if not result or not result.get("messages"):
                    yield ErrorEvent(message="Failed to generate hedge fund decisions").to_sse()
                    return

                # Send the final result
                final_data = CompleteEvent(
                    data={
                        "decisions": parse_hedge_fund_response(result.get("messages", [])[-1].content),
                        "analyst_signals": result.get("data", {}).get("analyst_signals", {}),
                    }
                )
                yield final_data.to_sse()

            finally:
                # Clean up
                progress.unregister_handler(progress_handler)
                if "run_task" in locals() and not run_task.done():
                    run_task.cancel()

        # Return a streaming response
        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except HTTPException as e:
        logger.error(f"HTTP error in run_hedge_fund: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in run_hedge_fund: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")

@router.get(
    path="/agents",
    responses={
        200: {"description": "List of available agents"},
        401: {"model": ErrorResponse, "description": "Authentication required"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
@limiter.limit(f"{RATE_LIMIT_CALLS * 2}/{RATE_LIMIT_PERIOD}s")  # More lenient for GET requests
async def get_agents(req: Request, auth_data: dict = Depends(verify_token)):
    """Get the list of available agents."""
    try:
        logger.info(f"User {auth_data['username']} requested agents list")
        return {"agents": get_agents_list()}
    except Exception as e:
        logger.error(f"Error retrieving agents: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve agents")


@router.get(
    path="/language-models",
    responses={
        200: {"description": "List of available LLMs"},
        401: {"model": ErrorResponse, "description": "Authentication required"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
@limiter.limit(f"{RATE_LIMIT_CALLS * 2}/{RATE_LIMIT_PERIOD}s")  # More lenient for GET requests
async def get_language_models(req: Request, auth_data: dict = Depends(verify_token)):
    """Get the list of available models."""
    try:
        logger.info(f"User {auth_data['username']} requested models list")
        return {"models": get_models_list()}
    except Exception as e:
        logger.error(f"Error retrieving models: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve models")


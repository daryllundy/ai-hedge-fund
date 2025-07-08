from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio
import json
from datetime import timedelta

from app.backend.security import create_demo_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, API_KEY

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to AI Hedge Fund API", "version": "1.0.0", "status": "operational"}


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "ai-hedge-fund-api",
        "version": "1.0.0"
    }


@router.post("/auth/token")
@limiter.limit("5/minute")
async def get_access_token(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Get access token for API authentication.
    For demo purposes, accepts 'demo'/'demo123' credentials.
    """
    # Simple demo authentication - in production, verify against a database
    if username == "demo" and password == "demo123":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/auth/demo-token")
@limiter.limit("3/minute")
async def get_demo_token(request: Request):
    """Get a demo token for testing purposes."""
    return {
        "access_token": create_demo_token(),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "api_key": API_KEY,
        "note": "This is a demo token for testing. In production, use proper authentication."
    }


@router.get("/ping")
@limiter.limit("10/minute")
async def ping(request: Request):
    async def event_generator():
        for i in range(5):
            # Create a JSON object for each ping
            data = {"ping": f"ping {i+1}/5", "timestamp": i + 1}

            # Format as SSE
            yield f"data: {json.dumps(data)}\n\n"

            # Wait 1 second
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

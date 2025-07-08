# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Python/Backend Development
```bash
# Install dependencies
poetry install

# Run the hedge fund CLI
poetry run python src/main.py --ticker AAPL,MSFT,NVDA

# Run the backtester
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA

# Run backend API server
poetry run fastapi dev app/backend/main.py

# Run linting and formatting
poetry run black src/ app/
poetry run isort src/ app/
poetry run flake8 src/ app/

# Run tests
poetry run pytest
```

### Frontend Development
```bash
# Navigate to frontend
cd app/frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

### Docker Development
```bash
# From docker/ directory
cd docker

# Build the image
./run.sh build  # Linux/Mac
run.bat build   # Windows

# Run hedge fund
./run.sh --ticker AAPL,MSFT,NVDA main

# Run backtester
./run.sh --ticker AAPL,MSFT,NVDA backtest
```

## System Architecture

This is an AI-powered hedge fund application that uses multiple AI analyst personas to make trading decisions.

### Core Components

**Multi-Agent System:**
- 15+ distinct AI analyst agents representing famous investors (Warren Buffett, Michael Burry, etc.)
- Each agent in `src/agents/` has unique investment philosophy and analysis approach
- Agents work together through LangGraph workflow orchestration

**Application Structure:**
- **CLI Interface**: `src/main.py` - Main entry point with interactive analyst selection
- **Backend API**: `app/backend/` - FastAPI server with SSE streaming for real-time updates
- **Frontend**: `app/frontend/` - React/TypeScript visual workflow editor using ReactFlow
- **Backtesting**: `src/backtester.py` - Historical performance analysis

**Workflow Orchestration (LangGraph):**
- **State Management**: `src/graph/state.py` defines `AgentState` with messages, data, and metadata
- **Execution Flow**: Start → Analyst agents (parallel) → Risk manager → Portfolio manager
- **Data Flow**: Input tickers → Analysis → Risk assessment → Trading decisions

### Key Services

**Graph Service**: Creates and executes LangGraph workflows
**Portfolio Service**: Manages portfolio state and calculations  
**Risk Manager**: Controls position sizing and risk parameters
**Portfolio Manager**: Makes final trading decisions

### LLM Integration

**Multi-Provider Support:**
- OpenAI (GPT-4 variants)
- Anthropic (Claude models)
- Ollama (local inference)
- Groq, DeepSeek

**Model Configuration:**
- Interactive CLI model selection
- API endpoints for model discovery
- Per-agent model configuration support

### API Structure

**Main Endpoints:**
- `POST /hedge-fund/run` - Execute analysis with streaming updates
- `GET /hedge-fund/agents` - List available analysts
- `GET /hedge-fund/language-models` - List supported models
- `GET /health` - Health check

**Features:**
- Server-Sent Events for real-time progress
- Async processing with progress tracking
- CORS support for frontend integration

### Frontend Architecture

**React + TypeScript with:**
- ReactFlow visual workflow editor
- Real-time toast notifications
- Flow persistence (save/load configurations)
- Keyboard shortcuts and dark mode
- Responsive layout system

## Environment Setup

Required environment variables:
- `OPENAI_API_KEY` - For OpenAI models
- `GROQ_API_KEY` - For Groq models  
- `ANTHROPIC_API_KEY` - For Claude models
- `DEEPSEEK_API_KEY` - For DeepSeek models
- `FINANCIAL_DATASETS_API_KEY` - For market data (optional for AAPL,GOOGL,MSFT,NVDA,TSLA)

## Project Structure

- `src/` - Core Python application
  - `agents/` - Individual AI analyst implementations
  - `graph/` - LangGraph state and workflow management
  - `tools/` - Market data and analysis utilities
  - `main.py` - CLI entry point
  - `backtester.py` - Backtesting functionality
- `app/` - Web application
  - `backend/` - FastAPI server
  - `frontend/` - React/TypeScript UI
- `docker/` - Docker configuration and scripts
- `tests/` - Test files

## Development Notes

- Use Poetry for Python dependency management
- Black line length set to 420 characters
- Pre-commit hooks enabled for security checks
- Frontend uses Vite + React with shadcn/ui components
- System supports both CLI and web interfaces
- All Docker commands must be run from `docker/` directory
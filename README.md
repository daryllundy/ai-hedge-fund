# 🚀 AI Hedge Fund: Revolutionizing Investment with Artificial Intelligence! 🌟

Welcome to the future of investing! This **AI-powered Hedge Fund** is a groundbreaking proof of concept that harnesses the power of artificial intelligence to make smarter, data-driven trading decisions. Imagine having the world's greatest investment minds at your fingertips—now, through AI, you can! This project is for **educational purposes only** and not intended for real trading or investment, but it offers a thrilling glimpse into what’s possible. Ready to explore the cutting edge of finance? Let’s dive in! 💰

## Why This Matters
In a world where markets move faster than ever, AI offers unparalleled insights by simulating the strategies of legendary investors. Our system brings together **17 unique AI agents**, each modeled after iconic financial gurus and specialized analysis techniques, to create a dynamic, collaborative decision-making engine. From Warren Buffett’s value-driven approach to Cathie Wood’s innovation focus, we’ve got it all covered.

Check out this stunning visualization of our AI Hedge Fund in action:
<img width="1042" alt="Screenshot 2025-03-22 at 6 19 07 PM" src="https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4" />

**Note**: This system simulates trading decisions—it does not execute real trades. But the insights are as real as it gets!

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Meet Our AI Investment Titans 🧠
Our AI agents work together to analyze, strategize, and simulate investment decisions:
1. **Aswath Damodaran Agent** - The Dean of Valuation, weaving stories with disciplined numbers.
2. **Ben Graham Agent** - The godfather of value investing, hunting hidden gems with a margin of safety.
3. **Bill Ackman Agent** - An activist investor, taking bold positions to drive change.
4. **Cathie Wood Agent** - The queen of growth, betting big on innovation and disruption.
5. **Charlie Munger Agent** - Buffett’s partner, seeking wonderful businesses at fair prices.
6. **Michael Burry Agent** - The Big Short contrarian, uncovering deep value.
7. **Peter Lynch Agent** - A practical investor chasing "ten-baggers" in everyday businesses.
8. **Phil Fisher Agent** - A meticulous growth investor with deep "scuttlebutt" research.
9. **Rakesh Jhunjhunwala Agent** - The Big Bull of India, mastering emerging markets.
10. **Stanley Druckenmiller Agent** - A macro legend finding asymmetric growth opportunities.
11. **Warren Buffett Agent** - The Oracle of Omaha, buying wonderful companies at fair prices.
12. **Valuation Agent** - Calculates intrinsic stock value and generates trading signals.
13. **Sentiment Agent** - Gauges market mood to inform decisions.
14. **Fundamentals Agent** - Dives deep into financial data for actionable insights.
15. **Technicals Agent** - Analyzes charts and indicators for precise timing.
16. **Risk Manager** - Keeps risk in check with calculated position limits.
17. **Portfolio Manager** - The final decision-maker, turning analysis into action.

## Disclaimer ⚠️
This project is for **educational and research purposes only**:
- Not intended for real trading or investment.
- No investment advice or guarantees provided.
- Creator assumes no liability for financial losses.
- Consult a financial advisor for investment decisions.
- Past performance does not indicate future results.

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [Setup](#setup)
  - [Using Poetry](#using-poetry)
  - [Using Docker](#using-docker)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
- [Contributing](#contributing)
- [Feature Requests](#feature-requests)
- [License](#license)

## Setup 🛠️

### Using Poetry
Clone the repository:
```bash
git clone https://github.com/daryllundy/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Install pre-commit hooks for security checks:
```bash
pipx install pre-commit
pre-commit install
```

4. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env
```

5. Set your API keys:
```bash
# For running LLMs hosted by OpenAI (gpt-4o, gpt-4o-mini, etc.)
# Get your OpenAI API key from https://platform.openai.com/
OPENAI_API_KEY=your-openai-api-key

# For running LLMs hosted by Groq (deepseek, llama3, etc.)
# Get your Groq API key from https://groq.com/
GROQ_API_KEY=your-groq-api-key

# For getting financial data to power the hedge fund
# Get your Financial Datasets API key from https://financialdatasets.ai/
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

### Using Docker
1. Make sure you have Docker installed on your system. If not, download it from [Docker's official website](https://www.docker.com/get-started).

2. Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Edit the .env file to add your API keys as described above.

5. Navigate to the docker directory:
```bash
cd docker
```

6. Build the Docker image:
```bash
# On Linux/Mac:
./run.sh build

# On Windows:
run.bat build
```

**Important**: You must set `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY` for the hedge fund to work. If you want to use LLMs from all providers, set all API keys.

Financial data for AAPL, GOOGL, MSFT, NVDA, and TSLA is free and does not require an API key. For any other ticker, set the `FINANCIAL_DATASETS_API_KEY` in the .env file.

## Usage 🚀

### Running the Hedge Fund

#### With Poetry
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

#### With Docker
**Note**: All Docker commands must be run from the `docker/` directory.
```bash
# Navigate to the docker directory first
cd docker

# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA main

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA main
```

**Example Output:**
<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

You can also specify a `--ollama` flag to run the AI hedge fund using local LLMs:
```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --ollama

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA --ollama main

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA --ollama main
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent:
```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA --show-reasoning main

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA --show-reasoning main
```

Optionally specify start and end dates for specific time periods:
```bash
# With Poetry:
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 main
```

### Running the Backtester

#### With Poetry
```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

#### With Docker
**Note**: All Docker commands must be run from the `docker/` directory.
```bash
# Navigate to the docker directory first
cd docker

# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA backtest

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA backtest
```

**Example Output:**
<img width="941" alt="Screenshot 2025-01-06 at 5 47 52 PM" src="https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47" />

Optionally specify start and end dates to backtest over a specific period:
```bash
# With Poetry:
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 backtest
```

You can also specify a `--ollama` flag to run the backtester using local LLMs:
```bash
# With Poetry:
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --ollama

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --ticker AAPL,MSFT,NVDA --ollama backtest

# On Windows:
run.bat --ticker AAPL,MSFT,NVDA --ollama backtest
```

## Contributing 🤝
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.

**Important**: Keep pull requests small and focused for easier review and merge.

## Feature Requests 💡
Have an idea to make this AI Hedge Fund even better? Open an [issue](https://github.com/daryllundy/ai-hedge-fund/issues) tagged with `enhancement`.

## License 📜
This project is licensed under the MIT License—see the LICENSE file for details.

---

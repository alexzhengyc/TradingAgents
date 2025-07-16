<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: Multi-Agent LLM Financial Trading Framework

![TradingAgents](assets/TauricResearch.png)

**TradingAgents** is a sophisticated multi-agent framework for financial trading analysis using Large Language Models (LLMs). The system employs multiple specialized agents working in concert to provide comprehensive market analysis and trading recommendations.

## Features

- **Multi-Agent Architecture**: Specialized agents for different aspects of market analysis
- **LLM Integration**: Support for OpenAI GPT models with configurable shallow and deep thinking agents
- **Comprehensive Analysis**: Market, sentiment, news, and fundamental analysis
- **Research Workflow**: Bull/Bear researcher debate with manager oversight
- **Risk Management**: Multi-perspective risk analysis with portfolio management decisions
- **Real-time Data**: Integration with multiple data sources including Yahoo Finance, Reddit, and news APIs
- **🆕 Parallel Processing**: Run analysis on multiple tickers simultaneously with configurable concurrency
- **Rich CLI Interface**: Beautiful command-line interface with progress tracking

## Architecture

![Architecture](assets/schema.png)

The system consists of several agent teams:

### Analyst Team
- **Market Analyst**: Technical analysis and market trends
- **Social Media Analyst**: Sentiment analysis from social platforms
- **News Analyst**: News impact and sentiment analysis  
- **Fundamentals Analyst**: Financial metrics and company fundamentals

### Research Team
- **Bull Researcher**: Optimistic investment perspective
- **Bear Researcher**: Pessimistic investment perspective
- **Research Manager**: Synthesizes bull/bear arguments

### Trading Team
- **Trader**: Develops specific trading strategies

### Risk Management Team
- **Risk Analysts**: Multiple risk perspectives (Aggressive, Conservative, Neutral)
- **Portfolio Manager**: Final investment decision

## Quick Start

### Single Ticker Analysis

Run analysis on a single ticker (backwards compatible):

```bash
# Run with default settings (SPY)
python cli/main.py

# Or analyze a specific ticker
python cli/parallel.py single --ticker AAPL
```

### 🆕 Parallel Multi-Ticker Analysis

Analyze multiple tickers simultaneously for faster results:

```bash
# Quick start: Analyze 3 tickers with 2 parallel workers
python cli/parallel.py quick --count 3 --parallel 2

# Analyze specific tickers in parallel
python cli/parallel.py run --tickers "AAPL,MSFT,GOOG,TSLA" --max-parallel 3

# Analyze first 5 default tickers with 3 parallel workers
python cli/parallel.py run --max-tickers 5 --max-parallel 3

# List all available default tickers
python cli/parallel.py list
```

### Parallel CLI Options

- `--tickers, -t`: Comma-separated list of custom tickers
- `--max-tickers, -n`: Maximum number of tickers to analyze from default list
- `--max-parallel, -p`: Number of parallel analyses to run simultaneously
- `--count, -c`: Quick start option for number of tickers
- `--parallel, -p`: Quick start option for parallel workers

### Example Commands

```bash
# Analyze top 10 tickers with 4 parallel workers
python cli/parallel.py run -n 10 -p 4

# Custom ticker analysis
python cli/parallel.py run -t "NVDA,AMD,INTC" -p 2

# Single ticker with full analysis
python cli/parallel.py single -t TSLA

# Quick analysis of 5 tickers
python cli/parallel.py quick -c 5 -p 3
```

## Performance Benefits

- **Parallel Processing**: Analyze multiple tickers simultaneously
- **Configurable Concurrency**: Control resource usage with parallel worker limits
- **Progress Tracking**: Real-time progress monitoring for each ticker
- **Error Handling**: Robust error handling with detailed reporting
- **Resource Optimization**: Thread-based parallelism for I/O-bound operations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- OpenAI API key
- Reddit API credentials (optional)
- News API key (optional)

## Configuration

The system uses a hierarchical configuration system:

- **Default Config**: `tradingagents/default_config.py`
- **Environment Variables**: Override via `.env` file
- **Runtime Parameters**: CLI arguments override config

Key configuration options:
- `max_debate_rounds`: Research team debate iterations
- `max_risk_discuss_rounds`: Risk management discussion rounds
- `quick_think_llm`: Fast reasoning model (e.g., gpt-4o)
- `deep_think_llm`: Deep analysis model (e.g., o3)
- `llm_provider`: LLM service provider
- `backend_url`: API endpoint URL

## Default Tickers

The system includes a curated list of default tickers covering major sectors:

```python
DEFAULT_TICKERS = [
    "UNH", "MSFT", "ADM", "AES", "AZO", "AXON", "WFC", "ABT", 
    "AAPL", "AMZN", "GOOG", "META", "NFLX", "TSLA", "NVDA",
    "ARE", "ALL", "ACN", "ALB", "ADBE", "AMGN", "MMM", 
    "APTV", "BKR", "APD", "AKAM"
]
```

## Output Structure

Analysis results are saved to `results/{TICKER}/{DATE}/`:
- `reports/`: Individual analysis reports in Markdown
- `message_tool.log`: Complete analysis log

Report sections:
- `market_report.md`: Technical analysis
- `sentiment_report.md`: Social sentiment analysis
- `news_report.md`: News analysis
- `fundamentals_report.md`: Financial fundamentals
- `investment_plan.md`: Research team decision
- `trader_investment_plan.md`: Trading strategy
- `final_trade_decision.md`: Final portfolio decision

## Advanced Usage

### Custom Agent Configuration

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Custom analyst selection
analysts = ["market", "news", "fundamentals"]

# Custom configuration
config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 3
config["deep_think_llm"] = "o3"

graph = TradingAgentsGraph(analysts, config=config)
```

### Batch Processing

```python
from cli.main import run_quick_analysis

# Analyze multiple ticker sets
results, errors = run_quick_analysis(
    tickers=["AAPL", "MSFT", "GOOG"],
    max_parallel=2,
    max_tickers=None
)
```

## Development

See [docs/development.md](docs/development.md) for development guidelines.

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Agent Details](docs/agents.md)
- [Data Sources](docs/data-sources.md)
- [Configuration Guide](docs/configuration.md)
- [API Reference](docs/api-reference.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Tauric Research** - Framework development and research
- **OpenAI** - LLM integration and reasoning capabilities
- **Rich** - Beautiful terminal interfaces
- **LangGraph** - Agent workflow orchestration

---

**Note**: This is a research framework for educational and analysis purposes. Not financial advice. Always consult with qualified financial professionals before making investment decisions.

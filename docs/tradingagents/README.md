# TradingAgents Documentation

Welcome to the TradingAgents documentation! This multi-agent LLM financial trading framework simulates the dynamics of real-world trading firms using specialized AI agents.

## 📚 Documentation Overview

This documentation is organized into several sections to help you understand and work with TradingAgents:

| Document | Description |
|----------|-------------|
| [Architecture Guide](./architecture.md) | Complete system architecture and workflow |
| [Agents Reference](./agents.md) | Detailed description of all trading agents |
| [Data Sources](./data-sources.md) | Data pipeline and external data sources |
| [Configuration](./configuration.md) | Configuration options and customization |
| [API Reference](./api-reference.md) | Python API and usage examples |
| [Development Guide](./development.md) | Development setup and contributing |
| [Future Work](./future-work.md) | Roadmap and enhancement opportunities |

## 🚀 Quick Start

### What is TradingAgents?

TradingAgents is a sophisticated multi-agent system that replicates the collaborative decision-making process of professional trading firms. It uses Large Language Models (LLMs) to power specialized agents that:

- **Analyze** market conditions from multiple perspectives
- **Research** investment opportunities through structured debates
- **Execute** trading strategies with risk management
- **Manage** portfolio decisions through consensus building

### Core Workflow

The system follows a structured 5-stage workflow:

```
I. Analyst Team → II. Research Team → III. Trader → IV. Risk Management → V. Portfolio Management
```

1. **Analyst Team**: Multiple analysts (Market, Social, News, Fundamentals) provide specialized analysis
2. **Research Team**: Bull and Bear researchers debate investment opportunities, managed by a Research Manager
3. **Trader**: Creates detailed trading plans based on analyst and research insights
4. **Risk Management**: Risk analysts (Aggressive, Conservative, Neutral) evaluate trading risks
5. **Portfolio Management**: Final decision authority that approves or rejects trades

### Key Features

- 🤖 **Multi-Agent Collaboration**: 11+ specialized AI agents working together
- 🔄 **Structured Debates**: Agents engage in formal debates to reach consensus
- 📊 **Multi-Source Data**: Integrates market data, news, social sentiment, and fundamentals
- 🎯 **LLM Flexibility**: Supports OpenAI, Anthropic, Google Gemini, Ollama, and OpenRouter
- 📱 **Rich CLI**: Beautiful terminal interface with real-time progress tracking
- 🔧 **Configurable**: Extensive configuration options for research depth and model selection

## 🛠️ Installation & Usage

### Prerequisites

- Python 3.10+
- API keys for data sources (FinnHub, OpenAI/Anthropic/Google)

### Install Dependencies

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
pip install -r requirements.txt
```

### Set Environment Variables

```bash
export FINNHUB_API_KEY=your_finnhub_key
export OPENAI_API_KEY=your_openai_key  # or other LLM provider keys
```

### Run Analysis

#### CLI Interface
```bash
python -m cli.standard
```

#### Python API
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize with default config
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Run analysis
final_state, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## 🏗️ System Architecture

The framework uses [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration and supports multiple LLM providers:

- **Agent Layer**: Specialized trading agents with unique roles
- **Graph Layer**: State management and workflow orchestration  
- **Data Layer**: Multi-source financial data integration
- **Memory Layer**: Agent memory for learning and consistency

## 📈 Example Output

The system produces comprehensive reports including:
- Technical market analysis with indicators (RSI, MACD, Bollinger Bands)
- Social sentiment analysis from Reddit and news sources
- Fundamental analysis with financial statements
- Structured investment debates between bull/bear perspectives
- Risk assessment from multiple risk tolerance levels
- Final portfolio management decisions

## ⚠️ Important Notes

- **Research Purpose**: This framework is designed for research and educational purposes
- **Not Financial Advice**: Trading performance may vary; this is not financial advice
- **API Costs**: The system makes numerous LLM API calls - monitor your usage
- **Data Dependencies**: Requires valid API keys for financial data sources

## 🤝 Contributing

We welcome contributions! See the [Development Guide](./development.md) for:
- Setting up the development environment
- Code style and standards
- Testing procedures
- Contribution workflow

## 📄 License

This project is licensed under the Apache 2.0 License. See [LICENSE](../LICENSE) for details.

## 🔗 Links

- [GitHub Repository](https://github.com/TauricResearch/TradingAgents)
- [Research Paper](https://arxiv.org/abs/2412.20138)
- [Tauric Research](https://tauric.ai/)
- [Discord Community](https://discord.com/invite/hk9PGKShPK)

---

**Need help?** Check the specific documentation sections linked above or join our Discord community for support. 
# TradingAgents Development Guide

This guide provides comprehensive information for developers who want to contribute to TradingAgents, extend its functionality, or set up a development environment.

## 🛠️ Development Environment Setup

### Prerequisites
- Python 3.10 or higher
- Git for version control
- API keys for testing (FinnHub, OpenAI, etc.)
- Optional: Docker for containerized development

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .  # Install in editable mode

# Set up environment variables
cp .env.example .env  # Copy and edit with your API keys
```

### Environment Variables
Create a `.env` file with your API credentials:
```bash
# Required for core functionality
FINNHUB_API_KEY=your_finnhub_api_key
OPENAI_API_KEY=your_openai_api_key

# Optional LLM providers
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Data configuration
TRADINGAGENTS_RESULTS_DIR=./results
TRADINGAGENTS_DATA_DIR=./data
```

### Development Dependencies
For development work, install additional packages:
```bash
pip install pytest pytest-cov black flake8 mypy pre-commit
```

## 🏗️ Project Structure

Understanding the codebase organization:

```
TradingAgents/
├── tradingagents/              # Main package
│   ├── agents/                 # Trading agents implementation
│   │   ├── analysts/           # Analyst agents (market, news, social, fundamentals)
│   │   ├── researchers/        # Research team (bull, bear)
│   │   ├── risk_mgmt/          # Risk management agents
│   │   ├── managers/           # Management agents (research, risk)
│   │   ├── trader/             # Trading execution agent
│   │   └── utils/              # Agent utilities and memory
│   ├── dataflows/              # Data acquisition and processing
│   │   ├── interface.py        # Unified data interface
│   │   ├── finnhub_utils.py    # FinnHub API integration
│   │   ├── yfin_utils.py       # Yahoo Finance integration
│   │   ├── reddit_utils.py     # Reddit data processing
│   │   └── stockstats_utils.py # Technical indicators
│   ├── graph/                  # LangGraph orchestration
│   │   ├── trading_graph.py    # Main graph class
│   │   ├── setup.py           # Graph configuration
│   │   ├── conditional_logic.py# Agent flow logic
│   │   └── propagation.py     # State management
│   └── default_config.py      # Default configuration
├── cli/                       # Command-line interface
│   ├── standard.py           # Main CLI application
│   ├── models.py             # CLI data models
│   └── utils.py              # CLI utilities
├── docs/                     # Documentation
├── tests/                    # Test suite
├── results/                  # Analysis outputs
└── requirements.txt          # Dependencies
```

## 🔧 Development Workflow

### Setting Up Git Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Code Formatting
We use Black for code formatting:
```bash
# Format all Python files
black .

# Check formatting without changing files
black --check .
```

### Linting
We use flake8 for linting:
```bash
# Run linting
flake8 tradingagents/ cli/ tests/

# Common settings in setup.cfg:
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv
```

### Type Checking
We use mypy for static type checking:
```bash
# Run type checking
mypy tradingagents/

# Configuration in mypy.ini:
[mypy]
python_version = 3.10
ignore_missing_imports = True
strict_optional = True
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tradingagents --cov-report=html

# Run specific test file
pytest tests/test_agents.py

# Run tests with specific marker
pytest -m "unit"
```

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── test_agents.py      # Agent functionality tests
│   ├── test_dataflows.py   # Data processing tests
│   └── test_config.py      # Configuration tests
├── integration/            # Integration tests
│   ├── test_graph.py       # Full workflow tests
│   └── test_api.py         # API integration tests
├── fixtures/               # Test data and fixtures
└── conftest.py            # Pytest configuration
```

### Writing Tests
Example test structure:
```python
# tests/unit/test_agents.py
import pytest
from unittest.mock import Mock, patch
from tradingagents.agents.analysts.market_analyst import create_market_analyst

@pytest.fixture
def mock_llm():
    """Mock LLM for testing"""
    llm = Mock()
    llm.invoke.return_value.content = "Mock analysis result"
    return llm

@pytest.fixture
def mock_toolkit():
    """Mock toolkit for testing"""
    toolkit = Mock()
    toolkit.get_YFin_data.return_value = "Mock price data"
    return toolkit

def test_market_analyst_creation(mock_llm, mock_toolkit):
    """Test market analyst can be created"""
    analyst = create_market_analyst(mock_llm, mock_toolkit)
    assert analyst is not None

@patch('tradingagents.agents.analysts.market_analyst.ChatPromptTemplate')
def test_market_analyst_analysis(mock_prompt, mock_llm, mock_toolkit):
    """Test market analyst performs analysis"""
    # Setup
    analyst = create_market_analyst(mock_llm, mock_toolkit)
    state = {
        "company_of_interest": "NVDA",
        "trade_date": "2024-05-01",
        "messages": []
    }
    
    # Execute
    result = analyst(state)
    
    # Assert
    assert "market_report" in result
    mock_toolkit.get_YFin_data.assert_called()
```

### Integration Testing
```python
# tests/integration/test_graph.py
import pytest
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

@pytest.mark.integration
def test_full_analysis_workflow():
    """Test complete analysis workflow"""
    config = DEFAULT_CONFIG.copy()
    config.update({
        "max_debate_rounds": 1,
        "online_tools": False,  # Use cached data for testing
        "quick_think_llm": "gpt-4o-mini"
    })
    
    ta = TradingAgentsGraph(
        selected_analysts=["market"],
        debug=False,
        config=config
    )
    
    final_state, decision = ta.propagate("NVDA", "2024-05-01")
    
    assert final_state is not None
    assert decision in ["BUY", "SELL", "HOLD"]
    assert "market_report" in final_state
```

## 🔧 Adding New Features

### Creating a New Agent
1. **Create Agent File**: Add new agent in appropriate subdirectory
```python
# tradingagents/agents/analysts/crypto_analyst.py
from langchain_core.prompts import ChatPromptTemplate

def create_crypto_analyst(llm, toolkit):
    """Create a cryptocurrency market analyst agent"""
    
    def crypto_analyst_node(state):
        ticker = state["company_of_interest"]
        current_date = state["trade_date"]
        
        # Define crypto-specific tools
        tools = [
            toolkit.get_crypto_data,
            toolkit.get_crypto_sentiment,
        ]
        
        # Create agent prompt
        system_message = """
        You are a cryptocurrency analyst specializing in digital asset markets.
        Analyze the provided crypto data and sentiment to generate insights.
        """
        
        # Implementation details...
        return updated_state
    
    return crypto_analyst_node
```

2. **Update Graph Setup**: Modify graph setup to include new agent
```python
# tradingagents/graph/setup.py
def setup_graph(self, selected_analysts):
    # Add crypto analyst option
    if "crypto" in selected_analysts:
        analyst_nodes["crypto"] = create_crypto_analyst(
            self.quick_thinking_llm, self.toolkit
        )
```

3. **Add Configuration**: Update configuration options
```python
# cli/utils.py
def select_analysts():
    analysts = [
        "market", "social", "news", "fundamentals", "crypto"  # Add crypto
    ]
    # Implementation...
```

### Adding New Data Sources
1. **Create Data Utility**: Add new data source integration
```python
# tradingagents/dataflows/blockchain_utils.py
import requests
from typing import Annotated

def get_blockchain_data(
    address: Annotated[str, "Blockchain address to analyze"],
    date: Annotated[str, "Analysis date in YYYY-MM-DD format"]
) -> str:
    """Fetch blockchain transaction data"""
    # Implementation
    pass

def get_defi_metrics(
    protocol: Annotated[str, "DeFi protocol name"],
    date: Annotated[str, "Analysis date"]
) -> str:
    """Fetch DeFi protocol metrics"""
    # Implementation
    pass
```

2. **Update Interface**: Add to unified data interface
```python
# tradingagents/dataflows/interface.py
from .blockchain_utils import get_blockchain_data, get_defi_metrics

# Export new functions
__all__ = [
    # ... existing exports
    "get_blockchain_data",
    "get_defi_metrics",
]
```

3. **Update Toolkit**: Add tools to agent toolkit
```python
# tradingagents/agents/utils/agent_utils.py
class Toolkit:
    def __init__(self, config):
        # ... existing init
        
    def get_crypto_data(self, symbol, date):
        """Get cryptocurrency data"""
        return get_blockchain_data(symbol, date)
```

### Extending LLM Support
1. **Add Provider Configuration**:
```python
# tradingagents/graph/trading_graph.py
def __init__(self, selected_analysts, debug, config):
    # Add new provider
    if self.config["llm_provider"].lower() == "custom_provider":
        from custom_provider import CustomLLM
        self.deep_thinking_llm = CustomLLM(model=self.config["deep_think_llm"])
        self.quick_thinking_llm = CustomLLM(model=self.config["quick_think_llm"])
```

2. **Update CLI Options**:
```python
# cli/utils.py
def select_llm_provider():
    providers = {
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "google": "Google Gemini",
        "ollama": "Ollama (Local)",
        "custom": "Custom Provider"  # Add new option
    }
```

## 📊 Performance Optimization

### Profiling
Use profiling tools to identify bottlenecks:
```python
import cProfile
import pstats

def profile_analysis():
    """Profile trading analysis performance"""
    profiler = cProfile.Profile()
    
    profiler.enable()
    # Run analysis
    ta = TradingAgentsGraph()
    final_state, decision = ta.propagate("NVDA", "2024-05-01")
    profiler.disable()
    
    # Save results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

# Run profiling
profile_analysis()
```

### Memory Optimization
Monitor memory usage:
```python
import tracemalloc
import psutil
import os

def monitor_memory():
    """Monitor memory usage during analysis"""
    process = psutil.Process(os.getpid())
    
    tracemalloc.start()
    
    # Run analysis
    ta = TradingAgentsGraph()
    final_state, decision = ta.propagate("NVDA", "2024-05-01")
    
    # Check memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    print(f"Process memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

### Caching Strategies
Implement caching for expensive operations:
```python
from functools import lru_cache
import pickle
import hashlib

class CachedAnalysis:
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _cache_key(self, ticker, date, config):
        """Generate cache key for analysis"""
        key_data = f"{ticker}_{date}_{hash(str(config))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_cached_analysis(self, ticker, date, config):
        """Retrieve cached analysis if available"""
        cache_key = self._cache_key(ticker, date, config)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def cache_analysis(self, ticker, date, config, result):
        """Cache analysis result"""
        cache_key = self._cache_key(ticker, date, config)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
```

## 🔧 Debugging

### Debug Mode
Enable comprehensive debugging:
```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Run with debug mode
ta = TradingAgentsGraph(debug=True)
```

### State Inspection
Inspect agent state during execution:
```python
def debug_state_changes(ta):
    """Add state debugging to trading graph"""
    original_propagate = ta.propagate
    
    def debug_propagate(ticker, date):
        print(f"Starting analysis for {ticker} on {date}")
        
        # Override graph to add debugging
        for chunk in ta.graph.stream(initial_state, **args):
            print(f"State update: {list(chunk.keys())}")
            if "messages" in chunk and chunk["messages"]:
                print(f"Latest message: {chunk['messages'][-1]}")
        
        return original_propagate(ticker, date)
    
    ta.propagate = debug_propagate
    return ta
```

### Error Handling
Implement comprehensive error handling:
```python
import traceback
from contextlib import contextmanager

@contextmanager
def error_handler(operation_name):
    """Context manager for handling errors with detailed logging"""
    try:
        yield
    except Exception as e:
        print(f"Error in {operation_name}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Log to file
        with open("error.log", "a") as f:
            f.write(f"{datetime.now()}: {operation_name} failed: {str(e)}\n")
            f.write(f"Traceback: {traceback.format_exc()}\n\n")
        
        raise

# Usage
with error_handler("Trading Analysis"):
    final_state, decision = ta.propagate("NVDA", "2024-05-01")
```

## 📝 Documentation

### Docstring Standards
Follow Google-style docstrings:
```python
def analyze_portfolio(tickers: List[str], date: str, config: Dict) -> Dict[str, str]:
    """Analyze multiple stocks in a portfolio.
    
    Args:
        tickers: List of stock ticker symbols to analyze.
        date: Analysis date in YYYY-MM-DD format.
        config: Configuration dictionary for analysis parameters.
    
    Returns:
        Dictionary mapping ticker symbols to trading decisions.
    
    Raises:
        ValueError: If date format is invalid.
        ConnectionError: If data sources are unavailable.
    
    Example:
        >>> portfolio = ["NVDA", "TSLA", "AAPL"]
        >>> results = analyze_portfolio(portfolio, "2024-05-01", config)
        >>> print(results["NVDA"])
        'BUY'
    """
```

### Adding Documentation
Update documentation when adding features:
1. Update relevant `.md` files in `docs/`
2. Add docstrings to new functions/classes
3. Include usage examples
4. Update API reference if needed

## 🤝 Contributing Guidelines

### Pull Request Process
1. **Fork Repository**: Create your own fork
2. **Create Branch**: Feature branch from main
3. **Make Changes**: Implement your feature/fix
4. **Add Tests**: Ensure adequate test coverage
5. **Update Docs**: Update relevant documentation
6. **Submit PR**: Create pull request with description

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] All tests pass
- [ ] Manual testing performed

## Documentation
- [ ] Updated docstrings
- [ ] Updated README/docs
- [ ] Added usage examples

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No new linting errors
- [ ] Backward compatibility maintained
```

### Code Review Checklist
**For Reviewers**:
- ✅ Code follows project conventions
- ✅ Adequate test coverage
- ✅ Documentation is updated
- ✅ No security vulnerabilities
- ✅ Performance impact considered
- ✅ Backward compatibility maintained

### Release Process
1. **Version Bump**: Update version in `setup.py`
2. **CHANGELOG**: Update changelog with new features
3. **Testing**: Run full test suite
4. **Documentation**: Ensure docs are current
5. **Tag Release**: Create git tag
6. **PyPI Upload**: Upload to package index

This development guide provides the foundation for contributing to TradingAgents effectively while maintaining code quality and system reliability. 
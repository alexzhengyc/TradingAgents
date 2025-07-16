# TradingAgents API Reference

This document provides comprehensive API reference documentation for the TradingAgents Python library, including classes, methods, and usage examples.

## 📚 Core API Overview

The TradingAgents API consists of several key components:

- **TradingAgentsGraph**: Main orchestration class
- **Configuration System**: Flexible configuration management  
- **Agent Classes**: Individual trading agent implementations
- **Data Interface**: Unified data access layer
- **Memory System**: Agent learning and persistence

## 🎯 Quick Start

### Basic Usage
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize with default configuration
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Run analysis
final_state, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

### Custom Configuration
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create custom configuration
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-opus-20240229",
    "max_debate_rounds": 3,
    "selected_analysts": ["market", "news", "fundamentals"]
})

# Initialize with custom config
ta = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    debug=True,
    config=config
)

# Run analysis
final_state, decision = ta.propagate("TSLA", "2024-03-15")
```

## 🏗️ Core Classes

### TradingAgentsGraph

**Primary Class**: Main orchestration class for the trading agents system.

#### Constructor
```python
class TradingAgentsGraph:
    def __init__(
        self,
        selected_analysts: List[str] = ["market", "social", "news", "fundamentals"],
        debug: bool = False,
        config: Dict[str, Any] = None
    ):
```

**Parameters**:
- `selected_analysts` (List[str]): Analysts to include in analysis
  - Options: `"market"`, `"social"`, `"news"`, `"fundamentals"`
  - Default: All four analysts
- `debug` (bool): Enable debug mode with detailed logging
- `config` (Dict): Configuration dictionary (uses DEFAULT_CONFIG if None)

**Example**:
```python
# Minimal initialization
ta = TradingAgentsGraph()

# Custom analyst selection
ta = TradingAgentsGraph(selected_analysts=["market", "fundamentals"])

# Full customization
ta = TradingAgentsGraph(
    selected_analysts=["market", "news"],
    debug=True,
    config=custom_config
)
```

#### propagate() Method
```python
def propagate(
    self, 
    company_name: str, 
    trade_date: str
) -> Tuple[Dict[str, Any], str]:
```

**Purpose**: Runs the complete trading analysis workflow.

**Parameters**:
- `company_name` (str): Stock ticker symbol (e.g., "NVDA", "TSLA", "AAPL")
- `trade_date` (str): Analysis date in YYYY-MM-DD format

**Returns**:
- `Tuple[Dict[str, Any], str]`: 
  - Final state dictionary with all agent outputs
  - Processed trading decision signal

**Example**:
```python
# Basic analysis
final_state, decision = ta.propagate("NVDA", "2024-05-10")

# Access individual reports
market_report = final_state.get("market_report", "")
news_report = final_state.get("news_report", "")
final_decision = final_state.get("final_trade_decision", "")

print(f"Trading Decision: {decision}")
print(f"Market Analysis: {market_report}")
```

#### process_signal() Method
```python
def process_signal(self, decision_text: str) -> str:
```

**Purpose**: Processes raw decision text into standardized trading signals.

**Parameters**:
- `decision_text` (str): Raw decision text from portfolio manager

**Returns**:
- `str`: Processed trading signal (BUY/SELL/HOLD)

**Example**:
```python
raw_decision = final_state["final_trade_decision"]
processed_signal = ta.process_signal(raw_decision)
print(f"Signal: {processed_signal}")
```

#### reflect() Method
```python
def reflect(
    self, 
    decision: str, 
    actual_outcome: str
) -> str:
```

**Purpose**: Performs reflection on past decisions to improve future performance.

**Parameters**:
- `decision` (str): Previous trading decision
- `actual_outcome` (str): Actual market outcome/performance

**Returns**:
- `str`: Reflection analysis and lessons learned

**Example**:
```python
# After some time has passed
actual_outcome = "Stock increased 15% over 3 months"
reflection = ta.reflect(decision, actual_outcome)
print(f"Lessons learned: {reflection}")
```

## 🔧 Configuration API

### DEFAULT_CONFIG Dictionary
```python
from tradingagents.default_config import DEFAULT_CONFIG

# Access default settings
print(DEFAULT_CONFIG["llm_provider"])        # "openai"
print(DEFAULT_CONFIG["max_debate_rounds"])   # 1

# Create modified configuration
config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 3
config["llm_provider"] = "anthropic"
```

### Configuration Validation
```python
def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration parameters"""
    required_keys = [
        "llm_provider", "deep_think_llm", "quick_think_llm",
        "max_debate_rounds", "max_risk_discuss_rounds"
    ]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    return True

# Usage
try:
    validate_config(my_config)
    ta = TradingAgentsGraph(config=my_config)
except ValueError as e:
    print(f"Configuration error: {e}")
```

## 📊 Data Interface API

### Market Data Functions
```python
from tradingagents.dataflows.interface import (
    get_YFin_data,
    get_YFin_data_online,
    get_stockstats_indicator,
    get_stock_stats_indicators_window
)

# Historical price data (offline)
price_data = get_YFin_data("NVDA", "2024-04-01", "2024-05-01")

# Real-time price data (online)
live_data = get_YFin_data_online("NVDA", "2024-04-01", "2024-05-01")

# Technical indicator
rsi_value = get_stockstats_indicator("NVDA", "rsi", "2024-05-01", online=True)

# Indicator time series
rsi_history = get_stock_stats_indicators_window(
    symbol="NVDA",
    indicator="rsi", 
    curr_date="2024-05-01",
    look_back_days=30,
    online=True
)
```

### News Data Functions
```python
from tradingagents.dataflows.interface import (
    get_finnhub_news,
    get_google_news
)

# Company-specific news
company_news = get_finnhub_news(
    ticker="NVDA",
    curr_date="2024-05-01", 
    look_back_days=7
)

# General market news
market_news = get_google_news(
    curr_date="2024-05-01",
    look_back_days=7
)
```

### Fundamental Data Functions
```python
from tradingagents.dataflows.interface import (
    get_simfin_balance_sheet,
    get_simfin_income_statements,
    get_simfin_cashflow
)

# Financial statements
balance_sheet = get_simfin_balance_sheet("NVDA", "quarterly", "2024-05-01")
income_stmt = get_simfin_income_statements("NVDA", "quarterly", "2024-05-01")
cash_flow = get_simfin_cashflow("NVDA", "quarterly", "2024-05-01")
```

### Social Media Data Functions
```python
from tradingagents.dataflows.interface import (
    get_reddit_company_news,
    get_reddit_global_news
)

# Company-specific Reddit sentiment
company_sentiment = get_reddit_company_news(
    ticker="NVDA",
    date="2024-05-01",
    max_posts=50
)

# General market sentiment
market_sentiment = get_reddit_global_news(
    date="2024-05-01", 
    max_posts=100
)
```

## 🧠 Memory System API

### FinancialSituationMemory Class
```python
from tradingagents.agents.utils.memory import FinancialSituationMemory

# Initialize memory for an agent
memory = FinancialSituationMemory("trader_memory", config)

# Add new memory
memory.add_memory(
    situation="NVDA analysis on 2024-05-01",
    decision="BUY recommendation with 2% allocation", 
    outcome="15% gain over 3 months"
)

# Retrieve relevant memories
current_situation = "TSLA analysis showing strong growth"
relevant_memories = memory.get_memories(current_situation, n_matches=3)

for memory_item in relevant_memories:
    print(f"Past situation: {memory_item['situation']}")
    print(f"Decision: {memory_item['decision']}")
    print(f"Outcome: {memory_item['outcome']}")
```

## 🤖 Individual Agent APIs

### Market Analyst
```python
from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.agents.utils.agent_utils import Toolkit

# Create market analyst
llm = ChatOpenAI(model="gpt-4o-mini")
toolkit = Toolkit(config=config)
market_analyst = create_market_analyst(llm, toolkit)

# Run market analysis (within graph context)
state = {
    "company_of_interest": "NVDA",
    "trade_date": "2024-05-01",
    "messages": []
}
result = market_analyst(state)
```

### News Analyst
```python
from tradingagents.agents.analysts.news_analyst import create_news_analyst

# Create and run news analyst
news_analyst = create_news_analyst(llm, toolkit)
result = news_analyst(state)
```

### Research Agents
```python
from tradingagents.agents.researchers.bull_researcher import create_bull_researcher
from tradingagents.agents.researchers.bear_researcher import create_bear_researcher
from tradingagents.agents.utils.memory import FinancialSituationMemory

# Create researchers with memory
bull_memory = FinancialSituationMemory("bull_memory", config)
bear_memory = FinancialSituationMemory("bear_memory", config)

bull_researcher = create_bull_researcher(llm, bull_memory)
bear_researcher = create_bear_researcher(llm, bear_memory)
```

## 📈 Advanced Usage Examples

### Batch Analysis
```python
def batch_analyze(tickers: List[str], date: str, config: Dict) -> Dict[str, str]:
    """Analyze multiple stocks in batch"""
    ta = TradingAgentsGraph(config=config)
    results = {}
    
    for ticker in tickers:
        try:
            final_state, decision = ta.propagate(ticker, date)
            results[ticker] = decision
            print(f"Completed analysis for {ticker}: {decision}")
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            results[ticker] = "ERROR"
    
    return results

# Usage
tech_stocks = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL"]
results = batch_analyze(tech_stocks, "2024-05-01", DEFAULT_CONFIG)
```

### Custom Analysis Pipeline
```python
class CustomTradingPipeline:
    def __init__(self, config):
        self.config = config
        self.ta = TradingAgentsGraph(config=config)
        
    def analyze_with_risk_management(self, ticker: str, date: str, portfolio_allocation: float):
        """Custom analysis with portfolio-specific risk management"""
        
        # Run standard analysis
        final_state, decision = self.ta.propagate(ticker, date)
        
        # Apply custom risk filters
        if portfolio_allocation > 0.05:  # More than 5% allocation
            risk_adjustment = self._apply_concentration_risk(decision, portfolio_allocation)
            decision = risk_adjustment
            
        # Log analysis
        self._log_analysis(ticker, date, final_state, decision)
        
        return final_state, decision
    
    def _apply_concentration_risk(self, decision: str, allocation: float) -> str:
        """Apply concentration risk adjustments"""
        if "BUY" in decision and allocation > 0.10:
            return decision.replace("BUY", "HOLD")  # Reduce position if over 10%
        return decision
    
    def _log_analysis(self, ticker: str, date: str, state: Dict, decision: str):
        """Log analysis results"""
        with open(f"analysis_log_{date}.txt", "a") as f:
            f.write(f"{ticker}: {decision}\n")

# Usage
pipeline = CustomTradingPipeline(config)
state, decision = pipeline.analyze_with_risk_management("NVDA", "2024-05-01", 0.08)
```

### Real-time Monitoring
```python
import time
from datetime import datetime

class RealTimeMonitor:
    def __init__(self, config):
        self.config = config
        self.ta = TradingAgentsGraph(config=config)
        
    def monitor_portfolio(self, tickers: List[str], check_interval: int = 3600):
        """Monitor portfolio stocks in real-time"""
        while True:
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            for ticker in tickers:
                try:
                    # Run quick analysis
                    quick_config = self.config.copy()
                    quick_config.update({
                        "selected_analysts": ["market", "news"],
                        "max_debate_rounds": 1
                    })
                    
                    ta = TradingAgentsGraph(config=quick_config)
                    final_state, decision = ta.propagate(ticker, current_date)
                    
                    # Check for significant changes
                    if self._significant_change_detected(ticker, decision):
                        self._alert_user(ticker, decision)
                        
                except Exception as e:
                    print(f"Error monitoring {ticker}: {e}")
            
            # Wait before next check
            time.sleep(check_interval)
    
    def _significant_change_detected(self, ticker: str, decision: str) -> bool:
        """Check if decision represents significant change"""
        # Implement change detection logic
        return "SELL" in decision  # Alert on sell signals
    
    def _alert_user(self, ticker: str, decision: str):
        """Send alert to user"""
        print(f"ALERT: {ticker} - {decision}")
        # Could integrate with email, Slack, etc.

# Usage
monitor = RealTimeMonitor(config)
portfolio = ["NVDA", "TSLA", "AAPL"]
monitor.monitor_portfolio(portfolio, check_interval=1800)  # Check every 30 minutes
```

## 🔍 Error Handling

### Common Exceptions
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

try:
    ta = TradingAgentsGraph(config=invalid_config)
except ValueError as e:
    print(f"Configuration error: {e}")

try:
    final_state, decision = ta.propagate("INVALID_TICKER", "2024-05-01")
except Exception as e:
    print(f"Analysis error: {e}")
```

### Graceful Degradation
```python
def robust_analysis(ticker: str, date: str, config: Dict) -> Tuple[Dict, str]:
    """Analysis with fallback options"""
    
    # Try full analysis first
    try:
        ta = TradingAgentsGraph(config=config)
        return ta.propagate(ticker, date)
    except Exception as e:
        print(f"Full analysis failed: {e}")
    
    # Fall back to simplified analysis
    try:
        simple_config = config.copy()
        simple_config.update({
            "selected_analysts": ["market"],
            "max_debate_rounds": 1,
            "online_tools": False
        })
        ta = TradingAgentsGraph(config=simple_config)
        return ta.propagate(ticker, date)
    except Exception as e:
        print(f"Simple analysis failed: {e}")
        return {}, "HOLD"  # Default conservative decision

# Usage
final_state, decision = robust_analysis("NVDA", "2024-05-01", config)
```

## 📊 Performance Optimization

### Async Analysis (Conceptual)
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def async_analyze_portfolio(tickers: List[str], date: str, config: Dict):
    """Analyze multiple stocks concurrently"""
    
    def analyze_single(ticker):
        ta = TradingAgentsGraph(config=config)
        return ta.propagate(ticker, date)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, analyze_single, ticker)
            for ticker in tickers
        ]
        results = await asyncio.gather(*futures)
    
    return dict(zip(tickers, results))

# Usage
portfolio = ["NVDA", "TSLA", "AAPL"]
results = asyncio.run(async_analyze_portfolio(portfolio, "2024-05-01", config))
```

This API reference provides comprehensive coverage of the TradingAgents Python interface, enabling you to build sophisticated trading analysis applications and integrate the framework into your existing systems. 
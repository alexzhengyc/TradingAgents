# TradingAgents Agent Reference

This document provides comprehensive details about each agent in the TradingAgents system, including their roles, capabilities, data sources, and implementation details.

## 🎯 Agent Overview

The TradingAgents framework employs 11+ specialized AI agents organized into 5 teams:

| Team | Agents | Primary Function |
|------|--------|------------------|
| **Analyst Team** | Market, Social, News, Fundamentals | Data gathering and initial analysis |
| **Research Team** | Bull, Bear, Research Manager | Investment opportunity evaluation |
| **Trading Team** | Trader | Execution planning and strategy |
| **Risk Management** | Aggressive, Conservative, Neutral | Risk assessment |
| **Portfolio Management** | Portfolio Manager | Final decision authority |

## 📊 Analyst Team

### Market Analyst
**Role**: Technical market analysis and trend identification

**Data Sources**:
- Yahoo Finance historical price data
- Technical indicators (RSI, MACD, Bollinger Bands, ATR, etc.)
- Volume and price action analysis

**Key Capabilities**:
```python
tools = [
    toolkit.get_YFin_data,                          # Price data retrieval
    toolkit.get_stockstats_indicators_report,       # Technical indicators
]

# Available Technical Indicators:
indicators = [
    "close_50_sma",    # 50-day Simple Moving Average
    "close_200_sma",   # 200-day Simple Moving Average  
    "close_10_ema",    # 10-day Exponential Moving Average
    "macd",            # MACD Line
    "macds",           # MACD Signal Line
    "macdh",           # MACD Histogram
    "rsi",             # Relative Strength Index
    "boll",            # Bollinger Middle Band
    "boll_ub",         # Bollinger Upper Band
    "boll_lb",         # Bollinger Lower Band
    "atr",             # Average True Range
    "vwma",            # Volume Weighted Moving Average
]
```

**Analysis Process**:
1. Retrieves historical price data for specified date range
2. Calculates up to 8 complementary technical indicators
3. Analyzes trends, support/resistance levels, and momentum
4. Provides detailed trading insights and pattern recognition

**Output Example**:
```
### Market Analysis for NVDA (2024-05-10)

Technical Indicators Analysis:
- RSI (14): 67.3 - Approaching overbought territory
- MACD: Bullish crossover detected on 2024-05-08
- Bollinger Bands: Price trading near upper band, potential resistance at $925
- 50-day SMA: Strong uptrend, acting as dynamic support at $885

Key Findings:
- Strong upward momentum with healthy volume confirmation
- Potential short-term resistance at $925 level
- Overall bullish trend remains intact
```

### Social Media Analyst
**Role**: Social sentiment analysis and community opinion monitoring

**Data Sources**:
- Reddit posts and comments from finance-related subreddits
- Social media sentiment scoring
- Community discussion analysis

**Key Capabilities**:
```python
tools = [
    toolkit.get_reddit_company_news,    # Company-specific Reddit discussions
    toolkit.get_reddit_global_news,     # General market sentiment
]

# Monitored Subreddits:
subreddits = [
    "investing", "stocks", "SecurityAnalysis", "ValueInvesting",
    "financialindependence", "SecurityAnalysis", "pennystocks"
]
```

**Analysis Process**:
1. Fetches recent posts mentioning target company
2. Analyzes sentiment using scoring algorithms
3. Identifies trending topics and community concerns
4. Quantifies bullish vs bearish sentiment ratios

**Output Example**:
```
### Social Sentiment Analysis for NVDA (2024-05-10)

Sentiment Summary:
- Overall Sentiment: Bullish (72% positive, 18% neutral, 10% negative)
- Post Volume: 145 mentions across monitored subreddits
- Trending Topics: AI chip demand, earnings expectations, competition

Key Insights:
- Strong positive sentiment around AI market growth
- Some concerns about valuation levels
- Community expects strong Q1 earnings results
```

### News Analyst
**Role**: News events and macroeconomic analysis

**Data Sources**:
- FinnHub news API for company-specific news
- Google News for broader market context
- Macroeconomic event analysis

**Key Capabilities**:
```python
tools = [
    toolkit.get_finnhub_news,      # Company-specific news
    toolkit.get_google_news,       # General market news
]
```

**Analysis Process**:
1. Retrieves recent news within specified lookback period
2. Categorizes news by impact level and relevance
3. Analyzes macroeconomic implications
4. Identifies potential market-moving events

**Output Example**:
```
### News Analysis for NVDA (2024-05-10)

Recent News Summary:
- NVIDIA announces new AI chip architecture (May 8) - Positive impact
- Fed interest rate decision pending (May 15) - Neutral to market
- China semiconductor restrictions update (May 6) - Negative risk

Market Context:
- Tech sector showing resilience despite rate concerns
- AI infrastructure spending continues to accelerate
- Regulatory environment remains uncertain but manageable
```

### Fundamentals Analyst
**Role**: Financial statement analysis and valuation assessment

**Data Sources**:
- SimFin financial statements (Balance Sheet, Income Statement, Cash Flow)
- Yahoo Finance fundamental metrics
- Historical financial ratios and trends

**Key Capabilities**:
```python
tools = [
    toolkit.get_simfin_balance_sheet,      # Balance sheet data
    toolkit.get_simfin_income_statements,  # Income statement data  
    toolkit.get_simfin_cashflow,          # Cash flow statement
]

# Available Frequencies:
frequencies = ["annual", "quarterly"]
```

**Analysis Process**:
1. Retrieves latest available financial statements
2. Calculates key financial ratios and metrics
3. Analyzes trends in profitability, liquidity, and leverage
4. Assesses financial health and valuation

**Output Example**:
```
### Fundamentals Analysis for NVDA (Q1 2024)

Financial Health:
- Revenue Growth: 262% YoY (exceptional growth in data center segment)
- Gross Margin: 73.2% (industry-leading profitability)
- ROE: 85.6% (excellent returns to shareholders)
- Debt-to-Equity: 0.15 (conservative capital structure)

Valuation Metrics:
- Forward P/E: 31.2x (premium but justified by growth)
- EV/Sales: 22.1x (elevated but declining with revenue growth)
- Free Cash Flow Yield: 2.8% (strong cash generation)
```

## 🔬 Research Team

### Bull Researcher
**Role**: Advocates for positive investment positions

**Memory System**: Maintains memory of successful bull arguments and market conditions

**Analysis Approach**:
- Identifies growth opportunities and competitive advantages
- Emphasizes positive catalysts and market trends
- Builds strong cases for buy/hold recommendations
- Challenges bear arguments with counter-evidence

**Typical Arguments**:
```
Bull Position on NVDA:
1. Dominant position in AI chip market with 80%+ market share
2. Expanding TAM with AI adoption across industries
3. Strong pricing power and margin expansion capability
4. Diversification into automotive and edge computing markets
5. Robust R&D pipeline ensuring technological leadership
```

### Bear Researcher
**Role**: Advocates for cautious or negative investment positions

**Memory System**: Tracks successful bear cases and risk factors

**Analysis Approach**:
- Identifies risks, weaknesses, and negative catalysts
- Challenges growth assumptions and valuation metrics
- Considers downside scenarios and market headwinds
- Provides counterarguments to bull positions

**Typical Arguments**:
```
Bear Position on NVDA:
1. Extreme valuation multiples leave little room for error
2. Cyclical nature of semiconductor industry suggests downturn ahead
3. Increasing competition from AMD, Intel, and custom chips
4. Regulatory risks in China market (significant revenue exposure)
5. AI bubble concerns with potential for demand normalization
```

### Research Manager
**Role**: Moderates debates and makes final investment recommendations

**LLM Configuration**: Uses "deep thinking" model for complex reasoning

**Decision Process**:
1. Reviews complete debate history from Bull and Bear researchers
2. Weighs evidence and arguments from both perspectives
3. Considers market context and timing factors
4. Makes final investment recommendation with reasoning

**Decision Framework**:
```python
decision_factors = [
    "strength_of_bull_arguments",
    "validity_of_bear_concerns", 
    "market_timing_considerations",
    "risk_reward_analysis",
    "confidence_level_assessment"
]
```

## 💼 Trading Team

### Trader
**Role**: Creates detailed execution plans and trading strategies

**Memory System**: Learns from past trading decisions and market outcomes

**Inputs**:
- Investment recommendation from Research Manager
- All analyst reports (Market, Social, News, Fundamentals)
- Historical trading performance and lessons learned

**Strategy Development**:
```python
trading_plan_components = [
    "position_sizing",         # Risk-adjusted position size
    "entry_strategy",         # Optimal entry points and timing
    "exit_strategy",          # Profit targets and stop losses
    "risk_management",        # Maximum loss limits
    "market_conditions",      # Favorable execution environment
    "contingency_plans"       # Alternative scenarios
]
```

**Output Example**:
```
### Trading Plan for NVDA (2024-05-10)

Recommendation: BUY
Position Size: 2% of portfolio
Entry Strategy: 
- Primary entry: Market open at $920-925
- Secondary entry: On any dip to $900-905 support

Risk Management:
- Stop Loss: $875 (-5% from entry)
- Position limit: Maximum 3% of portfolio
- Time horizon: 3-6 months

Execution Notes:
- Use limit orders to avoid market impact
- Consider scaling in over 2-3 days
- Monitor volume for optimal entry timing
```

## ⚖️ Risk Management Team

### Aggressive (Risky) Analyst
**Role**: Evaluates high-risk, high-reward scenarios

**Risk Tolerance**: High appetite for risk and volatility

**Evaluation Criteria**:
- Potential for outsized returns
- Willingness to accept higher volatility
- Focus on growth opportunities over preservation
- Aggressive position sizing recommendations

**Analysis Style**:
```
Aggressive Risk Assessment:
- Comfortable with 5-7% portfolio allocation
- Supportive of leveraged positions if fundamentals strong
- Views current volatility as opportunity rather than threat
- Recommends increasing position on any market weakness
```

### Conservative (Safe) Analyst  
**Role**: Emphasizes capital preservation and downside protection

**Risk Tolerance**: Low appetite for risk and volatility

**Evaluation Criteria**:
- Capital preservation as primary objective
- Emphasis on downside protection
- Conservative position sizing
- Focus on stable, established companies

**Analysis Style**:
```
Conservative Risk Assessment:
- Recommends limiting position to 1-2% of portfolio
- Suggests adding only on significant market weakness
- Concerned about current valuation levels
- Emphasizes importance of diversification
```

### Neutral Analyst
**Role**: Provides balanced risk assessment

**Risk Tolerance**: Moderate, balanced approach

**Evaluation Criteria**:
- Balanced risk-reward evaluation
- Standard portfolio allocation guidelines
- Objective assessment of probabilities
- Middle-ground perspective on uncertainties

**Analysis Style**:
```
Neutral Risk Assessment:
- Standard 2-3% portfolio allocation appropriate
- Current risk levels within acceptable parameters
- Recommends standard position sizing with monitoring
- Balanced view on timing and execution
```

## 👔 Portfolio Management

### Portfolio Manager
**Role**: Final decision authority with portfolio-wide perspective

**LLM Configuration**: Uses "deep thinking" model for final decisions

**Decision Factors**:
```python
portfolio_considerations = [
    "overall_portfolio_balance",     # Sector and asset allocation
    "correlation_with_existing",     # Diversification impact
    "risk_budget_utilization",      # Total portfolio risk
    "liquidity_requirements",       # Cash flow considerations
    "regulatory_constraints",       # Compliance requirements
    "market_timing_factors"         # Macro environment assessment
]
```

**Final Decision Process**:
1. Reviews all risk analyst assessments
2. Considers portfolio-wide implications
3. Evaluates alignment with investment objectives
4. Makes final approve/reject/modify decision

**Decision Output Example**:
```
### Portfolio Management Decision - NVDA

DECISION: APPROVED with modifications

Rationale:
- Strong fundamental case supported by analyst team
- Risk assessments show manageable downside
- Position fits within technology sector allocation limits
- Current market conditions favorable for execution

Modifications to Trading Plan:
- Reduce position size from 2% to 1.5% of portfolio
- Implement staged entry over 5 trading days
- Add hedging via sector ETF put options
- Establish profit-taking levels at +20% and +35%

Final Authorization: Proceed with modified parameters
```

## 🧠 Agent Memory System

### Memory Architecture
Each agent maintains persistent memory using vector embeddings:

```python
class FinancialSituationMemory:
    def __init__(self, name: str, config: Dict):
        self.embeddings = OpenAIEmbeddings()  # or other embedding models
        self.vector_store = Chroma(collection_name=name)
    
    def add_memory(self, situation: str, decision: str, outcome: str):
        # Store successful/failed decision patterns
    
    def get_memories(self, current_situation: str, n_matches: int = 2):
        # Retrieve similar past situations
```

### Memory Types by Agent:
- **Bull/Bear Researchers**: Successful argument patterns and market contexts
- **Trader**: Trading outcomes and strategy effectiveness  
- **Research Manager**: Decision quality and prediction accuracy
- **Portfolio Manager**: Portfolio-level decisions and risk outcomes

## 🔧 Agent Configuration

### LLM Assignment Strategy
```python
# Quick thinking agents (routine analysis)
quick_agents = [
    "Market Analyst", "Social Analyst", "News Analyst", 
    "Fundamentals Analyst", "Bull Researcher", "Bear Researcher",
    "Trader", "Risk Analysts"
]

# Deep thinking agents (complex reasoning)
deep_agents = [
    "Research Manager", "Portfolio Manager"
]
```

### Customization Options
- **Agent Selection**: Choose subset of analysts (market, social, news, fundamentals)
- **Debate Rounds**: Configure research and risk debate intensity
- **Memory Settings**: Adjust learning and recall parameters
- **Tool Configuration**: Online vs offline data sources

This agent system provides comprehensive market analysis through specialized expertise while maintaining flexibility for different use cases and research objectives. 
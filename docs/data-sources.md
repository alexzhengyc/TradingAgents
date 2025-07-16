# TradingAgents Data Sources Guide

This document details the data sources, data pipeline, and data processing capabilities of the TradingAgents framework.

## 📊 Data Source Overview

TradingAgents integrates multiple financial data sources to provide comprehensive market intelligence:

| Data Source | Provider | Data Types | Update Frequency |
|-------------|----------|------------|------------------|
| **Market Data** | Yahoo Finance | OHLCV, Technical Indicators | Real-time/Daily |
| **News Data** | FinnHub, Google News | Company News, Market News | Real-time |
| **Social Sentiment** | Reddit | Posts, Comments, Sentiment | Real-time |
| **Fundamentals** | SimFin | Financial Statements | Quarterly/Annual |
| **Technical Analysis** | StockStats | 50+ Technical Indicators | Real-time |

## 🏗️ Data Architecture

### Data Flow Pipeline
```
External APIs → Data Utils → Cache Layer → Agent Tools → Analysis
     ↓              ↓           ↓            ↓           ↓
  Raw Data    → Processed  → Stored    → Formatted → Insights
```

### Data Processing Layers

1. **Data Acquisition Layer**: Raw data retrieval from external APIs
2. **Processing Layer**: Data cleaning, formatting, and calculation
3. **Caching Layer**: Local storage for performance and offline use
4. **Interface Layer**: Unified API for agent consumption
5. **Tool Layer**: Agent-specific data access methods

## 📈 Market Data Sources

### Yahoo Finance (YFinance)
**Primary Use**: Historical price data and basic fundamentals

**Data Types**:
- OHLCV (Open, High, Low, Close, Volume) data
- Adjusted closing prices
- Stock splits and dividends
- Basic company information

**Implementation**:
```python
# Online data retrieval
def get_YFin_data_online(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol.upper())
    data = ticker.history(start=start_date, end=end_date)
    return data

# Offline cached data
def get_YFin_data(symbol, start_date, end_date):
    data_file = f"{symbol}-YFin-data-2015-01-01-2025-03-25.csv"
    data = pd.read_csv(data_file)
    filtered_data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]
    return filtered_data
```

**Available Functions**:
- `get_YFin_data()`: Cached historical data (2015-2025)
- `get_YFin_data_online()`: Real-time data retrieval
- `get_YFin_data_window()`: Data within lookback window

### Technical Indicators (StockStats)
**Primary Use**: Technical analysis calculations

**Available Indicators**:
```python
technical_indicators = {
    # Moving Averages
    "close_50_sma": "50-day Simple Moving Average",
    "close_200_sma": "200-day Simple Moving Average", 
    "close_10_ema": "10-day Exponential Moving Average",
    "vwma": "Volume Weighted Moving Average",
    
    # Momentum Indicators
    "rsi": "Relative Strength Index (14-period)",
    "macd": "MACD Line",
    "macds": "MACD Signal Line", 
    "macdh": "MACD Histogram",
    
    # Volatility Indicators
    "boll": "Bollinger Middle Band (20-period)",
    "boll_ub": "Bollinger Upper Band (+2 std dev)",
    "boll_lb": "Bollinger Lower Band (-2 std dev)",
    "atr": "Average True Range (14-period)",
}
```

**Usage Examples**:
```python
# Get single indicator value
rsi_value = get_stockstats_indicator("NVDA", "rsi", "2024-05-10", online=True)

# Get indicator time series
rsi_window = get_stock_stats_indicators_window(
    symbol="NVDA", 
    indicator="rsi", 
    curr_date="2024-05-10",
    look_back_days=30,
    online=True
)
```

## 📰 News Data Sources

### FinnHub News API
**Primary Use**: Company-specific news and financial events

**Data Coverage**:
- Company-specific news articles
- Market-moving announcements
- Earnings releases and guidance
- Regulatory filings and updates

**Data Structure**:
```python
news_entry = {
    "headline": "NVIDIA Reports Record Q1 Revenue",
    "summary": "NVIDIA reported Q1 revenue of $60.9B, up 262% YoY...",
    "datetime": "2024-05-08T16:30:00Z",
    "source": "NVIDIA Corp",
    "url": "https://...",
    "category": "earnings"
}
```

**Implementation**:
```python
def get_finnhub_news(ticker, curr_date, look_back_days):
    start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    before = start_date - relativedelta(days=look_back_days)
    
    # Retrieve cached news data
    result = get_data_in_range(ticker, before, curr_date, "news_data", DATA_DIR)
    
    # Format for agent consumption
    combined_result = ""
    for day, data in result.items():
        for entry in data:
            formatted_news = f"### {entry['headline']} ({day})\n{entry['summary']}"
            combined_result += formatted_news + "\n\n"
    
    return f"## {ticker} News, from {before} to {curr_date}:\n" + combined_result
```

### Google News Integration
**Primary Use**: Broader market context and macroeconomic news

**Data Coverage**:
- Global financial markets news
- Economic policy updates
- Central bank announcements
- Geopolitical events affecting markets

## 📱 Social Media Data

### Reddit Sentiment Analysis
**Primary Use**: Retail investor sentiment and community discussion analysis

**Monitored Subreddits**:
```python
subreddits = [
    "investing",              # General investment discussions
    "stocks",                 # Stock-specific conversations
    "SecurityAnalysis",       # Fundamental analysis discussions
    "ValueInvesting",         # Value investment community
    "financialindependence",  # FIRE community discussions
    "pennystocks",            # Small-cap stock discussions
    "options",                # Options trading discussions
]
```

**Data Processing**:
```python
def fetch_top_from_category(category, date, max_limit, query=None):
    """
    Fetch top posts from Reddit for specific date and company
    
    Args:
        category: Subreddit category (e.g., "company_news", "global_news")
        date: Target date for analysis (YYYY-MM-DD)
        max_limit: Maximum number of posts to retrieve
        query: Company ticker for filtering (e.g., "NVDA")
    
    Returns:
        List of relevant posts with sentiment scoring
    """
    posts = []
    
    for data_file in os.listdir(reddit_data_path):
        with open(data_file, 'rb') as f:
            for line in f:
                parsed_line = json.loads(line)
                
                # Filter by date
                post_date = datetime.utcfromtimestamp(parsed_line["created_utc"])
                if post_date.strftime("%Y-%m-%d") != date:
                    continue
                
                # Filter by company mention (if query provided)
                if query and not company_mentioned(parsed_line, query):
                    continue
                
                post = {
                    "title": parsed_line["title"],
                    "content": parsed_line["selftext"], 
                    "upvotes": parsed_line["ups"],
                    "posted_date": post_date.strftime("%Y-%m-%d"),
                    "url": parsed_line["url"]
                }
                posts.append(post)
    
    return sorted(posts, key=lambda x: x["upvotes"], reverse=True)[:max_limit]
```

**Sentiment Analysis Features**:
- Automated sentiment scoring (positive/negative/neutral)
- Upvote weighting for relevance
- Topic trend identification
- Community consensus analysis

## 💰 Fundamental Data Sources

### SimFin Financial Statements
**Primary Use**: Comprehensive financial statement analysis

**Available Statements**:
1. **Balance Sheet**: Assets, liabilities, and equity
2. **Income Statement**: Revenue, expenses, and profitability
3. **Cash Flow Statement**: Operating, investing, and financing activities

**Data Structure**:
```python
# Balance Sheet Example
balance_sheet_fields = [
    "Report Date", "Publish Date", "Ticker", "Currency",
    # Assets
    "Total Assets", "Current Assets", "Cash & Cash Equivalents",
    "Accounts Receivable", "Inventories", "Property Plant & Equipment",
    # Liabilities  
    "Total Liabilities", "Current Liabilities", "Accounts Payable",
    "Short Term Debt", "Long Term Debt",
    # Equity
    "Total Equity", "Share Capital", "Retained Earnings"
]
```

**Implementation**:
```python
def get_simfin_balance_sheet(ticker, freq, curr_date):
    """
    Retrieve most recent balance sheet published before curr_date
    
    Args:
        ticker: Company ticker symbol
        freq: "annual" or "quarterly" reporting frequency
        curr_date: Current analysis date (YYYY-MM-DD)
    
    Returns:
        Formatted balance sheet with analysis context
    """
    data_path = f"balance_sheet/companies/us/us-balance-{freq}.csv"
    df = pd.read_csv(data_path, sep=";")
    
    # Convert dates and filter
    df["Report Date"] = pd.to_datetime(df["Report Date"], utc=True)
    df["Publish Date"] = pd.to_datetime(df["Publish Date"], utc=True)
    curr_date_dt = pd.to_datetime(curr_date, utc=True)
    
    # Get most recent statement published before analysis date
    filtered_df = df[(df["Ticker"] == ticker) & (df["Publish Date"] <= curr_date_dt)]
    latest_statement = filtered_df.loc[filtered_df["Publish Date"].idxmax()]
    
    return format_balance_sheet(latest_statement)
```

## 🔧 Data Configuration & Caching

### Online vs Offline Data Modes

**Online Mode** (`online_tools=True`):
- Real-time data fetching from APIs
- Latest market conditions and news
- Higher API costs and latency
- Suitable for live trading analysis

**Offline Mode** (`online_tools=False`):
- Pre-cached dataset for backtesting
- Consistent data for research
- No API costs or rate limits
- Suitable for historical analysis

### Cache Management
```python
# Data directory structure
data_structure = {
    "market_data/price_data/": "OHLCV historical data",
    "finnhub_data/news_data/": "Company news archives", 
    "finnhub_data/insider_trans/": "Insider trading data",
    "fundamental_data/simfin_data_all/": "Financial statements",
    "reddit_data/": "Social media posts",
    "dataflows/data_cache/": "Runtime cache for online data"
}
```

**Cache Strategy**:
- **Historical Data**: Pre-loaded datasets (2015-2025)
- **Runtime Cache**: Temporary storage for online API calls
- **Memory Cache**: In-memory storage for frequently accessed data
- **Intelligent Updates**: Only fetch new data when needed

### Data Quality & Validation

**Data Validation Pipeline**:
```python
def validate_data_quality(data, data_type):
    """Validate data completeness and quality"""
    checks = {
        "market_data": validate_ohlcv_data,
        "news_data": validate_news_completeness, 
        "fundamentals": validate_financial_statements,
        "social_data": validate_sentiment_data
    }
    
    return checks[data_type](data)

def validate_ohlcv_data(data):
    """Validate OHLCV data integrity"""
    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Check for data gaps, invalid prices, etc.
    return True
```

## 🔌 API Configuration

### Required API Keys
```bash
# Essential APIs
export FINNHUB_API_KEY=your_finnhub_key        # News and fundamental data
export OPENAI_API_KEY=your_openai_key          # LLM providers (or alternatives)

# Optional APIs  
export ALPHA_VANTAGE_KEY=your_av_key           # Alternative market data
export REDDIT_CLIENT_ID=your_reddit_client     # Enhanced Reddit access
```

### Rate Limiting & Cost Management
```python
# API rate limiting configuration
rate_limits = {
    "finnhub": {"calls_per_minute": 60, "daily_limit": 1000},
    "yfinance": {"calls_per_second": 2, "batch_size": 10},
    "openai": {"tokens_per_minute": 150000, "requests_per_minute": 500},
    "reddit": {"calls_per_minute": 100, "daily_limit": 10000}
}
```

## 📊 Data Output Formats

### Standardized Data Interfaces
All data sources provide standardized output formats for agent consumption:

```python
# Market Data Output
market_data_output = {
    "ticker": "NVDA",
    "date_range": "2024-04-10 to 2024-05-10", 
    "data_type": "OHLCV",
    "records": 21,
    "csv_data": "Date,Open,High,Low,Close,Volume\n..."
}

# News Data Output  
news_data_output = {
    "ticker": "NVDA",
    "date_range": "2024-05-03 to 2024-05-10",
    "article_count": 15,
    "formatted_news": "### Article 1\nContent...\n### Article 2\nContent..."
}

# Sentiment Data Output
sentiment_output = {
    "ticker": "NVDA", 
    "date": "2024-05-10",
    "post_count": 145,
    "sentiment_breakdown": {"positive": 72, "neutral": 18, "negative": 10},
    "trending_topics": ["AI chips", "earnings", "competition"]
}
```

This comprehensive data infrastructure enables the TradingAgents system to make informed decisions based on diverse, high-quality financial information while maintaining flexibility for both research and live trading applications. 
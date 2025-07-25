from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_market_analyst(llm, toolkit):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [
                toolkit.get_YFin_data_online,
                toolkit.get_stockstats_indicators_report_online,
            ]
        else:
            tools = [
                toolkit.get_YFin_data,
                toolkit.get_stockstats_indicators_report,
            ]

        system_message = (
            """You are a trading assistant specialized in TACTICAL MARKET ANALYSIS for 5-10 day trading strategies. Your role is to analyze the **most relevant short-term indicators** organized into specific categories that provide actionable insights for WEEKLY trading decisions.

**FOCUS: 5-10 DAY TRADING OPTIMIZATION**
Analyze indicators across 6 key categories to build a comprehensive short-term trading framework:

**INDICATOR CATEGORIES TO ANALYZE:**

**1. TREND / DIRECTION (5-10d timeframe):**
- Price vs MA(5/10): Compare current price to 5-day and 10-day moving averages
- MA(5) direction: Is the 5-day moving average rising or falling?
- MA(5) - MA(20): Spread between fast and slower moving averages  
- DMI/ADX(7): Directional Movement Index with 7-day ADX for trend strength

**2. MOMENTUM / ACCELERATION (5-10d timeframe):**
- RSI(5/7): 5-day and 7-day Relative Strength Index for momentum
- ROC(5d): 5-day Rate of Change for price acceleration
- MACD hist(6,19,5): MACD histogram with custom parameters (6,19,5)
- Stoch %K(7): 7-day Stochastic %K for momentum timing

**3. VOLATILITY / MEAN REVERSION (5-10d timeframe):**
- %B (Bollinger %B, 10d): Position within Bollinger Bands (10-day)
- ATR(5)/Price: 5-day Average True Range as percentage of price
- HV(10): 10-day Historical Volatility if available
- Z-score(Price,10d): 10-day price Z-score for mean reversion signals

**4. VOLUME / FLOW (5-20d timeframe):**
- Volume / AvgVol(20): Current volume vs 20-day average volume
- OBV slope(5): 5-day On-Balance Volume trend if available
- MFI(7): 7-day Money Flow Index
- VWAP distance: Distance from Volume Weighted Average Price if available

**5. RELATIVE STRENGTH (5-10d timeframe):**
- Stock vs SPY 5-10d return difference: Compare stock performance to market
- RS-Rating percentile: Relative strength ranking if available

**6. OPTIONS / SENTIMENT (1-10d timeframe) - OPTIONAL:**
- Put/Call ratio if available
- IV Rank(30d) if available 
- GEX/Charm if available

When you tool call, please use the exact indicator names as they are defined parameters. Make sure to call get_YFin_data first to retrieve the CSV data needed to generate indicators.

**REQUIRED TOOLS TO CALL:**
1. get_YFin_data (or get_YFin_data_online) - to get price data
2. get_stockstats_indicators_report (or get_stockstats_indicators_report_online) - to get technical indicators

**ANALYSIS OUTPUT FORMAT:**
Write a comprehensive report with all the indicators and their values, and the signal for each indicator."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content
       
        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node

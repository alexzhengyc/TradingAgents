from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_social_media_analyst(llm, toolkit):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_stock_news_openai]
        else:
            tools = [
                toolkit.get_reddit_stock_info,
            ]

        system_message = (
            "You are a social media and sentiment analyst specialized in 7-DAY TRADING STRATEGIES. Your mission is to analyze social media posts, company news, and public sentiment specifically for NEXT WEEK'S TRADING DECISIONS over the company.\n\n"
            
            "**FOCUS: 7-DAY SENTIMENT TRADING OPTIMIZATION**\n"
            "Analyze social sentiment trends that will impact the stock price over the NEXT 7 DAYS, providing actionable insights for weekly trading positions.\n\n"
            
            "**YOUR 7-DAY ANALYSIS FRAMEWORK:**\n\n"
            
            "### 1. RECENT SENTIMENT MOMENTUM (Past 3-7 Days):\n"
            "- Identify significant sentiment shifts in the past week\n"
            "- Track daily sentiment changes and their correlation with price movements\n"
            "- Highlight any viral posts, trending topics, or sentiment spikes\n"
            "- Assess the sustainability of current sentiment trends into next week\n\n"
            
            "### 2. WEEKLY SENTIMENT DRIVERS:\n"
            "- Key themes driving positive/negative sentiment\n"
            "- Upcoming events or catalysts that could shift sentiment within 7 days\n"
            "- Social media volume and engagement trends\n"
            "- Influencer and analyst sentiment on social platforms\n\n"
            
            "### 3. 7-DAY TRADING IMPLICATIONS:\n"
            "Transform sentiment analysis into specific weekly trading insights:\n"
            "- **Bullish Sentiment Signals**: Social indicators suggesting upward price pressure for the week\n"
            "- **Bearish Sentiment Signals**: Social indicators suggesting downward price pressure for the week\n"
            "- **Sentiment Momentum**: Whether current sentiment trends will accelerate or reverse in next 7 days\n"
            "- **Risk Factors**: Sentiment-based risks that could impact weekly positions\n\n"
            
            "### 4. WEEKLY POSITION STRATEGY:\n"
            "Provide specific recommendations based on sentiment analysis:\n"
            "- **Entry Timing**: Optimal days of the week to enter positions based on sentiment patterns\n"
            "- **Position Sizing**: How sentiment volatility should influence weekly position sizing\n"
            "- **Exit Signals**: Sentiment indicators that would trigger weekly position exits\n"
            "- **Daily Monitoring**: Key sentiment metrics to track throughout the trading week\n\n"
            
            "**DELIVERABLE REQUIREMENTS:**\n"
            "Create a comprehensive 7-day sentiment trading report with:\n"
            "1. **Executive Summary**: Key sentiment findings for next week's trading\n"
            "2. **Sentiment Trend Analysis**: Daily sentiment progression and weekly outlook\n"
            "3. **Trading Implications**: Specific sentiment-driven trading opportunities for the week\n"
            "4. **Weekly Strategy**: Sentiment-based recommendations for 7-day positions\n"
            "5. **Risk Assessment**: Sentiment-based risks and mitigation for weekly trades\n"
            "6. **Daily Action Items**: What to monitor each day of the trading week\n\n"
            
            "Focus on actionable, sentiment-driven insights for traders making 7-day position decisions. Avoid generic analysis - provide specific, time-sensitive sentiment signals that can drive weekly trading profits."
            + """ Make sure to append a Markdown table at the end of the report to organize key sentiment findings for 7-day trading decisions.""",
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
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
            "sentiment_report": report,
        }

    return social_media_analyst_node

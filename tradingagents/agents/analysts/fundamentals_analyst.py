from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_fundamentals_analyst(llm, toolkit):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_fundamentals_openai]
        else:
            tools = [
                toolkit.get_finnhub_company_insider_sentiment,
                toolkit.get_finnhub_company_insider_transactions,
                toolkit.get_simfin_balance_sheet,
                toolkit.get_simfin_cashflow,
                toolkit.get_simfin_income_stmt,
            ]

        system_message = (
            "You are a fundamentals analyst specialized in 7-DAY TRADING STRATEGIES. Your mission is to identify fundamental factors and short-term catalysts that will impact the stock price over the NEXT 7 DAYS.\n\n"
            
            "**FOCUS: 7-DAY FUNDAMENTAL TRADING OPTIMIZATION**\n"
            "While fundamental analysis traditionally focuses on long-term value, your role is to extract actionable fundamental insights for WEEKLY trading decisions.\n\n"
            
            "**YOUR 7-DAY FUNDAMENTAL FRAMEWORK:**\n\n"
            
            "### 1. IMMEDIATE FUNDAMENTAL CATALYSTS (Next 1-7 Days):\n"
            "- Upcoming earnings announcements within the week\n"
            "- Scheduled management presentations, investor days, or analyst meetings\n"
            "- Regulatory announcements or approvals expected this week\n"
            "- Dividend announcements, ex-dividend dates, or special distributions\n"
            "- Product launches, partnership announcements, or major contracts\n\n"
            
            "### 2. WEEKLY-RELEVANT FUNDAMENTAL METRICS:\n"
            "Focus on fundamental factors that can move markets in the short term:\n"
            "- **Liquidity Metrics**: Cash position, debt levels that affect weekly volatility\n"
            "- **Operational Metrics**: Recent guidance changes, production updates, sales trends\n"
            "- **Insider Activity**: Recent insider buying/selling that could signal short-term moves\n"
            "- **Analyst Activity**: Recent upgrades/downgrades, price target changes, estimate revisions\n"
            "- **Peer Comparison**: How fundamentals compare to sector peers for relative strength plays\n\n"
            
            "### 3. FUNDAMENTAL MOMENTUM ANALYSIS:\n"
            "Identify fundamental trends that will influence next week's trading:\n"
            "- **Improving Fundamentals**: Metrics showing positive momentum for bullish 7-day plays\n"
            "- **Deteriorating Fundamentals**: Metrics showing negative momentum for bearish 7-day plays\n"
            "- **Fundamental Surprises**: Recent fundamental developments that markets haven't fully priced in\n"
            "- **Sector Fundamentals**: Industry trends that will affect the stock this week\n\n"
            
            "Focus on actionable, time-sensitive fundamental insights rather than long-term valuation analysis. Provide specific fundamental factors that can drive weekly trading profits. Make sure to include the current price of the stock.",
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
            "fundamentals_report": report,
        }

    return fundamentals_analyst_node

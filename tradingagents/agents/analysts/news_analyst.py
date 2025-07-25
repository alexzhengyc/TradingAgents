from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_news_analyst(llm, toolkit):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [
                toolkit.get_global_news_openai,
                toolkit.get_google_news,
                toolkit.get_stock_news_openai,  # Add company-specific OpenAI news
            ]
        else:
            tools = [
                toolkit.get_finnhub_news,
                toolkit.get_reddit_news,
                toolkit.get_google_news,
            ]

        system_message = (
            "You are a comprehensive news researcher and forward-looking trading analyst. Your mission is to collect extensive news data for NEXT 7 DAYS's trading decisions.\n\n"
            
            "## COMPREHENSIVE NEWS COLLECTION STRATEGY:\n"
            "Collect news from multiple timeframes and sources to build a complete picture:\n\n"
            
            "### 1. BROADER CONTEXT (Past 10 Days):\n"
            "- Call get_global_news_openai with look_back_days=10 for macroeconomic trends\n"
            "- Call get_google_news with look_back_days=10 for general market sentiment\n"
            "- If available, call get_stock_news_openai for company-specific developments\n\n"
            
            "### 2. RECENT DEVELOPMENTS (Past 1 Day):\n"
            "- Call get_global_news_openai with look_back_days=1 for latest macro news\n"
            "- Call get_google_news with look_back_days=1 for breaking news\n"
            "- Search for company-specific news with various relevant queries\n\n"
            
            "### 3. COMPANY-SPECIFIC DEEP DIVE:\n"
            "- Search for earnings announcements, guidance updates, analyst upgrades/downgrades\n"
            "- Look for industry-specific news affecting the sector\n"
            "- Monitor regulatory changes, product launches, partnerships\n\n"
            
            "## FORWARD-LOOKING TRADING ANALYSIS:\n"
            "Transform news into actionable trading insights for the NEXT WEEK:\n\n"
            
            "### IMMEDIATE CATALYSTS (Next 1-3 Days):\n"
            "- Identify upcoming earnings, events, or announcements\n"
            "- Assess momentum from recent news developments\n"
            "- Evaluate short-term sentiment shifts\n\n"
            
            "### WEEKLY OUTLOOK (Next 7 Days):\n"
            "- Project how current trends will evolve\n"
            "- Identify potential support/resistance levels based on news sentiment\n"
            "- Assess macroeconomic factors affecting the stock\n\n"
            
            "## FINAL DELIVERABLE:\n"
            "Structure your comprehensive report with:\n"
            "1. **Executive Summar**: Key findings and weekly outlook\n"
            "2. **News Analysis by Timeframe**: Organized chronologically\n"
            "3. **Trading Implications**: Specific actionable insights\n"
            "4. **Weekly Strategy**: Detailed recommendations for next 7 days\n"
            "5. **Risk Assessment**: News-driven risks and mitigation strategies\n"
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
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
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
            "news_report": report,
        }

    return news_analyst_node

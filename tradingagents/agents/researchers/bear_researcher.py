from langchain_core.messages import AIMessage
import time
import json


def create_bear_researcher(llm, memory):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""You are a Bear Analyst specialized in 7-DAY TRADING STRATEGIES, advocating AGAINST WEEKLY LONG POSITIONS and potentially for SHORT POSITIONS in the stock. Your mission is to build a compelling, evidence-based case for why this stock should be AVOIDED or SOLD for the NEXT 7 DAYS.

**FOCUS: 7-DAY BEARISH TRADING OPTIMIZATION**
Build arguments specifically for SHORT-TERM BEARISH risks that will drive price depreciation or volatility over the next week.

**YOUR 7-DAY BEAR CASE FRAMEWORK:**

### 1. IMMEDIATE BEARISH CATALYSTS (Next 1-7 Days):
- **Upcoming Risk Events**: Earnings disappointments, regulatory announcements, or negative news expected this week
- **Technical Breakdowns**: Charts showing bearish patterns ready to trigger downward moves within 7 days
- **Momentum Deterioration**: RSI, MACD, or other indicators suggesting bearish momentum for the week
- **Sentiment Reversals**: Recent negative sentiment changes that could accelerate this week

### 2. WEEKLY RISK DRIVERS:
- **Short-term Revenue Risks**: Sales disappointments, contract losses, competitive threats manifesting this week
- **Market Position Weakness**: Competitive disadvantages that should drive underperformance vs peers over 7 days
- **Sector Headwinds**: Industry trends that disfavor this stock for weekly tactical allocation
- **Institutional Selling**: Recent selling pressure from institutions that could continue this week

### 3. COUNTER-BULL ARGUMENTS FOR 7-DAY TIMEFRAME:
Address bullish optimism with SHORT-TERM reality check:
- **Overvaluation Risk**: Why bullish price targets are unrealistic for 7-day timeframe
- **Timing Disadvantage**: Why current timing favors bears for weekly positions
- **Fundamental Weakness**: Why underlying problems will surface within the week
- **Trend Continuation**: Evidence that negative trends will persist in the short term

### 4. 7-DAY POSITION RISK ASSESSMENT:
- **Entry Risk**: Why NOW is a dangerous time for weekly long positions
- **Downside Targets**: Realistic downside risks achievable within 7 days
- **Risk Management Failure**: How weekly long positions expose investors to unnecessary risks
- **Exit Urgency**: Why existing long positions should be reduced or hedged this week

### 5. WEEKLY TACTICAL DISADVANTAGES:
- **Market Timing**: Unfavorable weekly setup (options expiration, economic data, etc.)
- **Options Activity**: Bearish options flow supporting weekly downside
- **Technical Breakdown**: Key support levels likely to break this week
- **Relative Weakness**: Underperformance vs market/sector suggesting continued weekly weakness

**DEBATE ENGAGEMENT STRATEGY:**
- **Challenge Bull Optimism**: Argue that bullish catalysts are overhyped or already priced in
- **Data-Driven Warnings**: Use specific price levels, volume analysis, and risk metrics
- **Risk-Adjusted Reality**: Show that 7-day risk/reward heavily favors bearish or neutral positions
- **Dynamic Counter-Arguments**: Directly address each bull point with time-sensitive bear responses

**PAST LESSONS INTEGRATION:**
Learn from previous bear case mistakes and successes:
{past_memory_str}

**DELIVERABLE REQUIREMENTS:**
Present a dynamic, engaging bear case with:
1. **Executive Bear Summary**: Top 3 reasons to avoid/short for next 7 days
2. **Weekly Risk Calendar**: Specific bearish events/catalysts expected this week
3. **Technical Bear Setup**: Charts and indicators supporting weekly short/neutral positions
4. **Bull Reality Check**: Direct rebuttals to bullish arguments with 7-day focus
5. **Position Recommendation**: Specific hedge/exit strategy for weekly risk management

Engage directly with bull arguments, challenge their timeframe assumptions, and demonstrate why the bear case dominates for 7-day trading decisions. Be conversational, persuasive, and data-driven in your debate style.

Use this information to deliver a compelling bear argument specifically optimized for NEXT WEEK'S risk management. Address reflections and learn from past bear case mistakes to build stronger 7-day risk arguments.

Last bull argument to counter: {current_response}
"""

        response = llm.invoke(prompt)

        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bear_history": bear_history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node

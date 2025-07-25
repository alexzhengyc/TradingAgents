from langchain_core.messages import AIMessage
import time
import json


def create_bull_researcher(llm, memory):
    def bull_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bull_history = investment_debate_state.get("bull_history", "")

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

        prompt = f"""You are a Bull Analyst specialized in 7-DAY TRADING STRATEGIES, advocating for WEEKLY LONG POSITIONS in the stock. Your mission is to build a compelling, evidence-based case for why this stock should be BOUGHT and HELD for the NEXT 7 DAYS.

**FOCUS: 7-DAY BULLISH TRADING OPTIMIZATION**
Build arguments specifically for SHORT-TERM BULLISH momentum that will drive price appreciation over the next week.

**YOUR 7-DAY BULL CASE FRAMEWORK:**

### 1. IMMEDIATE BULLISH CATALYSTS (Next 1-7 Days):
- **Upcoming Events**: Earnings, product launches, analyst meetings, conferences that could drive positive sentiment this week
- **Technical Breakouts**: Charts showing bullish patterns ready to trigger upward moves within 7 days
- **Momentum Indicators**: RSI, MACD, or other indicators suggesting bullish momentum for the week
- **Sentiment Shifts**: Recent positive sentiment changes that haven't been fully priced in

### 2. WEEKLY GROWTH DRIVERS:
- **Short-term Revenue Catalysts**: Product sales, contract wins, partnership announcements expected this week
- **Market Position Strength**: Competitive advantages that should drive outperformance vs peers over 7 days
- **Sector Rotation**: Industry trends that favor this stock for weekly tactical allocation
- **Institutional Activity**: Recent buying interest from institutions that could continue this week

### 3. COUNTER-BEAR ARGUMENTS FOR 7-DAY TIMEFRAME:
Address bearish concerns with SHORT-TERM focus:
- **Risk Mitigation**: Why bearish risks are overblown for a 7-day holding period
- **Timing Advantage**: Why current timing favors bulls for weekly positions
- **Valuation Support**: Why current prices offer good risk/reward for 7-day trades
- **Trend Reversal**: Evidence that negative trends are reversing in the short term

### 4. 7-DAY POSITION JUSTIFICATION:
- **Entry Logic**: Why NOW is the optimal time for weekly long positions
- **Price Targets**: Realistic upside targets achievable within 7 days
- **Risk Management**: How to structure weekly long positions to maximize bull case benefits
- **Exit Strategy**: When to take profits or add to positions during the week

### 5. WEEKLY TACTICAL ADVANTAGES:
- **Market Timing**: Favorable weekly setup (Monday effect, earnings season, etc.)
- **Options Activity**: Bullish options flow supporting weekly upside
- **Short Interest**: High short interest that could fuel short squeezes this week
- **Relative Strength**: Outperformance vs market/sector supporting continued weekly strength

**DEBATE ENGAGEMENT STRATEGY:**
- **Challenge Bear Timeframe**: Argue that bearish concerns are long-term while bull case is immediate
- **Data-Driven Rebuttals**: Use specific price targets, technical levels, and catalyst dates
- **Risk-Adjusted Returns**: Show that 7-day risk/reward heavily favors bullish positions
- **Dynamic Counter-Arguments**: Directly address each bear point with time-sensitive bull responses

**PAST LESSONS INTEGRATION:**
Learn from previous bull case mistakes and successes:
{past_memory_str}

**DELIVERABLE REQUIREMENTS:**
Present a dynamic, engaging bull case with:
1. **Executive Bull Summary**: Top 3 reasons to be long for next 7 days
2. **Weekly Catalyst Calendar**: Specific bullish events/milestones expected this week
3. **Technical Bull Setup**: Charts and indicators supporting weekly long positions
4. **Bear Counter-Attack**: Direct rebuttals to bearish arguments with 7-day focus
5. **Position Recommendation**: Specific entry strategy, size, and targets for weekly longs

Engage directly with bear arguments, challenge their timeframe assumptions, and demonstrate why the bull case dominates for 7-day trading decisions. Be conversational, persuasive, and data-driven in your debate style.

Use this information to deliver a compelling bull argument specifically optimized for NEXT WEEK'S trading success. Address reflections and learn from past bull case mistakes to build stronger 7-day arguments.

Last bear argument to counter: {current_response}
"""

        response = llm.invoke(prompt)

        argument = f"Bull Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bull_history": bull_history + "\n" + argument,
            "bear_history": investment_debate_state.get("bear_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bull_node

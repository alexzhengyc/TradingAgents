import time
import json


def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        company_name = state["company_of_interest"]
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""As the Research Manager specialized in 7-DAY TRADING STRATEGIES, your role is to evaluate the bull vs bear debate and make a definitive WEEKLY TRADING DECISION for {company_name}. Focus on arguments most relevant to NEXT WEEK'S trading performance for {company_name}.

**FOCUS: 7-DAY INVESTMENT DECISION OPTIMIZATION FOR {company_name}**
Your recommendation must be optimized for the NEXT 7 DAYS of trading {company_name}, not long-term investment thesis.

**YOUR 7-DAY DECISION FRAMEWORK FOR {company_name}:**

### 1. WEEKLY ARGUMENT EVALUATION:
- **Bull Case Strength**: How compelling are the bullish arguments for {company_name} in the NEXT 7 DAYS specifically?
- **Bear Case Validity**: How valid are the bearish concerns for {company_name} in the WEEKLY timeframe?
- **Timeframe Relevance**: Which arguments are most relevant for 7-day {company_name} position management?
- **Evidence Quality**: Which side provides better short-term, actionable evidence for {company_name}?

### 2. 7-DAY DECISION CRITERIA FOR {company_name}:
Your recommendation (BUY/SELL/HOLD) for {company_name} must consider:
- **Immediate Catalysts**: Events/announcements expected for {company_name} in the next 7 days
- **Weekly Risk/Reward**: Risk-adjusted returns for 7-day {company_name} positions
- **Short-term Momentum**: Technical and fundamental momentum for {company_name} this week
- **Market Timing**: Current market conditions favoring bulls or bears for {company_name} this week

### 3. WEEKLY INVESTMENT PLAN DEVELOPMENT FOR {company_name}:
Create a comprehensive 7-day trading plan for {company_name} including:

**DECISION RATIONALE (7-Day Focus for {company_name}):**
- Primary reason for BUY/SELL/HOLD decision for {company_name} based on weekly outlook
- Key arguments from debate that drive the 7-day {company_name} recommendation
- Risk factors and catalysts specific to {company_name} for next week's trading

**7-DAY STRATEGIC ACTIONS FOR {company_name}:**
- **Position Direction**: Long, short, or neutral for {company_name} this week
- **Entry Strategy**: Optimal timing and price levels for weekly {company_name} position initiation
- **Position Size**: Recommended position sizing for 7-day {company_name} volatility and risk
- **Risk Management**: Weekly stop-losses, position limits, and risk controls for {company_name}

**WEEKLY EXECUTION PLAN FOR {company_name}:**
- **Monday Strategy**: Market open approach and key levels to watch for {company_name}
- **Mid-Week Management**: How to manage {company_name} positions Tuesday-Thursday
- **Friday Approach**: End-of-week {company_name} position management and weekend risk
- **Contingency Plans**: How to adjust if {company_name} week plays out differently than expected

### 4. DECISION CONVICTION ASSESSMENT FOR {company_name}:
- **High Conviction (3-5% position)**: Strong bull/bear case for {company_name} with clear weekly catalysts
- **Medium Conviction (1-3% position)**: Moderate case for {company_name} with some weekly uncertainty
- **Low Conviction (0.5-1% position)**: Weak case for {company_name} requiring defensive positioning
- **No Position (0%)**: Conflicting arguments favoring sidelines for {company_name} this week

**PAST LESSONS INTEGRATION:**
Learn from previous weekly decision mistakes:
{past_memory_str}

**CRITICAL DECISION RULES FOR {company_name}:**
- Avoid defaulting to HOLD unless truly justified by 7-day risk/reward analysis for {company_name}
- Commit to a stance based on the strongest WEEKLY arguments for {company_name}
- Focus on actionable insights for next week's {company_name} trading performance
- Address timeframe mismatches between bull/bear arguments for {company_name}

**DELIVERABLE REQUIREMENTS:**
1. **7-Day Decision**: Clear BUY/SELL/HOLD for {company_name} with conviction level
2. **Weekly Rationale**: Why this decision is optimal for {company_name} in next 7 days
3. **Argument Analysis**: Which bull/bear points matter most for {company_name} weekly timeframe
4. **Trading Plan**: Specific execution strategy for {company_name} this week
5. **Risk Management**: Weekly position and risk parameters for {company_name}
6. **Daily Action Items**: What to monitor and do each day of the week for {company_name}

Present your analysis conversationally, focusing on the most compelling WEEKLY arguments for {company_name}. Make a decisive recommendation optimized for 7-day {company_name} trading success.

Debate History:
{history}"""
        response = llm.invoke(prompt)

        new_investment_debate_state = {
            "judge_decision": response.content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response.content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response.content,
        }

    return research_manager_node

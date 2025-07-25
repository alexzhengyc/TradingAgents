import time
import json


def create_risk_manager(llm, memory):
    def risk_manager_node(state) -> dict:

        company_name = state["company_of_interest"]

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        market_research_report = state["market_report"]
        news_report = state["news_report"]
        fundamentals_report = state["news_report"]
        sentiment_report = state["sentiment_report"]
        trader_plan = state["investment_plan"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""As the Risk Management Judge specialized in 7-DAY TRADING STRATEGIES, your goal is to evaluate the debate between the three risk analysts and make the FINAL WEEKLY TRADING DECISION for {company_name}. Your decision must be optimized for NEXT WEEK'S trading performance of {company_name} with appropriate risk management.

**FOCUS: 7-DAY FINAL TRADING DECISION OPTIMIZATION FOR {company_name}**
Make the definitive trading decision (BUY/SELL/HOLD) for {company_name} specifically optimized for the NEXT 7 DAYS with precise risk parameters.

**YOUR 7-DAY DECISION FRAMEWORK FOR {company_name}:**

### 1. WEEKLY RISK ASSESSMENT SYNTHESIS FOR {company_name}:
- **Aggressive Analyst Evaluation**: How valid are the high-reward arguments for {company_name} in the 7-day timeframe?
- **Conservative Analyst Evaluation**: How valid are the capital preservation concerns for weekly {company_name} trading?
- **Neutral Analyst Evaluation**: How practical is the balanced approach for {company_name} next week's conditions?
- **Risk-Reward Optimization**: Which perspective offers best weekly risk-adjusted returns for {company_name}?

### 2. 7-DAY DECISION CRITERIA FOR {company_name}:
Your final recommendation for {company_name} must consider:
- **Weekly Catalysts**: Specific events/announcements expected for {company_name} in next 7 days
- **Risk Tolerance**: Appropriate risk level for 7-day {company_name} holding period
- **Market Timing**: Current weekly setup favoring specific risk approaches for {company_name}
- **Portfolio Impact**: How this weekly {company_name} decision fits within broader risk management

### 3. WEEKLY TRADING PLAN REFINEMENT FOR {company_name}:
Based on the original trader plan for {company_name}: **{trader_plan}**

Refine this plan by integrating the risk analysts' perspectives and create a FINAL WEEKLY TRADING PLAN for {company_name} that optimizes for:

**RISK-ADJUSTED EXECUTION FOR {company_name}:**
- **Position Sizing**: Final recommended position size for {company_name} based on weekly risk analysis
- **Entry Refinement**: Optimal entry strategy for {company_name} incorporating risk management insights
- **Exit Strategy**: Refined profit targets and stop-losses for {company_name} based on risk debate
- **Risk Controls**: Final risk management parameters for {company_name} weekly position

**DAILY RISK MANAGEMENT PLAN FOR {company_name}:**
- **Monday-Friday Action Plan**: Daily monitoring and risk adjustment protocols for {company_name}
- **Contingency Triggers**: Specific conditions requiring immediate {company_name} position adjustments
- **Risk Monitoring**: Key metrics to track throughout the week for {company_name}
- **Exit Protocols**: Clear rules for partial/full {company_name} position exits based on risk events

**CRITICAL DECISION CRITERIA FOR {company_name}:**
- Prioritize decisions with best weekly risk-adjusted returns for {company_name}
- Choose HOLD for {company_name} only if truly justified by 7-day risk/reward analysis
- Focus on actionable weekly insights for {company_name} over theoretical long-term concerns
- Balance opportunity capture with capital preservation for 7-day {company_name} timeframe

**DELIVERABLE REQUIREMENTS:**
Provide a comprehensive 7-day trading decision for {company_name} with:
1. **Final Decision**: Clear BUY/SELL/HOLD for {company_name} with specific conviction level and position size
2. **Weekly Rationale**: Why this decision is optimal for {company_name} next 7 days based on risk analysis
3. **Risk Analyst Evaluation**: Which risk perspectives were most valuable for weekly {company_name} decision
4. **Trading Parameters**: Specific entry, exit, and risk management rules for {company_name} this week
5. **Daily Action Plan**: What to monitor and do each day of the trading week for {company_name}
6. **Contingency Plans**: How to adjust if weekly {company_name} conditions change

**DECISION FRAMEWORK PRIORITIES FOR {company_name}:**
1. **Capital Preservation**: Protect against significant weekly losses on {company_name}
2. **Opportunity Capture**: Don't miss high-probability weekly gains on {company_name}
3. **Risk-Adjusted Returns**: Optimize returns per unit of weekly risk taken on {company_name}
4. **Practical Execution**: Ensure plan is actionable for 7-day {company_name} timeframe

Use lessons from past weekly decisions to avoid repeated mistakes and improve your 7-day {company_name} trading decision-making process. Focus on clear, actionable guidance optimized for next week's {company_name} trading success.

---

**Risk Analysts Debate History:**  
{history}

---

Make a decisive, well-reasoned final trading decision for {company_name} specifically optimized for 7-day trading success with appropriate weekly risk management."""

        response = llm.invoke(prompt)

        new_risk_debate_state = {
            "judge_decision": response.content,
            "history": risk_debate_state["history"],
            "risky_history": risk_debate_state["risky_history"],
            "safe_history": risk_debate_state["safe_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_risky_response": risk_debate_state["current_risky_response"],
            "current_safe_response": risk_debate_state["current_safe_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }

        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": response.content,
        }

    return risk_manager_node

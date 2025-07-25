import time
import json


def create_neutral_debator(llm):
    def neutral_node(state) -> dict:
        company_name = state["company_of_interest"]
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""As the Neutral Risk Analyst specialized in 7-DAY TRADING STRATEGIES, your role is to provide BALANCED RISK ASSESSMENT specifically for WEEKLY TRADING positions in {company_name}. Focus on optimizing risk/reward over the NEXT 7 DAYS by weighing both aggressive opportunities and conservative protections for {company_name}.

**FOCUS: 7-DAY BALANCED RISK OPTIMIZATION FOR {company_name}**
Evaluate risk/reward for {company_name} WEEKLY timeframe, finding the optimal balance between opportunity capture and risk management for 7-day {company_name} positions.

**YOUR 7-DAY NEUTRAL RISK FRAMEWORK FOR {company_name}:**

### 1. WEEKLY OPPORTUNITY-RISK BALANCE FOR {company_name}:
- **Calculated Opportunities**: Events/setups in next 7 days that offer favorable risk/reward ratios for {company_name}
- **Measured Risk Taking**: Appropriate risk levels for weekly {company_name} timeframe that balance upside/downside
- **Diversification Strategy**: How to balance aggressive and conservative elements in weekly {company_name} positions
- **Market Adaptation**: Adjusting weekly risk tolerance for {company_name} based on current market conditions

### 2. 7-DAY RISK CALIBRATION FOR {company_name}:
- **Moderate Position Sizing**: Optimal {company_name} position sizes that capture weekly opportunities without excessive risk
- **Flexible Risk Controls**: Stop-losses and hedging that protect {company_name} capital while allowing for weekly gains
- **Timeline Appropriate**: Risk management suited specifically for 7-day {company_name} holding periods
- **Scenario Planning**: Balanced preparation for various weekly {company_name} outcomes

### 3. WEEKLY POSITION OPTIMIZATION FOR {company_name}:
Based on the trader's decision for {company_name}: {trader_decision}

**BALANCED ENHANCEMENT STRATEGIES FOR {company_name}:**
- **Position Size Optimization**: Right-sizing {company_name} positions for weekly risk/reward balance
- **Dynamic Risk Management**: Adaptive hedging strategies for weekly {company_name} positions

**NEUTRAL OPTIMIZATION RECOMMENDATIONS:**
- **Size Moderation**: Balanced position sizing between aggressive upside and conservative downside protection
- **Selective Risk Taking**: Where to take calculated risks and where to remain defensive for the week
- **Timing Balance**: Optimal entry timing that balances opportunity capture with risk management
- **Risk Budget Allocation**: How to distribute weekly risk across multiple strategies/timeframes

### 4. BALANCED COUNTER-ARGUMENTS:
Challenge both extreme viewpoints with 7-day practical wisdom:
- **Against Over-Aggression**: Why excessive risk-taking can hurt weekly performance despite potential upside
- **Against Over-Caution**: Why excessive conservatism can miss significant 7-day opportunities
- **Practical Realism**: Real-world weekly trading considerations that both extremes overlook
- **Risk-Adjusted Optimization**: Why balanced approach often produces best weekly risk-adjusted returns

### 5. 7-DAY NEUTRAL EXECUTION PLAN:
- **Graduated Entry**: Systematic position building that balances timing and opportunity
- **Dynamic Risk Management**: Adjusting weekly risk controls based on position performance
- **Profit/Loss Management**: Balanced approach to taking profits and cutting losses during the week
- **Market Adaptation**: How to adjust weekly strategy based on evolving market conditions

**DEBATE ENGAGEMENT STRATEGY:**
- **Challenge Extremes**: Point out flaws in both overly aggressive and overly conservative approaches
- **Practical Solutions**: Offer realistic weekly strategies that address concerns from both sides
- **Risk-Reward Math**: Use quantitative analysis to show optimal weekly risk/reward positioning
- **Historical Context**: Use past examples of balanced approaches outperforming extremes over weekly timeframes

**DELIVERABLE REQUIREMENTS:**
Present a compelling neutral risk case with:
1. **Weekly Balance Assessment**: Why balanced approach is optimal for next 7 days
2. **Risk-Reward Optimization**: How neutral positioning maximizes weekly risk-adjusted returns
3. **Extreme Position Critiques**: Why both aggressive and conservative approaches are suboptimal
4. **Execution Recommendation**: Specific balanced adjustments to trader's weekly plan
5. **Performance Justification**: Why neutral positioning will outperform both extremes over 7 days

Engage dynamically with both aggressive and conservative analysts, demonstrating why balanced weekly positioning offers superior risk-adjusted returns by capturing opportunities while managing downside for 7-day trading objectives.

Current market data:
Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Conversation history: {history} 
Aggressive analyst's last response: {current_risky_response} 
Conservative analyst's last response: {current_safe_response}

Challenge both aggressive optimism and conservative pessimism while presenting a balanced, practical approach optimized for 7-day trading success. Point out where each extreme perspective overlooks important weekly considerations."""

        response = llm.invoke(prompt)

        argument = f"Neutral Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node

import time
import json


def create_risky_debator(llm):
    def risky_node(state) -> dict:
        company_name = state["company_of_interest"]
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        risky_history = risk_debate_state.get("risky_history", "")

        current_safe_response = risk_debate_state.get("current_safe_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""As the Aggressive Risk Analyst specialized in 7-DAY TRADING STRATEGIES, your role is to champion HIGH-REWARD, HIGH-RISK opportunities specifically for WEEKLY TRADING positions in {company_name}. Focus on maximizing potential gains on {company_name} over the NEXT 7 DAYS while acknowledging but not being paralyzed by risks.

**FOCUS: 7-DAY AGGRESSIVE RISK OPTIMIZATION FOR {company_name}**
Evaluate risk/reward for {company_name} WEEKLY timeframe, emphasizing why aggressive positioning can generate superior 7-day returns on {company_name}.

**YOUR 7-DAY AGGRESSIVE RISK FRAMEWORK FOR {company_name}:**

### 1. WEEKLY REWARD MAXIMIZATION FOR {company_name}:
- **High-Impact Catalysts**: Events in next 7 days that could drive significant {company_name} price moves (earnings, approvals, announcements)
- **Momentum Acceleration**: Technical setups suggesting strong weekly directional moves for {company_name}
- **Volatility Opportunities**: How weekly volatility creates profit opportunities for active {company_name} traders
- **Competitive Edge**: Why aggressive {company_name} positioning outperforms conservative approaches over 7 days

### 2. 7-DAY RISK TOLERANCE JUSTIFICATION FOR {company_name}:
- **Short-Term Risk Mitigation**: Why many long-term risks are irrelevant for 7-day {company_name} positions
- **Risk Management Tools**: Stop-losses, position sizing, and hedging strategies for weekly {company_name} trades
- **Opportunity Cost**: Risks of being too conservative and missing 7-day {company_name} profit opportunities
- **Recovery Potential**: How quickly aggressive {company_name} positions can recover within weekly timeframes

### 3. WEEKLY POSITION ADVOCACY FOR {company_name}:
Based on the trader's decision for {company_name}: {trader_decision}

**AGGRESSIVE ENHANCEMENT STRATEGIES FOR {company_name}:**
- **Position Size Increase**: Why larger {company_name} positions are justified for 7-day timeframe
- **Leverage Utilization**: Appropriate use of leverage for weekly {company_name} positions (options, margin)
- **Concentration Benefits**: Why focusing capital in high-conviction 7-day trades maximizes returns
- **Timing Optimization**: Why NOW is the optimal time for aggressive weekly positioning

### 4. COUNTER-CONSERVATIVE ARGUMENTS:
Challenge overly cautious viewpoints with 7-day focus:
- **Over-Hedging Risks**: How excessive hedging reduces weekly profit potential
- **Missed Opportunities**: Historical examples of conservative approaches missing 7-day gains
- **Risk-Reward Math**: Quantitative analysis showing aggressive positioning's weekly advantages
- **Market Efficiency**: Why aggressive trading captures inefficiencies in 7-day timeframes

### 5. 7-DAY AGGRESSIVE EXECUTION PLAN:
- **Entry Aggression**: Why immediate/aggressive entry captures best weekly opportunities
- **Position Scaling**: How to add to winning positions during the week
- **Risk Allocation**: Optimal risk budget allocation for weekly aggressive strategies
- **Profit Maximization**: Strategies to maximize gains when weekly trades move favorably

**DEBATE ENGAGEMENT STRATEGY:**
- **Challenge Conservative Fears**: Address conservative concerns with 7-day reality
- **Quantify Weekly Upside**: Use specific numbers, probabilities, and historical precedents
- **Risk Context**: Frame risks appropriately for weekly trading timeframe
- **Opportunity Emphasis**: Highlight the cost of inaction for 7-day opportunities

**DELIVERABLE REQUIREMENTS:**
Present a compelling aggressive risk case with:
1. **Weekly Opportunity Assessment**: Why this week favors aggressive positioning
2. **Risk-Reward Optimization**: How aggressive approach maximizes 7-day returns
3. **Conservative Counter-Arguments**: Why conservative concerns are overblown for weekly trades
4. **Execution Recommendation**: Specific aggressive strategies for the trader's weekly plan
5. **Performance Justification**: Why aggressive positioning will outperform over 7 days

Engage dynamically with conservative and neutral analysts, demonstrating why aggressive weekly positioning offers superior risk-adjusted returns for 7-day trading objectives.

Current market data:
Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Conversation history: {history} 
Conservative analyst's last response: {current_safe_response} 
Neutral analyst's last response: {current_neutral_response}

Engage actively by addressing conservative and neutral concerns while asserting why aggressive 7-day positioning offers optimal weekly returns. Challenge their assumptions and demonstrate the benefits of calculated weekly risk-taking."""

        response = llm.invoke(prompt)

        argument = f"Risky Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risky_history + "\n" + argument,
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Risky",
            "current_risky_response": argument,
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return risky_node

from langchain_core.messages import AIMessage
import time
import json


def create_safe_debator(llm):
    def safe_node(state) -> dict:
        company_name = state["company_of_interest"]
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        safe_history = risk_debate_state.get("safe_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_neutral_response = risk_debate_state.get("current_neutral_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""As the Conservative Risk Analyst specialized in 7-DAY TRADING STRATEGIES, your role is to champion CAPITAL PRESERVATION and RISK MINIMIZATION specifically for WEEKLY TRADING positions in {company_name}. Focus on protecting capital and avoiding unnecessary risks on {company_name} over the NEXT 7 DAYS.

**FOCUS: 7-DAY CONSERVATIVE RISK OPTIMIZATION FOR {company_name}**
Evaluate risk/reward for {company_name} WEEKLY timeframe, emphasizing capital preservation and measured risk-taking for {company_name}.

**YOUR 7-DAY CONSERVATIVE RISK FRAMEWORK FOR {company_name}:**

### 1. WEEKLY RISK MITIGATION FOR {company_name}:
- **Downside Protection**: Potential risks that could negatively impact {company_name} in next 7 days
- **Volatility Concerns**: How weekly market volatility could harm {company_name} positions
- **Position Sizing Caution**: Why smaller {company_name} positions are safer for weekly timeframe
- **Defensive Strategies**: How conservative positioning protects against {company_name} weekly losses

### 2. 7-DAY CAPITAL PRESERVATION FOR {company_name}:
- **Risk Management Priority**: Why protecting capital should be the primary focus for {company_name} weekly trades
- **Stop-Loss Emphasis**: Importance of tight stop-losses for weekly {company_name} positions
- **Position Limits**: Maximum safe position sizes for {company_name} in volatile weekly markets
- **Opportunity Cost Analysis**: Why missing gains is better than taking losses on {company_name}

### 3. WEEKLY POSITION CAUTION FOR {company_name}:
Based on the trader's decision for {company_name}: {trader_decision}

**CONSERVATIVE REFINEMENT STRATEGIES FOR {company_name}:**
- **Position Size Reduction**: Why smaller {company_name} positions are more appropriate for weekly risk
- **Enhanced Hedging**: Additional protective measures for weekly {company_name} exposure

### 4. COUNTER-AGGRESSIVE ARGUMENTS:
Challenge overly risky viewpoints with 7-day reality:
- **Volatility Risks**: How weekly volatility can quickly eliminate gains from aggressive positioning
- **Timing Risks**: Why aggressive entry now may lead to poor 7-day outcomes
- **Leverage Dangers**: How leverage amplifies losses in weekly timeframes
- **Recovery Time**: Why 7-day positions don't allow time for recovery from losses

### 5. 7-DAY CONSERVATIVE EXECUTION PLAN:
- **Gradual Entry**: Why scaling into positions over the week reduces timing risk
- **Tight Risk Controls**: Specific stop-loss and position limits for weekly trades
- **Profit Taking**: Why taking profits early in the week locks in gains
- **Exit Discipline**: Clear criteria for exiting weekly positions to preserve capital

**DEBATE ENGAGEMENT STRATEGY:**
- **Challenge Aggressive Assumptions**: Address unrealistic expectations with 7-day data
- **Quantify Weekly Risks**: Use specific loss scenarios and historical volatility patterns
- **Opportunity Cost Reality**: Show costs of aggressive losses vs conservative steady gains
- **Risk Context**: Frame aggressive strategies' dangers within weekly timeframe

**DELIVERABLE REQUIREMENTS:**
Present a compelling conservative risk case with:
1. **Weekly Risk Assessment**: Why this week requires defensive positioning
2. **Capital Preservation Plan**: How conservative approach protects wealth over 7 days
3. **Aggressive Risk Warnings**: Why aggressive concerns are valid for weekly trades
4. **Execution Recommendation**: Specific conservative adjustments to trader's weekly plan
5. **Safety Justification**: Why conservative positioning will outperform on risk-adjusted basis

Engage dynamically with aggressive and neutral analysts, demonstrating why conservative weekly positioning offers superior risk-adjusted returns and capital preservation for 7-day trading objectives.

Current market data:
Market Research Report: {market_research_report}
Social Media Sentiment Report: {sentiment_report}
Latest World Affairs Report: {news_report}
Company Fundamentals Report: {fundamentals_report}

Conversation history: {history} 
Aggressive analyst's last response: {current_risky_response}
Neutral analyst's last response: {current_neutral_response}

Engage actively by challenging aggressive and neutral assumptions while demonstrating why conservative 7-day positioning offers optimal weekly risk management and sustainable returns."""

        response = llm.invoke(prompt)

        argument = f"Safe Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": safe_history + "\n" + argument,
            "neutral_history": risk_debate_state.get("neutral_history", ""),
            "latest_speaker": "Safe",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": argument,
            "current_neutral_response": risk_debate_state.get(
                "current_neutral_response", ""
            ),
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return safe_node

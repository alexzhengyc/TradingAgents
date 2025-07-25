Below is a **worked‑out recipe** you can drop in right after `get_stock_stats_metrics()`.
It is completely self‑contained, uses only the metrics your function already returns, and gives you a **0‑to‑100 “Uptrend Score”** that estimates how strong an upside move is in the next 7‑14 days.

---

## 1.  Design philosophy

| Block                       | Why it matters for a 7‑14 d swing                                                                                   | How we translate it to numbers                          |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Trend / Direction**       | We want price already pressing above short MAs *and* a healthy ADX (≥ 20) so we’re betting with the current thrust. | Price‑vs‑MA ratios, MA5 direction, MA5‑MA20 spread, ADX |
| **Momentum / Acceleration** | Fresh momentum often precedes multi‑day follow‑through.                                                             | RSI, ROC, MACD‑hist, Stoch‑%K                           |
| **Volume / Flow**           | Rising price on rising volume / positive OBV is higher conviction.                                                  | Vol‑over‑avg20, OBV slope, MFI                          |
| **Volatility & Stretch**    | Extreme volatility or a stretched band move (< 2σ below or > 2σ above) tends to mean‑revert—so we *penalize* it.    | ATR %, HV10, Bollinger %B, z‑score                      |

We compute a **sub‑score for each block (0‑100)** and finally a weighted average:

```
UptrendScore = 0.4*Trend  + 0.3*Momentum
             + 0.2*Volume + 0.1*(100‑VolatilityPenalty)
```

*(weights sum to 1; tweak after you back‑test).*

---

## 2.  Scoring mechanics

To keep things interpretable, each raw metric is first mapped to a **unit interval** via a simple piece‑wise rule or logistic curve, then rescaled to 0‑100.

```python
import numpy as np

def _sig(x, center=0, width=1):
    """Logistic squashing helper – maps ℝ→(0,1)."""
    return 1/(1+np.exp(-(x-center)/width))

def score_from_metrics(m):
    """Return UptrendScore and the block‑level scores."""
    # --- 1. Trend block ---------------------------------
    trend_parts = [
        _sig(m['price_vs_ma5']-1, 0, 0.02),        # want >1
        _sig(m['price_vs_ma10']-1, 0, 0.02),
        1 if m['ma5_direction_sign']>0 else 0,
        _sig(m['ma5_minus_ma20']/m['price_vs_ma10'], 0, 0.01),
        _sig(m['adx_7']-20, 0, 5)                  # ADX 25≃strong
    ]
    trend = np.mean(trend_parts)*100

    # --- 2. Momentum block ------------------------------
    momentum_parts = [
        _sig(m['rsi_5']-50, 0, 7),                 # smooth around 50
        _sig(m['rsi_7']-50, 0, 7),
        _sig(m['roc_5'], 0, 1),
        _sig(m['macd_hist_6_19_5'], 0, 0.5),
        _sig(m['stoch_k_7']-50, 0, 10)
    ]
    momentum = np.mean(momentum_parts)*100

    # --- 3. Volume / Flow block -------------------------
    volume_parts = [
        _sig(m['vol_over_avg20']-1, 0, 0.3),
        _sig(m['obv_slope_5'], 0, 1e6),            # scale obv slope
        _sig(m['mfi_7']-50, 0, 10)
    ]
    volume = np.mean(volume_parts)*100

    # --- 4. Volatility penalty (higher = worse) ---------
    vol_penalty_parts = [
        _sig(m['atr5_pct']-0.025, 0, 0.01),        # >2.5 % daily ATR?
        _sig(m['hv_10']-0.35, 0, 0.1),             # >35 % annual HV?
        _sig(abs(m['zscore_price_10'])-1.5, 0, 0.5), # price stretched?
        _sig(abs(m['pctB_10']-0.5)-0.4, 0, 0.1)    # near band extremes?
    ]
    vol_penalty = np.mean(vol_penalty_parts)*100

    # --- 5. Final weighted score ------------------------
    uptrend = (0.4*trend + 0.3*momentum + 0.2*volume + 0.1*(100-vol_penalty))

    return {
        'UptrendScore': round(uptrend,1),
        'Trend': round(trend,1),
        'Momentum': round(momentum,1),
        'VolumeFlow': round(volume,1),
        'VolatilityPenalty': round(vol_penalty,1)
    }
```

### Interpretation

| UptrendScore | Interpretation               | Suggested action\*                           |
| ------------ | ---------------------------- | -------------------------------------------- |
| **≥ 75**     | Strong, broad confirmation   | Consider scaling into a 1–2 wk long          |
| 60 – 74      | Constructive but not perfect | Smaller starter position / wait for pullback |
| 45 – 59      | Neutral                      | Stay flat unless you have other edge         |
| **< 45**     | Weak / downtrend             | Avoid longs or look for shorts               |

\*Not financial advice—just a sample decision rubric.

---

## 3.  How to calibrate / validate

1. **Label 10 yrs of history**: For each trading day, compute whether `Close(t+10)` is ≥ `Close(t)*(1+X%)` (e.g., +2.0 %).
2. **Create a dataframe** with your metrics at *t* and the binary label.
3. **Run logistic regression** (or gradient boosting) to learn optimal weights.
4. Plug the learned coefficients back into the block construction (or replace the whole scoring rule).
5. **Walk‑forward test** by retraining yearly and checking hit‑rate, average return per flagged trade, Kelly‑criterion value, etc.

---

## 4.  Usage example

```python
metrics = get_stock_stats_metrics('AAPL', '2025-07-23')
score   = score_from_metrics(metrics)
print(score)
# {'UptrendScore': 68.4, 'Trend': 72.1, 'Momentum': 65.7,
#  'VolumeFlow': 59.3, 'VolatilityPenalty': 30.0}
```

You now have a single, interpretable number that combines price action, momentum, volume, and risk into a 7‑14 day directional bias—and a clear path to tune it with real data.

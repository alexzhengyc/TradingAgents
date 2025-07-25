import pandas as pd
import numpy as np
import yfinance as yf
from stockstats import StockDataFrame as Sdf


def get_stock_stats_metrics(symbol: str, date: str) -> dict:
    """
    symbol: e.g. 'AAPL'
    date: 'YYYY-MM-DD'
    returns: dict of metrics
    """
    curr_dt = pd.to_datetime(date)

    # ---- 1) Download enough history (at least 60 trading days) ----
    hist_start = curr_dt - pd.Timedelta(days=120)
    raw = yf.download(symbol, start=hist_start.strftime("%Y-%m-%d"), end=(curr_dt + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), auto_adjust=True)
    if raw.empty:
        raise ValueError("No data returned. Check symbol/date.")
    
    # Handle multi-level columns from yfinance
    if isinstance(raw.columns, pd.MultiIndex):
        # Flatten multi-level columns by taking the first level (the actual column names)
        raw.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in raw.columns]
    else:
        raw = raw.rename(columns=str.lower)  # yfinance uses 'Close', etc.

    # Stockstats needs columns: open, close, high, low, volume
    df = Sdf.retype(raw[['open','high','low','close','volume']].copy())

    # Ensure we have rows up to date
    df = df[df.index <= curr_dt]
    if len(df) < 25:
        raise ValueError("Not enough history before date to compute all metrics.")

    # Helper: latest row
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last

    # ---- Trend / Direction ----
    # Calculate moving averages - access them to trigger calculation, then get latest values
    ma5_series = df['close_5_sma']
    ma10_series = df['close_10_sma'] 
    ma20_series = df['close_20_sma']
    
    price_vs_ma5  = last['close'] / ma5_series.iloc[-1]
    price_vs_ma10 = last['close'] / ma10_series.iloc[-1]
    ma5_direction = np.sign(ma5_series.iloc[-1] - ma5_series.iloc[-2])  # +1 up, -1 down, 0 flat
    ma5_minus_ma20 = ma5_series.iloc[-1] - ma20_series.iloc[-1]

    # Calculate DMI and ADX indicators with error handling
    try:
        pdi_series = df['pdi_7']
        dmi_pdi_7 = float(pdi_series.iloc[-1])
    except:
        dmi_pdi_7 = 50.0  # Neutral value
    
    try:
        mdi_series = df['mdi_7']
        dmi_mdi_7 = float(mdi_series.iloc[-1])
    except:
        dmi_mdi_7 = 50.0  # Neutral value
        
    try:
        adx_series = df['adx_7']
        adx_7 = float(adx_series.iloc[-1])
    except:
        adx_7 = 25.0  # Moderate trend strength

    # ---- Momentum / Acceleration ----
    # Calculate RSI indicators
    rsi5_series = df['rsi_5']
    rsi7_series = df['rsi_7']
    rsi_5 = rsi5_series.iloc[-1]; rsi_7 = rsi7_series.iloc[-1]

    # Calculate ROC indicator with error handling
    try:
        roc5_series = df['roc_5']
        roc_5 = float(roc5_series.iloc[-1])
    except:
        roc_5 = 0.0  # No change

    # Calculate MACD histogram with error handling
    try:
        macdh_series = df['macdh_6_19_5']
        macd_hist_6_19_5 = float(macdh_series.iloc[-1])
    except:
        macd_hist_6_19_5 = 0.0  # Neutral

    # Stochastic %K(7) with error handling
    try:
        kdjk_series = df['kdjk_7']
        stoch_k_7 = float(kdjk_series.iloc[-1])
    except:
        stoch_k_7 = 50.0  # Neutral

    # ---- Volatility / Mean Reversion ----
    # %B (10-day)
    roll10_mean = df['close'].rolling(10).mean()
    roll10_std  = df['close'].rolling(10).std(ddof=0)
    upper = roll10_mean + 2 * roll10_std
    lower = roll10_mean - 2 * roll10_std
    pctB_10 = float((last['close'] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]))

    # ATR(5)/Price with error handling
    try:
        atr5_series = df['atr_5']
        atr5_pct = float(atr5_series.iloc[-1] / last['close'])
    except:
        atr5_pct = 0.02  # Default 2% volatility

    # HV(10) using log returns
    logret = np.log(df['close']).diff()
    hv10 = float(logret.rolling(10).std(ddof=0).iloc[-1] * np.sqrt(252))

    # Z-score(Price,10)
    zscore_10 = float((last['close'] - roll10_mean.iloc[-1]) / roll10_std.iloc[-1])

    # ---- Volume / Flow ----
    vol_ratio_20 = float(last['volume'] / df['volume'].rolling(20).mean().iloc[-1])

    # Calculate OBV and its slope with error handling
    try:
        obv_series = df['obv']
        # slope of OBV over last 5 days (simple linear regression coefficient)
        window = 5
        x = np.arange(window)
        obv_slice = obv_series.iloc[-window:]
        obv_slope_5 = float(np.polyfit(x, obv_slice.values, 1)[0])
    except:
        obv_slope_5 = 0.0  # No trend

    # Calculate MFI indicator with error handling
    try:
        mfi7_series = df['mfi_7']
        mfi_7 = float(mfi7_series.iloc[-1])
    except:
        mfi_7 = 50.0  # Neutral

    # VWAP distance (daily cumulative)
    vwap = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    vwap_distance = float((last['close'] - vwap.iloc[-1]) / vwap.iloc[-1])

    # ---- Build output ----
    out = {
        "symbol": symbol,
        "as_of": str(df.index[-1].date()),
        # 1. Trend / Direction
        "price_vs_ma5": float(price_vs_ma5),
        "price_vs_ma10": float(price_vs_ma10),
        "ma5_direction_sign": int(ma5_direction),  # +1 up, -1 down, 0 flat
        "ma5_minus_ma20": float(ma5_minus_ma20),
        "pdi_7": float(dmi_pdi_7),
        "mdi_7": float(dmi_mdi_7),
        "adx_7": float(adx_7),

        # 2. Momentum / Acceleration
        "rsi_5": float(rsi_5),
        "rsi_7": float(rsi_7),
        "roc_5": float(roc_5),
        "macd_hist_6_19_5": float(macd_hist_6_19_5),
        "stoch_k_7": float(stoch_k_7),

        # 3. Volatility / Mean Reversion
        "pctB_10": float(pctB_10),
        "atr5_pct": float(atr5_pct),
        "hv_10": float(hv10),
        "zscore_price_10": float(zscore_10),

        # 4. Volume / Flow
        "vol_over_avg20": float(vol_ratio_20),
        "obv_slope_5": float(obv_slope_5),
        "mfi_7": float(mfi_7),
        "vwap_distance": float(vwap_distance),
    }
    return out


def _sig(x, center=0, width=1):
    """Logistic squashing helper – maps ℝ→(0,1)."""
    return 1/(1+np.exp(-(x-center)/width))


def score_stock_from_metrics(m):
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
        _sig(m['atr5_pct']-0.025, 0, 0.01),        # >2.5 % daily ATR?
        _sig(m['hv_10']-0.35, 0, 0.1),             # >35 % annual HV?
        _sig(abs(m['zscore_price_10'])-1.5, 0, 0.5), # price stretched?
        _sig(abs(m['pctB_10']-0.5)-0.4, 0, 0.1)    # near band extremes?
    ]
    vol_penalty = np.mean(vol_penalty_parts)*100

    return {
        'Trend': round(trend,1),
        'Momentum': round(momentum,1),
        'VolumeFlow': round(volume,1),
        'VolatilityPenalty': round(vol_penalty,1)
    } 
import pandas as pd
import numpy as np
import yfinance as yf
from stockstats import StockDataFrame as Sdf
from typing import Annotated
import os
from .config import get_config


def compute_metrics(symbol: str, curr_date: str) -> dict:
    """
    symbol: e.g. 'AAPL'
    curr_date: 'YYYY-MM-DD'
    returns: dict of metrics
    """
    curr_dt = pd.to_datetime(curr_date)

    # ---- 1) Download enough history (at least 60 trading days) ----
    hist_start = curr_dt - pd.Timedelta(days=120)
    raw = yf.download(symbol, start=hist_start.strftime("%Y-%m-%d"), end=(curr_dt + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    if raw.empty:
        raise ValueError("No data returned. Check symbol/date.")
    raw = raw.rename(columns=str.lower)  # yfinance uses 'Close', etc.

    # Stockstats needs columns: open, close, high, low, volume
    df = Sdf.retype(raw[['open','high','low','close','volume']].copy())

    # Ensure we have rows up to curr_date
    df = df[df.index <= curr_dt]
    if len(df) < 25:
        raise ValueError("Not enough history before curr_date to compute all metrics.")

    # Helper: latest row
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last

    # ---- Trend / Direction ----
    df['close_5_sma']; df['close_10_sma']; df['close_20_sma']
    price_vs_ma5  = last['close'] / last['close_5_sma']
    price_vs_ma10 = last['close'] / last['close_10_sma']
    ma5_direction = np.sign(last['close_5_sma'] - prev['close_5_sma'])  # +1 up, -1 down, 0 flat
    ma5_minus_ma20 = last['close_5_sma'] - last['close_20_sma']

    df['pdi_7']; df['mdi_7']; df['adx_7']   # stockstats calculates these
    dmi_pdi_7 = last['pdi_7']
    dmi_mdi_7 = last['mdi_7']
    adx_7     = last['adx_7']

    # ---- Momentum / Acceleration ----
    df['rsi_5']; df['rsi_7']
    rsi_5 = last['rsi_5']; rsi_7 = last['rsi_7']

    df['roc_5']
    roc_5 = last['roc_5']

    df['macdh_6_19_5']  # hist
    macd_hist_6_19_5 = last['macdh_6_19_5']

    # Stochastic %K(7) (stockstats kdjk_7)
    df['kdjk_7']
    stoch_k_7 = last['kdjk_7']

    # ---- Volatility / Mean Reversion ----
    # %B (10-day)
    roll10_mean = df['close'].rolling(10).mean()
    roll10_std  = df['close'].rolling(10).std(ddof=0)
    upper = roll10_mean + 2 * roll10_std
    lower = roll10_mean - 2 * roll10_std
    pctB_10 = float((last['close'] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]))

    # ATR(5)/Price
    df['atr_5']
    atr5_pct = float(last['atr_5'] / last['close'])

    # HV(10) using log returns
    logret = np.log(df['close']).diff()
    hv10 = float(logret.rolling(10).std(ddof=0).iloc[-1] * np.sqrt(252))

    # Z-score(Price,10)
    zscore_10 = float((last['close'] - roll10_mean.iloc[-1]) / roll10_std.iloc[-1])

    # ---- Volume / Flow ----
    vol_ratio_20 = float(last['volume'] / df['volume'].rolling(20).mean().iloc[-1])

    df['obv']
    # slope of OBV over last 5 days (simple linear regression coefficient)
    window = 5
    x = np.arange(window)
    obv_slice = df['obv'].iloc[-window:]
    obv_slope_5 = float(np.polyfit(x, obv_slice.values, 1)[0])

    df['mfi_7']
    mfi_7 = last['mfi_7']

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


# Example:
if __name__ == "__main__":
    print(compute_metrics("AAPL", "2025-07-23"))

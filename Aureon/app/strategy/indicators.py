"""
Technical Indicators Calculation Module.
Implements EMA, RSI, ATR, and Volume confirmation metrics using Pandas.
"""

import pandas as pd
import numpy as np


def calculate_ema(df: pd.DataFrame, period: int = 20, column: str = "close") -> pd.Series:
    """
    Calculates Exponential Moving Average (EMA).
    """
    return df[column].ewm(span=period, adjust=False).mean()


def calculate_rsi(df: pd.DataFrame, period: int = 14, column: str = "close") -> pd.Series:
    """
    Calculates Relative Strength Index (RSI) using Wilder's smoothing technique.
    """
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Wilder's smoothing using Exponential Moving Average
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    
    # Handle division by zero or NaN cases
    rsi = rsi.replace([np.inf, -np.inf], np.nan).fillna(50.0)
    return rsi


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculates Average True Range (ATR).
    """
    high = df["high"]
    low = df["low"]
    close_prev = df["close"].shift(1)

    tr1 = high - low
    tr2 = (high - close_prev).abs()
    tr3 = (low - close_prev).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR is Wilder's smoothing (EMA) of True Range
    atr = tr.ewm(alpha=1/period, adjust=False).mean()
    return atr


def calculate_volume_sma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Calculates Simple Moving Average (SMA) of Volume.
    """
    return df["volume"].rolling(window=period).mean()


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and appends all strategy technical indicators to the DataFrame.
    
    Required Columns in df:
        'close', 'high', 'low', 'volume'
        
    Returns:
        pd.DataFrame: DataFrame with indicators: 'ema_20', 'ema_50', 'rsi_14', 'atr_14', 'volume_sma_20'
    """
    df = df.copy()
    
    # Sort by time index if necessary
    if "time" in df.columns:
        df = df.sort_values("time").reset_index(drop=True)
        
    df["ema_20"] = calculate_ema(df, period=20)
    df["ema_50"] = calculate_ema(df, period=50)
    df["rsi_14"] = calculate_rsi(df, period=14)
    df["atr_14"] = calculate_atr(df, period=14)
    df["volume_sma_20"] = calculate_volume_sma(df, period=20)
    
    return df

"""
Market Structure Analysis Module.
Analyzes local swings (Highs and Lows) to determine if structure is Bullish, Bearish, or Neutral.
Supports Break of Structure (BOS) detection.
"""

import pandas as pd
from typing import Tuple, List, Optional


def find_swings(df: pd.DataFrame, window: int = 5) -> Tuple[List[int], List[float], List[int], List[float]]:
    """
    Identifies Swing Highs and Swing Lows (local extrema) in a DataFrame.
    
    A swing high is a high that is greater than or equal to 'window' bars before and after.
    A swing low is a low that is less than or equal to 'window' bars before and after.
    
    Returns:
        Tuple[List[int], List[float], List[int], List[float]]: (high_indices, high_prices, low_indices, low_prices)
    """
    high_indices, high_prices = [], []
    low_indices, low_prices = [], []
    
    n = len(df)
    if n < (window * 2 + 1):
        return high_indices, high_prices, low_indices, low_prices

    for i in range(window, n - window):
        # Slice the window surrounding the current bar
        window_highs = df["high"].iloc[i - window : i + window + 1]
        window_lows = df["low"].iloc[i - window : i + window + 1]
        
        current_high = df["high"].iloc[i]
        current_low = df["low"].iloc[i]
        
        # Check if current high is the maximum in window
        if current_high == window_highs.max():
            # Avoid duplicate indices
            if not high_indices or high_indices[-1] != i:
                high_indices.append(i)
                high_prices.append(current_high)
                
        # Check if current low is the minimum in window
        if current_low == window_lows.min():
            if not low_indices or low_indices[-1] != i:
                low_indices.append(i)
                low_prices.append(current_low)

    return high_indices, high_prices, low_indices, low_prices


def analyze_market_structure(df: pd.DataFrame, window: int = 5) -> str:
    """
    Determines if the market structure is BULLISH, BEARISH, or NEUTRAL.
    
    Rules:
        - BULLISH: Close price crosses above the last Swing High (Break of Structure to upside)
                   or Higher High + Higher Low sequence.
        - BEARISH: Close price crosses below the last Swing Low (Break of Structure to downside)
                   or Lower High + Lower Low sequence.
    """
    if len(df) < 30:
        return "NEUTRAL"

    high_idx, high_vals, low_idx, low_vals = find_swings(df, window=window)
    current_close = df["close"].iloc[-1]
    
    # Need at least two swings to compare HH/HL or LH/LL
    if len(high_vals) < 2 or len(low_vals) < 2:
        # Fallback to Simple EMA trend comparison
        if "ema_20" in df.columns and "ema_50" in df.columns:
            ema20 = df["ema_20"].iloc[-1]
            ema50 = df["ema_50"].iloc[-1]
            return "BULLISH" if ema20 > ema50 else "BEARISH"
        return "NEUTRAL"

    last_swing_high = high_vals[-1]
    prev_swing_high = high_vals[-2]
    
    last_swing_low = low_vals[-1]
    prev_swing_low = low_vals[-2]

    # 1. Break of Structure (BOS) Rule
    if current_close > last_swing_high:
        return "BULLISH"
    if current_close < last_swing_low:
        return "BEARISH"

    # 2. Sequence Rule (HH/HL or LH/LL)
    is_higher_high = last_swing_high > prev_swing_high
    is_higher_low = last_swing_low > prev_swing_low
    is_lower_high = last_swing_high < prev_swing_high
    is_lower_low = last_swing_low < prev_swing_low

    if is_higher_high and is_higher_low:
        return "BULLISH"
    elif is_lower_high and is_lower_low:
        return "BEARISH"

    # 3. Dynamic trend fallback
    if "ema_20" in df.columns and "ema_50" in df.columns:
        ema20 = df["ema_20"].iloc[-1]
        ema50 = df["ema_50"].iloc[-1]
        if ema20 > ema50 and current_close > last_swing_low:
            return "BULLISH"
        if ema20 < ema50 and current_close < last_swing_high:
            return "BEARISH"

    return "NEUTRAL"

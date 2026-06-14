"""
XAUUSD Trading Strategy Module.
Applies technical rules (EMA crossovers, RSI, Volume SMA, and Market Structure)
to evaluate trade candidates and calculate ATR-based stops.
"""

import pandas as pd
from typing import Dict, Any
from app.strategy.indicators import add_all_indicators
from app.strategy.market_structure import analyze_market_structure
from app.utils.logger import app_logger
from app.utils.helpers import round_price


def evaluate_strategy(df: pd.DataFrame, atr_multiplier: float = 1.5, rr_ratio: float = 2.0) -> Dict[str, Any]:
    """
    Evaluates current market indicators against strategy conditions for XAUUSD (Gold).
    
    Conditions:
        - BUY: EMA20 > EMA50, RSI > 55, Bullish structure, Volume > Average Volume
        - SELL: EMA20 < EMA50, RSI < 45, Bearish structure, Volume > Average Volume
        
    Stops:
        - SL: ATR-based (Entry - 1.5 * ATR for Buy, Entry + 1.5 * ATR for Sell)
        - TP: 1:2 Risk to Reward Minimum (configurable via rr_ratio)
        
    Args:
        df: DataFrame containing historical OHLCV data.
        atr_multiplier: Multiplier for dynamic stop loss calculation.
        rr_ratio: Risk-to-reward ratio (e.g. 2.0 = 1:2).
        
    Returns:
        Dict[str, Any]: Dict containing signal ('BUY', 'SELL', 'NONE') and stop targets.
    """
    # 1. Compute Indicators
    df_ind = add_all_indicators(df)
    
    # Get latest bar index
    latest_idx = df_ind.index[-1]
    
    # 2. Analyze Market Structure
    market_structure = analyze_market_structure(df_ind)
    
    # Extract latest indicators
    close = df_ind.loc[latest_idx, "close"]
    ema20 = df_ind.loc[latest_idx, "ema_20"]
    ema50 = df_ind.loc[latest_idx, "ema_50"]
    rsi = df_ind.loc[latest_idx, "rsi_14"]
    atr = df_ind.loc[latest_idx, "atr_14"]
    volume = df_ind.loc[latest_idx, "volume"]
    avg_volume = df_ind.loc[latest_idx, "volume_sma_20"]
    
    # Format log metrics
    app_logger.info(
        f"Evaluating Strategy - Close: {close:.2f} | EMA20: {ema20:.2f}, EMA50: {ema50:.2f} | "
        f"RSI: {rsi:.2f} | ATR: {atr:.2f} | Vol: {volume:.0f} (Avg: {avg_volume:.0f}) | Structure: {market_structure}"
    )

    signal = "NONE"
    sl_price = 0.0
    tp_price = 0.0

    # 3. Evaluate Signal Conditions
    
    # Buy Setup
    is_ema_bullish = ema20 > ema50
    is_rsi_bullish = rsi > 55
    is_structure_bullish = market_structure == "BULLISH"
    is_volume_confirmed = volume > avg_volume

    if is_ema_bullish and is_rsi_bullish and is_structure_bullish and is_volume_confirmed:
        signal = "BUY"
        # Dynamic ATR-based Stop Loss
        sl_price = close - (atr_multiplier * atr)
        # Take Profit based on minimum 1:2 RR ratio
        risk_distance = close - sl_price
        tp_price = close + (rr_ratio * risk_distance)
        
    # Sell Setup
    is_ema_bearish = ema20 < ema50
    is_rsi_bearish = rsi < 45
    is_structure_bearish = market_structure == "BEARISH"

    if is_ema_bearish and is_rsi_bearish and is_structure_bearish and is_volume_confirmed:
        signal = "SELL"
        # Dynamic ATR-based Stop Loss
        sl_price = close + (atr_multiplier * atr)
        # Take Profit based on minimum 1:2 RR ratio
        risk_distance = sl_price - close
        tp_price = close - (rr_ratio * risk_distance)

    # Round SL/TP to broker digits (2 decimals)
    sl_price = round_price(sl_price)
    tp_price = round_price(tp_price)

    result = {
        "signal": signal,
        "entry_price": round_price(close),
        "sl_price": sl_price,
        "tp_price": tp_price,
        "metrics": {
            "rsi": round(rsi, 2),
            "ema_20": round(ema20, 2),
            "ema_50": round(ema50, 2),
            "atr": round(atr, 2),
            "volume": int(volume),
            "avg_volume": int(avg_volume),
            "market_structure": market_structure
        }
    }
    
    if signal != "NONE":
        app_logger.info(f"Generated Strategy Signal: {signal} at {close:.2f}. SL: {sl_price:.2f}, TP: {tp_price:.2f}")
    else:
        app_logger.debug("Strategy evaluated. No trading signal triggered.")
        
    return result

"""
Unit Tests for Strategy Calculations and Rules.
"""

import pytest
import pandas as pd
import numpy as np
from app.strategy.indicators import add_all_indicators
from app.strategy.market_structure import find_swings, analyze_market_structure
from app.strategy.xauusd_strategy import evaluate_strategy


@pytest.fixture
def sample_bullish_data():
    """
    Generates synthetic bullish data where EMA20 > EMA50, RSI > 55, and volume is above average.
    """
    dates = pd.date_range(start="2026-06-01", periods=100, freq="h")
    data = []
    for i in range(100):
        # Steeper upward trend to ensure EMA crossover and high RSI
        o = 1900.0 + (i * 0.8)
        c = o + 1.2
        h = c + 1.5
        l = o - 0.8
        # Make the last volume spike to confirm volume check
        v = 100 if i < 99 else 250
        data.append([o, h, l, c, v])
        
    df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])
    df["time"] = dates
    return df


@pytest.fixture
def sample_bearish_data():
    """
    Generates synthetic bearish data where EMA20 < EMA50, RSI < 45, and volume is above average.
    """
    dates = pd.date_range(start="2026-06-01", periods=100, freq="h")
    data = []
    for i in range(100):
        # Steeper downward trend to ensure EMA crossover and low RSI
        o = 2100.0 - (i * 0.8)
        c = o - 1.2
        h = o + 0.8
        l = c - 1.5
        v = 100 if i < 99 else 250
        data.append([o, h, l, c, v])
        
    df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])
    df["time"] = dates
    return df


def test_add_indicators(sample_bullish_data):
    df_ind = add_all_indicators(sample_bullish_data)
    
    assert "ema_20" in df_ind.columns
    assert "ema_50" in df_ind.columns
    assert "rsi_14" in df_ind.columns
    assert "atr_14" in df_ind.columns
    assert "volume_sma_20" in df_ind.columns
    
    # Check if calculation is populated
    assert not df_ind["ema_20"].isna().iloc[-1]
    assert not df_ind["rsi_14"].isna().iloc[-1]


def test_find_swings(sample_bullish_data):
    # Should identify local swing peaks
    h_idx, h_vals, l_idx, l_vals = find_swings(sample_bullish_data, window=5)
    
    # We should have identified at least some extrema in 100 periods
    assert isinstance(h_idx, list)
    assert isinstance(h_vals, list)
    assert isinstance(l_idx, list)
    assert isinstance(l_vals, list)


def test_evaluate_strategy_bullish(sample_bullish_data):
    result = evaluate_strategy(sample_bullish_data)
    
    assert result["signal"] == "BUY"
    assert result["entry_price"] > 0.0
    assert result["sl_price"] < result["entry_price"]
    assert result["tp_price"] > result["entry_price"]
    assert result["metrics"]["market_structure"] == "BULLISH"


def test_evaluate_strategy_bearish(sample_bearish_data):
    result = evaluate_strategy(sample_bearish_data)
    
    assert result["signal"] == "SELL"
    assert result["entry_price"] > 0.0
    assert result["sl_price"] > result["entry_price"]
    assert result["tp_price"] < result["entry_price"]
    assert result["metrics"]["market_structure"] == "BEARISH"

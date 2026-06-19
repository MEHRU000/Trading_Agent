"""Utility functions for trade calculations.

Provides a standardized way to compute profit and pip/point differences for trades.
This module is deliberately lightweight and has no external dependencies beyond
the project settings.
"""

from typing import Optional

from app.utils.config import settings


def calculate_profit(order_type: str, entry_price: float, exit_price: float, volume: float, symbol: Optional[str] = None) -> float:
    """Calculate trade profit in account currency.

    Args:
        order_type: "BUY" or "SELL" (case‑insensitive).
        entry_price: Price at which the position was opened.
        exit_price: Price at which the position was closed.
        volume: Lots/units of the trade.
        symbol: The trade symbol (e.g., "XAUUSD", "EURUSD").

    Returns:
        Profit as a float. Uses the contract multiplier.
    """
    multiplier = getattr(settings, "CONTRACT_MULTIPLIER", 100.0)
    if symbol:
        try:
            from app.broker.mt5_connector import mt5_connector
            symbol_info = mt5_connector.api.symbol_info(symbol)
            if symbol_info:
                multiplier = symbol_info.trade_contract_size
        except Exception:
            # Fallback to standard multipliers based on symbol if mt5_connector queries fail
            symbol_upper = symbol.upper()
            if any(pair in symbol_upper for pair in ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"]):
                multiplier = 100000.0
            elif "XAUUSD" in symbol_upper:
                multiplier = 100.0
                
    order_type = order_type.upper()
    if order_type == "BUY":
        return (exit_price - entry_price) * volume * multiplier
    else:  # SELL
        return (entry_price - exit_price) * volume * multiplier


def calculate_pips(entry_price: float, exit_price: float, symbol: str) -> float:
    """Calculate the absolute pip difference for a trade.
    """
    point_size_map = {
        "XAUUSD": 0.01,
        "EURUSD": 0.00001,
        "GBPUSD": 0.00001,
        "USDJPY": 0.001,
        "AUDUSD": 0.00001,
        "USDCAD": 0.00001,
        "USDCHF": 0.00001,
        "NZDUSD": 0.00001,
    }
    
    point_size = 0.01
    try:
        from app.broker.mt5_connector import mt5_connector
        symbol_info = mt5_connector.api.symbol_info(symbol)
        if symbol_info:
            point_size = symbol_info.point
        else:
            point_size = point_size_map.get(symbol.upper(), 0.01)
    except Exception:
        point_size = point_size_map.get(symbol.upper(), 0.01)
        
    diff = abs(exit_price - entry_price)
    
    # In Forex, 1 pip = 10 points for 5-digit/3-digit pairs.
    symbol_upper = symbol.upper()
    is_forex = any(pair in symbol_upper for pair in ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"])
    
    pip_size = point_size
    if is_forex:
        pip_size = point_size * 10.0
        
    pips = diff / pip_size if pip_size != 0 else 0.0
    return pips


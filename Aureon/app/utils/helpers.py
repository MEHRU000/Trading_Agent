"""
Helper Utilities for XAUUSD Automated Trading System.
Provides timezone checks, pip/point math, and rounding routines.
"""

from datetime import datetime, timezone
from app.utils.config import settings


def get_utc_now() -> datetime:
    """
    Returns the current UTC time.
    """
    return datetime.now(timezone.utc)


def is_within_trading_hours() -> bool:
    """
    Checks if the current UTC time falls within the configured session hours.
    
    Returns:
        bool: True if current time is in trading hours, False otherwise.
    """
    now = get_utc_now()
    current_hour = now.hour
    return settings.SESSION_START_HOUR <= current_hour < settings.SESSION_END_HOUR


def points_to_pips(points: float) -> float:
    """
    Converts MT5 broker points to pips.
    For Gold (XAUUSD), 1 pip = 10 points = $0.10.
    
    Args:
        points: Number of points
        
    Returns:
        float: Equivalent pips
    """
    return points / 10.0


def pips_to_points(pips: float) -> float:
    """
    Converts pips to MT5 broker points.
    For Gold (XAUUSD), 1 pip = 10 points = $0.10.
    
    Args:
        pips: Number of pips
        
    Returns:
        float: Equivalent points
    """
    return pips * 10.0


def calculate_sl_distance_in_points(entry_price: float, sl_price: float) -> float:
    """
    Calculates the absolute distance between entry price and stop loss in points.
    
    Args:
        entry_price: The trade entry price
        sl_price: The trade stop loss price
        
    Returns:
        float: SL distance in points (rounded to integer)
    """
    # For XAUUSD, price scale is typically 2 decimal places. 1 point = 0.01.
    distance_price = abs(entry_price - sl_price)
    return round(distance_price * 100.0)


def round_lot_size(lot: float, step: float = 0.01, min_lot: float = 0.01, max_lot: float = 100.0) -> float:
    """
    Rounds the calculated lot size to comply with broker specification.
    
    Args:
        lot: Raw calculated lot size
        step: Lot step limit (usually 0.01)
        min_lot: Minimum lot size allowed (usually 0.01)
        max_lot: Maximum lot size allowed (usually 100.0)
        
    Returns:
        float: Conformed lot size
    """
    if lot < min_lot:
        return min_lot
    if lot > max_lot:
        return max_lot
        
    # Standard decimal precision based on step
    decimals = 0
    temp_step = step
    while temp_step < 1.0:
        temp_step *= 10.0
        decimals += 1
        
    rounded_lot = round(round(lot / step) * step, decimals)
    return max(min(rounded_lot, max_lot), min_lot)


def round_price(price: float, digits: int = 2) -> float:
    """
    Rounds price to the broker's digits (Gold is normally 2 decimal places).
    
    Args:
        price: Price to round
        digits: Broker decimal precision
        
    Returns:
        float: Rounded price
    """
    return round(price, digits)

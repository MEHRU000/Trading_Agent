"""
Drawdown Protection Module.
Monitors account balance and equity changes against daily/weekly limits.
"""

from datetime import datetime, timezone, timedelta
from typing import Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import AccountSnapshot
from app.utils.config import settings
from app.utils.logger import app_logger
from app.utils.helpers import get_utc_now


def get_peak_balance(db: Session, since: datetime) -> float:
    """
    Finds the maximum balance recorded in the account snapshots database since a specific time.
    
    Args:
        db: Database session
        since: Start datetime window
        
    Returns:
        float: Peak balance value found
    """
    peak = db.query(func.max(AccountSnapshot.balance)).filter(
        AccountSnapshot.timestamp >= since
    ).scalar()
    return float(peak) if peak is not None else 0.0


def check_drawdown(db: Session, current_equity: float, current_balance: float) -> Tuple[bool, str]:
    """
    Evaluates current equity against daily/weekly peak balance drawdown thresholds.
    
    Args:
        db: SQLAlchemy DB Session
        current_equity: Current account equity from broker terminal
        current_balance: Current account balance from broker terminal
        
    Returns:
        Tuple[bool, str]: (is_exceeded, reason_description)
    """
    now = get_utc_now()
    
    # Define time windows
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    start_of_week = start_of_day - timedelta(days=now.weekday())  # Monday 00:00

    # Get peak balances for tracking
    daily_peak = get_peak_balance(db, start_of_day)
    weekly_peak = get_peak_balance(db, start_of_week)

    # If no snapshots exist yet, use the current balance as base
    if daily_peak == 0.0:
        daily_peak = current_balance
    if weekly_peak == 0.0:
        weekly_peak = current_balance

    # Ensure peaks are at least equal to current balance
    daily_peak = max(daily_peak, current_balance)
    weekly_peak = max(weekly_peak, current_balance)

    # Calculate current drawdown percentages
    current_daily_drawdown = (daily_peak - current_equity) / daily_peak if daily_peak > 0 else 0.0
    current_weekly_drawdown = (weekly_peak - current_equity) / weekly_peak if weekly_peak > 0 else 0.0

    app_logger.debug(
        f"Drawdown Check - Equity: {current_equity:.2f}, Balance: {current_balance:.2f} | "
        f"Daily Peak: {daily_peak:.2f} (DD: {current_daily_drawdown * 100.0:.2f}%), "
        f"Weekly Peak: {weekly_peak:.2f} (DD: {current_weekly_drawdown * 100.0:.2f}%)"
    )

    # Validate against limits
    if current_daily_drawdown >= settings.MAX_DAILY_DRAWDOWN_PCT:
        msg = f"Daily drawdown limit of {settings.MAX_DAILY_DRAWDOWN_PCT * 100.0:.1f}% exceeded. Current: {current_daily_drawdown * 100.0:.2f}% (Peak: {daily_peak:.2f})"
        app_logger.warning(msg)
        return True, msg

    if current_weekly_drawdown >= settings.MAX_WEEKLY_DRAWDOWN_PCT:
        msg = f"Weekly drawdown limit of {settings.MAX_WEEKLY_DRAWDOWN_PCT * 100.0:.1f}% exceeded. Current: {current_weekly_drawdown * 100.0:.2f}% (Peak: {weekly_peak:.2f})"
        app_logger.warning(msg)
        return True, msg

    return False, "Drawdown within limits."

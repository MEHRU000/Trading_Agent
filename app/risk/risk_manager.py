"""
Risk Management Gateway.
Orchestrates trade safety checks (session, spread, trade limits, drawdown, duplicate trades).
"""

from typing import Tuple
from sqlalchemy.orm import Session
from app.broker.mt5_connector import mt5_connector
from app.broker.position_manager import position_manager
from app.database.trade_history import get_daily_trade_count
from app.risk.drawdown_protection import check_drawdown
from app.utils.config import settings
from app.utils.logger import app_logger
from app.utils.helpers import is_within_trading_hours


class RiskManager:
    """
    Main risk controller. Validates trade candidates against account and session parameters.
    """
    def __init__(self):
        self.connector = mt5_connector
        self.position_manager = position_manager

    def validate_trade_setup(self, db: Session, symbol: str, entry_price: float, sl_price: float) -> Tuple[bool, str]:
        """
        Validates all risk constraints. Returns (True, "Approved") if passed, or (False, rejection_reason).
        """
        app_logger.info(f"Starting risk validation for {symbol} trade setup...")

        # 1. Market Session Filter
        if not is_within_trading_hours():
            reason = f"Trade rejected: outside allowed trading hours ({settings.SESSION_START_HOUR}:00 - {settings.SESSION_END_HOUR}:00 UTC)."
            app_logger.warning(reason)
            return False, reason

        # Query broker statistics
        balance, equity, margin, free_margin = self.connector.get_account_state()
        if balance == 0.0:
            reason = "Trade rejected: Unable to query account state from broker terminal."
            app_logger.error(reason)
            return False, reason

        # 2. Drawdown Protection Check
        dd_exceeded, dd_reason = check_drawdown(db, equity, balance)
        if dd_exceeded:
            reason = f"Trade rejected: Drawdown limit breached. Details: {dd_reason}"
            app_logger.warning(reason)
            return False, reason

        # 3. Daily Trade Count Check
        today_trade_count = get_daily_trade_count(db)
        if today_trade_count >= settings.MAX_TRADES_PER_DAY:
            reason = f"Trade rejected: Daily trade execution limit reached ({today_trade_count}/{settings.MAX_TRADES_PER_DAY})."
            app_logger.warning(reason)
            return False, reason

        # 4. Duplicate Trade Check
        open_positions = self.position_manager.get_open_positions(symbol=symbol)
        if len(open_positions) > 0:
            reason = f"Trade rejected: Active position for {symbol} already exists. Duplicate trading blocked."
            app_logger.warning(reason)
            return False, reason

        # 5. Spread Check
        # For Gold (XAUUSD), 1 point = 0.01 price spread.
        symbol_info = self.connector.api.symbol_info(symbol)
        if symbol_info is None:
            reason = f"Trade rejected: Unable to fetch symbol info for {symbol}."
            app_logger.warning(reason)
            return False, reason
            
        current_spread = symbol_info.spread
        if current_spread > settings.MAX_SPREAD_POINTS:
            reason = f"Trade rejected: Current spread ({current_spread} points) exceeds maximum limit ({settings.MAX_SPREAD_POINTS} points)."
            app_logger.warning(reason)
            return False, reason

        app_logger.info("Risk validation successful. All risk criteria met.")
        return True, "Approved"


# Instantiate risk manager singleton
risk_manager = RiskManager()

"""
Position Management Module for XAUUSD Automated Trading System.
Monitors open positions, calculates pips profit, and executes trailing stop-loss logic.
"""

from typing import List, Dict, Any
from app.broker.mt5_connector import mt5_connector
from app.broker.order_manager import order_manager
from app.utils.config import settings
from app.utils.logger import app_logger
from app.utils.helpers import points_to_pips, pips_to_points, round_price


class PositionManager:
    """
    Monitors open positions and handles modifications such as trailing stops.
    """
    def __init__(self):
        self.connector = mt5_connector
        self.order_manager = order_manager

    def get_open_positions(self, symbol: str = "XAUUSD") -> List[Dict[str, Any]]:
        """
        Retrieves all currently active positions filtered by symbol and agent magic number.
        """
        api = self.connector.api
        
        # Query active positions from broker terminal
        raw_positions = api.positions_get(symbol=symbol)
        if raw_positions is None:
            err_code, err_msg = api.last_error()
            app_logger.error(f"Failed to query positions from terminal: {err_msg} (code: {err_code})")
            return []

        active_positions = []
        for pos in raw_positions:
            # Filter by Magic Number to prevent interfering with other strategies/manual trades
            if pos.magic == settings.MT5_MAGIC_NUMBER:
                active_positions.append({
                    "ticket": pos.ticket,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "type": "BUY" if pos.type == api.ORDER_TYPE_BUY else "SELL",
                    "price_open": pos.price_open,
                    "price_current": pos.price_current,
                    "sl": pos.sl,
                    "tp": pos.tp,
                    "profit": pos.profit,
                    "comment": pos.comment
                })
        return active_positions

    def manage_trailing_stops(self, symbol: str = "XAUUSD", trail_pips: float = 30.0, activation_pips: float = 40.0) -> None:
        """
        Scans open positions and adjusts Stop Loss if they move in favor of the trade by activation_pips.
        
        Args:
            symbol: Target symbol
            trail_pips: Distance to trailing price in pips
            activation_pips: Minimum profit in pips required to activate the trailing stop
        """
        positions = self.get_open_positions(symbol=symbol)
        if not positions:
            return

        tick = self.connector.get_tick_data(symbol)
        if not tick:
            app_logger.warning(f"Skipping trailing stop check: Tick pricing unavailable for {symbol}")
            return
            
        bid, ask = tick
        
        for pos in positions:
            ticket = pos["ticket"]
            entry_price = pos["price_open"]
            current_sl = pos["sl"]
            order_type = pos["type"]
            current_price = pos["price_current"]

            trail_points = pips_to_points(trail_pips)
            activation_points = pips_to_points(activation_pips)
            
            # Gold price calculation helper: distance in points
            # 1 pip = 10 points = $0.10. Therefore activation of 40 pips = 400 points = $4.00 profit.
            
            if order_type == "BUY":
                # Compute distance trade has traveled in profit
                profit_points = (bid - entry_price) * 100.0
                
                # Check if trade has reached activation threshold
                if profit_points >= activation_points:
                    # Calculate new SL level (trail_pips behind current price)
                    new_sl = bid - (trail_points / 100.0)
                    new_sl = round_price(new_sl)
                    
                    # Move SL up if the new SL is higher than current SL (and entry)
                    if current_sl == 0.0 or new_sl > current_sl:
                        app_logger.info(
                            f"Trailing Stop Triggered (BUY ticket {ticket}): "
                            f"Price: {bid}, Entry: {entry_price}, Old SL: {current_sl}, New SL: {new_sl}"
                        )
                        self.order_manager.modify_stops(ticket=ticket, sl=new_sl, tp=pos["tp"])
                        
            elif order_type == "SELL":
                # Compute distance trade has traveled in profit
                profit_points = (entry_price - ask) * 100.0
                
                # Check if trade has reached activation threshold
                if profit_points >= activation_points:
                    # Calculate new SL level (trail_pips behind current price)
                    new_sl = ask + (trail_points / 100.0)
                    new_sl = round_price(new_sl)
                    
                    # Move SL down if new SL is lower than current SL (and entry)
                    if current_sl == 0.0 or new_sl < current_sl:
                        app_logger.info(
                            f"Trailing Stop Triggered (SELL ticket {ticket}): "
                            f"Price: {ask}, Entry: {entry_price}, Old SL: {current_sl}, New SL: {new_sl}"
                        )
                        self.order_manager.modify_stops(ticket=ticket, sl=new_sl, tp=pos["tp"])


# Instantiate position manager singleton
position_manager = PositionManager()

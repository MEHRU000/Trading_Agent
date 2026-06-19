"""
Order Management Module for XAUUSD Automated Trading System.
Provides functionality for executing and modifying market orders.
"""

from typing import Dict, Any, Optional
from app.broker.mt5_connector import mt5_connector
from app.utils.config import settings
from app.utils.logger import app_logger
from app.utils.helpers import round_price


class OrderManager:
    """
    Coordinates direct order routing to the MT5 terminal client.
    """
    def __init__(self):
        self.connector = mt5_connector

    def send_market_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        sl: float,
        tp: float,
        comment: str = ""
    ) -> Dict[str, Any]:
        """
        Submits a market execution order (BUY or SELL) with stop loss and take profit.
        
        Returns:
            Dict[str, Any]: Execution details containing 'status', 'ticket', 'price', etc.
        """
        api = self.connector.api
        
        # Determine order type constants
        if order_type.upper() == "BUY":
            mt5_order_type = api.ORDER_TYPE_BUY
            price_type = "ask"
        elif order_type.upper() == "SELL":
            mt5_order_type = api.ORDER_TYPE_SELL
            price_type = "bid"
        else:
            raise ValueError(f"Invalid order type specified: {order_type}")

        # Fetch current price ticks
        tick = self.connector.get_tick_data(symbol)
        if not tick:
            raise RuntimeError(f"Cannot execute order: tick pricing unavailable for {symbol}")
        
        bid, ask = tick
        execution_price = ask if price_type == "ask" else bid
        
        # Round stops to required digits (usually 2 decimal places for Gold)
        sl = round_price(sl)
        tp = round_price(tp)
        
        # Build trade request payload
        request = {
            "action": api.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5_order_type,
            "price": execution_price,
            "sl": sl,
            "tp": tp,
            "deviation": settings.MAX_SLIPPAGE_POINTS,
            "magic": settings.MT5_MAGIC_NUMBER,
            "comment": comment,
            "type_time": 0,  # GTC (Good till cancelled)
            "type_filling": 1,  # FOK (Fill or Kill) - adjust if broker requires IOC or Return
        }

        app_logger.info(f"Submitting order request: {order_type} {volume} lots on {symbol} at {execution_price} SL: {sl} TP: {tp}")
        
        try:
            result = api.order_send(request)
            
            if result is None:
                err_code, err_msg = api.last_error()
                raise RuntimeError(f"Broker terminal returned None. Last error: {err_msg} (code: {err_code})")
                
            if result.retcode != api.TRADE_RETCODE_DONE:
                raise RuntimeError(
                    f"Broker order submission failed. Retcode: {result.retcode}. "
                    f"Comment: {getattr(result, 'comment', 'N/A')}"
                )
                
            app_logger.info(f"Order executed successfully. Ticket: {result.order}. Execution Price: {result.price}")
            
            return {
                "status": "SUCCESS",
                "ticket": result.order,
                "price": result.price,
                "volume": result.volume,
                "sl": sl,
                "tp": tp,
                "commission": getattr(result, "commission", 0.0),
                "comment": comment
            }
            
        except Exception as e:
            app_logger.error(f"Order submission exception raised: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "ticket": None
            }

    def modify_stops(self, ticket: int, sl: float, tp: float) -> bool:
        """
        Modifies the Stop Loss and Take Profit targets of an existing open position.
        """
        api = self.connector.api
        
        # Round stops
        sl = round_price(sl)
        tp = round_price(tp)
        
        # Retrieve active position to capture symbol
        positions = api.positions_get(ticket=ticket)
        if not positions:
            app_logger.warning(f"Could not locate active position for ticket {ticket} to modify stops.")
            return False
            
        position = positions[0]
        
        request = {
            "action": 6,  # TRADE_ACTION_SLTP (Modify Stop Loss & Take Profit)
            "symbol": position.symbol,
            "position": ticket,
            "sl": sl,
            "tp": tp
        }
        
        app_logger.info(f"Submitting stops modification for ticket {ticket}. New SL: {sl} New TP: {tp}")
        
        try:
            result = api.order_send(request)
            if result is None:
                err_code, err_msg = api.last_error()
                app_logger.error(f"Modification returned None. Last error: {err_msg} (code: {err_code})")
                return False
                
            if result.retcode != api.TRADE_RETCODE_DONE:
                app_logger.error(f"Stops modification failed. Retcode: {result.retcode}. Comment: {getattr(result, 'comment', 'N/A')}")
                return False
                
            app_logger.info(f"Stops modified successfully for position ticket: {ticket}")
            return True
        except Exception as e:
            app_logger.error(f"Error modifying stops for ticket {ticket}: {e}")
            return False

    def close_position_by_ticket(self, ticket: int, comment: str = "Close order") -> bool:
        """
        Closes an active position completely at market price.
        """
        api = self.connector.api
        
        # Retrieve position details
        positions = api.positions_get(ticket=ticket)
        if not positions:
            app_logger.warning(f"Cannot close position: Ticket {ticket} not found among active positions.")
            return False
            
        position = positions[0]
        symbol = position.symbol
        volume = position.volume
        
        # Determine opposite order type to close
        close_type = api.ORDER_TYPE_SELL if position.type == api.ORDER_TYPE_BUY else api.ORDER_TYPE_BUY
        
        # Fetch current price ticks
        tick = self.connector.get_tick_data(symbol)
        if not tick:
            app_logger.error(f"Cannot close position {ticket}: pricing tick info unavailable for {symbol}")
            return False
            
        bid, ask = tick
        price = ask if close_type == api.ORDER_TYPE_BUY else bid
        
        request = {
            "action": api.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": settings.MAX_SLIPPAGE_POINTS,
            "magic": settings.MT5_MAGIC_NUMBER,
            "comment": comment
        }
        
        app_logger.info(f"Closing position ticket {ticket} ({symbol} {volume} lots) at price {price}")
        
        try:
            result = api.order_send(request)
            if result is None:
                err_code, err_msg = api.last_error()
                app_logger.error(f"Close order returned None. Last error: {err_msg} (code: {err_code})")
                return False
                
            if result.retcode != api.TRADE_RETCODE_DONE:
                app_logger.error(f"Close order failed. Retcode: {result.retcode}. Comment: {getattr(result, 'comment', 'N/A')}")
                return False
                
            app_logger.info(f"Position ticket {ticket} closed successfully.")
            return True
        except Exception as e:
            app_logger.error(f"Error closing position ticket {ticket}: {e}")
            return False


# Instantiate order manager singleton
order_manager = OrderManager()

"""
Alert Manager Module.
Orchestrates formatting and transmission of notifications for system events and analytics.
"""

from typing import Dict, Any
from app.notifications.telegram_bot import send_telegram_message
from app.utils.logger import app_logger


class AlertManager:
    """
    Coordinates and delivers HTML messages to Telegram and application logs.
    """
    
    @staticmethod
    async def notify_new_trade(trade_data: Dict[str, Any]) -> None:
        """
        Formats and transmits an alert for a newly executed trade.
        """
        ticket = trade_data.get("ticket")
        symbol = trade_data.get("symbol", "XAUUSD")
        order_type = trade_data.get("order_type", "BUY")
        volume = trade_data.get("volume", 0.0)
        entry_price = trade_data.get("entry_price", 0.0)
        sl_price = trade_data.get("sl_price", 0.0)
        tp_price = trade_data.get("tp_price", 0.0)
        ai_conf = trade_data.get("ai_confidence")
        ai_reason = trade_data.get("ai_reasoning", "No AI analysis performed.")

        emoji = "🟢" if order_type.upper() == "BUY" else "🔴"
        
        message = (
            f"<b>{emoji} NEW TRADE EXECUTED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Ticket:</b> #{ticket}\n"
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Direction:</b> {order_type}\n"
            f"<b>Volume:</b> {volume} Lots\n"
            f"<b>Entry Price:</b> {entry_price:.2f}\n"
            f"<b>Stop Loss (SL):</b> {sl_price:.2f}\n"
            f"<b>Take Profit (TP):</b> {tp_price:.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Claude AI Confidence:</b> {f'{ai_conf * 100:.0f}%' if ai_conf is not None else 'Bypassed'}\n"
            f"<b>AI Reasoning:</b> <i>{ai_reason}</i>"
        )
        
        app_logger.info(f"Notification: Trade #{ticket} opened.")
        await send_telegram_message(message)

    @staticmethod
    async def notify_close_trade(trade_data: Dict[str, Any]) -> None:
        """
        Formats and transmits an alert for a closed trade position.
        """
        ticket = trade_data.get("ticket")
        symbol = trade_data.get("symbol", "XAUUSD")
        order_type = trade_data.get("order_type", "BUY")
        volume = trade_data.get("volume", 0.0)
        entry_price = trade_data.get("entry_price", 0.0)
        exit_price = trade_data.get("exit_price", 0.0)
        profit = trade_data.get("profit", 0.0)
        comment = trade_data.get("comment", "")

        emoji = "💰" if profit >= 0 else "📉"
        profit_sign = "+" if profit >= 0 else ""
        
        message = (
            f"<b>{emoji} TRADE CLOSED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Ticket:</b> #{ticket}\n"
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Direction:</b> {order_type}\n"
            f"<b>Volume:</b> {volume} Lots\n"
            f"<b>Entry Price:</b> {entry_price:.2f}\n"
            f"<b>Exit Price:</b> {exit_price:.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>PnL:</b> <code style='color:green'>{profit_sign}{profit:.2f} USD</code>\n"
            f"<b>Comment:</b> {comment}"
        )
        
        app_logger.info(f"Notification: Trade #{ticket} closed. Profit: {profit:.2f} USD")
        await send_telegram_message(message)

    @staticmethod
    async def notify_drawdown_warning(reason: str) -> None:
        """
        Delivers an emergency warning regarding account drawdown breaches.
        """
        message = (
            f"<b>⚠️ DRAWDOWN PROTECTION ALERT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Alert:</b> Trading deactivated due to drawdown limit.\n"
            f"<b>Details:</b> <i>{reason}</i>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Manual verification of current account equity recommended.</i>"
        )
        app_logger.error(f"Notification: Drawdown warning! {reason}")
        await send_telegram_message(message)

    @staticmethod
    async def notify_performance_report(stats: Dict[str, Any], type_report: str = "Daily") -> None:
        """
        Formats and transmits a performance summary report (Daily/Weekly).
        """
        days = stats.get("period_days", 30)
        total_trades = stats.get("total_trades", 0)
        win_rate = stats.get("win_rate_pct", 0.0)
        net_profit = stats.get("net_profit", 0.0)
        profit_factor = stats.get("profit_factor", 0.0)
        avg_win = stats.get("avg_win", 0.0)
        avg_loss = stats.get("avg_loss", 0.0)
        wins = stats.get("wins", 0)
        losses = stats.get("losses", 0)

        trend_emoji = "📈" if net_profit >= 0 else "📉"
        profit_sign = "+" if net_profit >= 0 else ""

        message = (
            f"<b>📊 {type_report.upper()} PERFORMANCE REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Period scanned:</b> Past {days} days\n"
            f"<b>Total trades executed:</b> {total_trades}\n"
            f"<b>Wins/Losses:</b> {wins} / {losses}\n"
            f"<b>Win Rate:</b> {win_rate:.1f}%\n"
            f"<b>Profit Factor:</b> {profit_factor:.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Average Win:</b> ${avg_win:.2f}\n"
            f"<b>Average Loss:</b> ${avg_loss:.2f}\n"
            f"<b>Net PnL:</b> <b>{profit_sign}${net_profit:,.2f} USD</b> {trend_emoji}\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        
        app_logger.info(f"Notification: Transmitted {type_report} performance report.")
        await send_telegram_message(message)

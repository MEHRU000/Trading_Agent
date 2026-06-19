"""
Signal Processor Module.
Orchestrates the entire trade lifecycle: receives alerts, calculates indicators,
applies risk metrics, validates using Claude AI, and triggers execution.
"""

import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.broker.mt5_connector import mt5_connector
from app.broker.order_manager import order_manager
from app.broker.position_manager import position_manager
from app.database.trade_history import create_signal, create_trade, update_trade_by_ticket
from app.strategy.xauusd_strategy import evaluate_strategy
from app.risk.risk_manager import risk_manager
from app.risk.lot_calculator import calculate_lot_size
from app.ai.market_reasoning import build_analysis_prompt
from app.ai.claude_analyzer import validate_trade_with_ai
from app.notifications.alert_manager import AlertManager
from app.utils.config import settings
from app.utils.logger import app_logger


async def process_incoming_signal(db: Session, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coordinates the validation and execution workflow for an incoming TradingView signal.
    """
    app_logger.info(f"Ingested new payload from TradingView: {json.dumps(raw_payload)}")
    
    # 1. Parse and record initial signal
    symbol = raw_payload.get("symbol", "XAUUSD").upper()
    direction = raw_payload.get("direction", "").upper()
    timeframe = raw_payload.get("timeframe", "H1").upper()
    price_alert = float(raw_payload.get("price", 0.0))

    if direction not in ["BUY", "SELL"]:
        msg = f"Invalid direction '{direction}' received. Signal discarded."
        app_logger.error(msg)
        return {"status": "REJECTED", "reason": msg}

    signal_db_entry = {
        "symbol": symbol,
        "direction": direction,
        "timeframe": timeframe,
        "price": price_alert,
        "raw_payload": json.dumps(raw_payload),
        "action_taken": "PENDING"
    }
    
    signal_record = create_signal(db, signal_db_entry)

    # 2. Fetch Candlesticks from Broker to verify indicators locally
    candles = mt5_connector.get_candles(symbol, timeframe, count=100)
    if candles is None or len(candles) == 0:
        reason = "Failed to copy rates from broker terminal."
        signal_record.action_taken = "ERROR"
        signal_record.reason = reason
        signal_record.processed = True
        db.commit()
        return {"status": "ERROR", "reason": reason}

    # 3. Calculate indicators and evaluate technical strategy confluence
    strategy_result = evaluate_strategy(candles)
    metrics = strategy_result["metrics"]
    
    # Update signal record with calculated indicators
    signal_record.rsi = metrics.get("rsi")
    signal_record.ema_20 = metrics.get("ema_20")
    signal_record.ema_50 = metrics.get("ema_50")
    signal_record.atr = metrics.get("atr")
    signal_record.volume = metrics.get("volume")
    signal_record.avg_volume = metrics.get("avg_volume")
    signal_record.market_structure = metrics.get("market_structure")
    db.commit()

    strategy_signal = strategy_result["signal"]
    entry_price = strategy_result["entry_price"]
    sl_price = strategy_result["sl_price"]
    tp_price = strategy_result["tp_price"]

    # 4. Check if strategy indicators match the alert direction
    if strategy_signal != direction:
        reason = f"Confluence check failed. Alert is {direction}, but technical indicators generated: {strategy_signal}."
        app_logger.warning(reason)
        signal_record.action_taken = "REJECTED_INDICATORS"
        signal_record.reason = reason
        signal_record.processed = True
        db.commit()
        return {"status": "REJECTED", "reason": reason}

    # 5. Risk Management Verification
    risk_approved, risk_reason = risk_manager.validate_trade_setup(db, symbol, entry_price, sl_price)
    if not risk_approved:
        signal_record.action_taken = "REJECTED_RISK"
        signal_record.reason = risk_reason
        signal_record.processed = True
        db.commit()
        return {"status": "REJECTED", "reason": risk_reason}

    # 6. Claude AI Confluence Verification
    ai_validation = True
    ai_confidence = 1.0
    ai_reason = "AI Validation Disabled."
    
    if settings.AI_VALIDATION_ENABLED:
        balance, equity, _, _ = mt5_connector.get_account_state()
        prompt = build_analysis_prompt(
            symbol, direction, entry_price, sl_price, tp_price, metrics, balance, equity
        )
        ai_result = validate_trade_with_ai(prompt)
        ai_validation = ai_result["validation"]
        ai_confidence = ai_result["confidence_score"]
        ai_reason = ai_result["reasoning"]

        if not ai_validation or ai_confidence < settings.MIN_CONFIDENCE_SCORE:
            reason = f"Claude validation rejected setup (Conf: {ai_confidence:.2f} < Min: {settings.MIN_CONFIDENCE_SCORE:.2f}). Reason: {ai_reason}"
            app_logger.warning(reason)
            signal_record.action_taken = "REJECTED_AI"
            signal_record.reason = reason
            signal_record.processed = True
            db.commit()
            return {"status": "REJECTED", "reason": reason}

    # 7. Calculate lot size using 1% risk rule
    balance, _, _, _ = mt5_connector.get_account_state()
    lot_size = calculate_lot_size(balance, entry_price, sl_price, symbol)

    if lot_size <= 0.0:
        reason = "Lot size calculation returned 0.0. Execution cancelled."
        app_logger.error(reason)
        signal_record.action_taken = "REJECTED_RISK"
        signal_record.reason = reason
        signal_record.processed = True
        db.commit()
        return {"status": "REJECTED", "reason": reason}

    # 8. Order routing execution via MT5
    comment = f"AI Validated (Conf: {ai_confidence * 100:.0f}%)" if settings.AI_VALIDATION_ENABLED else "Agent Executed"
    
    execution_result = order_manager.send_market_order(
        symbol=symbol,
        order_type=direction,
        volume=lot_size,
        sl=sl_price,
        tp=tp_price,
        comment=comment
    )

    if execution_result["status"] == "SUCCESS":
        ticket = execution_result["ticket"]
        exec_price = execution_result["price"]
        
        # Log successful trade to database
        trade_db_entry = {
            "ticket": ticket,
            "symbol": symbol,
            "order_type": direction,
            "volume": lot_size,
            "entry_price": exec_price,
            "sl_price": sl_price,
            "tp_price": tp_price,
            "status": "OPEN",
            "magic_number": settings.MT5_MAGIC_NUMBER,
            "comment": comment,
            "ai_confidence": ai_confidence if settings.AI_VALIDATION_ENABLED else None,
            "ai_validation_reasoning": ai_reason if settings.AI_VALIDATION_ENABLED else None
        }
        create_trade(db, trade_db_entry)
        
        # Update signal
        signal_record.action_taken = "EXECUTED"
        signal_record.processed = True
        db.commit()

        # Send Telegram Bot Alerts
        notification_data = {
            "ticket": ticket,
            "symbol": symbol,
            "order_type": direction,
            "volume": lot_size,
            "entry_price": exec_price,
            "sl_price": sl_price,
            "tp_price": tp_price,
            "ai_confidence": ai_confidence if settings.AI_VALIDATION_ENABLED else None,
            "ai_reasoning": ai_reason if settings.AI_VALIDATION_ENABLED else None
        }
        
        # Non-blocking background notification task
        try:
            await AlertManager.notify_new_trade(notification_data)
        except Exception as telegram_err:
            app_logger.error(f"Failed to post Telegram notification: {telegram_err}")

        return {"status": "EXECUTED", "ticket": ticket, "price": exec_price}
    else:
        # Broker execution failure
        error_reason = execution_result.get("error", "Broker execution failed.")
        signal_record.action_taken = "ERROR"
        signal_record.reason = error_reason
        signal_record.processed = True
        db.commit()
        return {"status": "FAILED", "reason": error_reason}

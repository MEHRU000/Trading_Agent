"""
CRUD and Analysis utilities for Trade History, Signals, and Account snapshots.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import Trade, Signal, AccountSnapshot
from app.utils.logger import app_logger
from app.utils.helpers import get_utc_now


# --- SIGNAL SERVICES ---

def create_signal(db: Session, signal_data: Dict[str, Any]) -> Signal:
    """
    Persists an incoming TradingView signal.
    """
    try:
        signal = Signal(**signal_data)
        db.add(signal)
        db.commit()
        db.refresh(signal)
        return signal
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to record signal: {e}")
        raise e


# --- TRADE SERVICES ---

def create_trade(db: Session, trade_data: Dict[str, Any]) -> Trade:
    """
    Logs a new trade execution entry.
    """
    try:
        trade = Trade(**trade_data)
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return trade
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to log trade: {e}")
        raise e


def get_open_trades(db: Session) -> List[Trade]:
    """
    Retrieves all currently active trades.
    """
    return db.query(Trade).filter(Trade.status == "OPEN").all()


def update_trade_by_ticket(db: Session, ticket: int, updates: Dict[str, Any]) -> Optional[Trade]:
    """
    Updates trade fields by MT5 ticket ID.
    """
    try:
        trade = db.query(Trade).filter(Trade.ticket == ticket).first()
        if not trade:
            app_logger.warning(f"Trade record with ticket {ticket} not found in database.")
            return None
        
        for key, value in updates.items():
            setattr(trade, key, value)
            
        if "status" in updates and updates["status"] == "CLOSED":
            trade.closed_at = get_utc_now()

        db.commit()
        db.refresh(trade)
        return trade
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to update trade for ticket {ticket}: {e}")
        return None


def get_daily_trade_count(db: Session) -> int:
    """
    Returns the number of trades executed today (since midnight UTC).
    """
    now = get_utc_now()
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
    
    return db.query(Trade).filter(
        Trade.created_at >= start_of_day,
        Trade.status != "FAILED"
    ).count()


def get_daily_pnl(db: Session) -> float:
    """
    Returns the total closed PnL for trades closed today (since midnight UTC).
    """
    now = get_utc_now()
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
    
    trades = db.query(Trade).filter(
        Trade.status == "CLOSED",
        Trade.closed_at >= start_of_day
    ).all()
    
    total_pnl = sum(t.profit for t in trades) if trades else 0.0
    return round(total_pnl, 2)


# --- ACCOUNT SNAPSHOT SERVICES ---

def create_account_snapshot(db: Session, balance: float, equity: float, margin: float = 0.0, free_margin: float = 0.0) -> AccountSnapshot:
    """
    Creates an account balance snapshot and calculates current drawdown thresholds.
    """
    try:
        # Fetch peak balance in the past day (for daily drawdown)
        now = get_utc_now()
        one_day_ago = now - timedelta(days=1)
        one_week_ago = now - timedelta(days=7)

        # Get peak balance for daily drawdown calculation
        daily_peak = db.query(func.max(AccountSnapshot.balance)).filter(
            AccountSnapshot.timestamp >= one_day_ago
        ).scalar() or balance

        # Get peak balance for weekly drawdown calculation
        weekly_peak = db.query(func.max(AccountSnapshot.balance)).filter(
            AccountSnapshot.timestamp >= one_week_ago
        ).scalar() or balance

        # Compute drawdown %
        daily_dd = (daily_peak - equity) / daily_peak if daily_peak > 0 else 0.0
        weekly_dd = (weekly_peak - equity) / weekly_peak if weekly_peak > 0 else 0.0

        snapshot = AccountSnapshot(
            balance=balance,
            equity=equity,
            margin=margin,
            free_margin=free_margin,
            daily_drawdown=max(0.0, daily_dd),
            weekly_drawdown=max(0.0, weekly_dd),
            timestamp=now
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return snapshot
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to record account snapshot: {e}")
        raise e


def get_latest_snapshot(db: Session) -> Optional[AccountSnapshot]:
    """
    Returns the most recent account snapshot.
    """
    return db.query(AccountSnapshot).order_by(AccountSnapshot.timestamp.desc()).first()


# --- PERFORMANCE ANALYTICS SERVICES ---

def get_performance_stats(db: Session, days: int = 365) -> Dict[str, Any]:
    """
    Calculates key performance metrics for closed trades over a specific time range.
    
    Metrics:
        - Win Rate %
        - Profit Factor
        - Total Trades
        - Net Profit / Loss
        - Average Win / Average Loss
    """
    start_date = get_utc_now() - timedelta(days=days)
    
    trades = db.query(Trade).filter(
        Trade.status == "CLOSED",
        Trade.created_at >= start_date
    ).all()
    
    total_trades = len(trades)
    if total_trades == 0:
        return {
            "period_days": days,
            "total_trades": 0,
            "win_rate_pct": 0.0,
            "profit_factor": 0.0,
            "net_profit": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "wins": 0,
            "losses": 0
        }
        
    wins = []
    losses = []
    
    for t in trades:
        net_pnl = t.profit + (t.swap or 0.0) + (t.commission or 0.0)
        if net_pnl > 0:
            wins.append(net_pnl)
        else:
            losses.append(net_pnl)
        
    win_count = len(wins)
    loss_count = len(losses)
    
    total_win_amt = sum(wins)
    total_loss_amt = abs(sum(losses))
    
    net_profit = total_win_amt - total_loss_amt
    win_rate = (win_count / total_trades) * 100.0
    
    profit_factor = total_win_amt / total_loss_amt if total_loss_amt > 0 else (total_win_amt if total_win_amt > 0 else 1.0)
    
    avg_win = total_win_amt / win_count if win_count > 0 else 0.0
    avg_loss = total_loss_amt / loss_count if loss_count > 0 else 0.0
    
    return {
        "period_days": days,
        "total_trades": total_trades,
        "win_rate_pct": round(win_rate, 2),
        "profit_factor": round(profit_factor, 2),
        "net_profit": round(net_profit, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "wins": win_count,
        "losses": loss_count
    }


# --- LIVE MT5 SYNCHRONIZATION SERVICES ---

def sync_trades_from_mt5(db: Session, days: int = 365):
    """
    Pulls historical deals from MT5 for the last N days,
    groups them by position_id, and synchronizes them into the local trades database.
    Also synchronizes current active open positions.
    """
    from datetime import datetime, timedelta
    from app.broker.mt5_connector import mt5_connector
    from app.utils.config import settings

    now = datetime.utcnow()
    date_from = now - timedelta(days=days)
    date_to = now + timedelta(days=1)  # Add 1 day buffer for broker terminal timezone differences
    
    api = mt5_connector.api
    
    # Retrieve history deals
    if mt5_connector.is_mock:
        deals = api.history_deals_get(date_from=date_from, date_to=date_to)
    else:
        if not api.terminal_info():
            app_logger.warning("MT5 terminal is not connected. Skipping historical deals query.")
            deals = []
        else:
            deals = api.history_deals_get(date_from, date_to)
        
    if not deals:
        err_msg = ""
        try:
            if hasattr(api, "last_error"):
                err_msg = f" Error: {api.last_error()}"
        except Exception:
            pass
        app_logger.warning(f"No historical deals retrieved from MT5.{err_msg}")
    else:
        # Group deals by position_id
        deals_by_pos = {}
        for deal in deals:
            pos_id = getattr(deal, "position_id", None)
            if pos_id is not None:
                if pos_id not in deals_by_pos:
                    deals_by_pos[pos_id] = []
                deals_by_pos[pos_id].append(deal)
                
        # Group entries and exits
        for pos_id, pos_deals in deals_by_pos.items():
            entry_deals = [d for d in pos_deals if getattr(d, "entry", None) == 0]
            exit_deals = [d for d in pos_deals if getattr(d, "entry", None) == 1]
            
            # If there are exit deals, the position was at least partially closed
            if exit_deals:
                existing_trade = db.query(Trade).filter(Trade.ticket == pos_id).first()
                
                main_entry = entry_deals[0] if entry_deals else pos_deals[0]
                main_exit = exit_deals[-1]  # Latest exit deal
                
                order_type = "BUY" if main_entry.type == 0 else "SELL"
                
                # Aggregate entry volume & price
                total_entry_vol = sum(d.volume for d in entry_deals) if entry_deals else main_entry.volume
                if entry_deals and total_entry_vol > 0:
                    entry_price = sum(d.price * d.volume for d in entry_deals) / total_entry_vol
                else:
                    entry_price = main_entry.price
                
                # Aggregate exit volume & price
                total_exit_vol = sum(d.volume for d in exit_deals)
                if total_exit_vol > 0:
                    exit_price = sum(d.price * d.volume for d in exit_deals) / total_exit_vol
                else:
                    exit_price = main_exit.price
                    
                # Aggregate metrics over all deals in position
                profit = sum(getattr(d, "profit", 0.0) for d in pos_deals)
                swap = sum(getattr(d, "swap", 0.0) for d in pos_deals)
                commission = sum(getattr(d, "commission", 0.0) for d in pos_deals)
                
                magic = getattr(main_entry, "magic", settings.MT5_MAGIC_NUMBER)
                raw_comment = getattr(main_exit, "comment", "") or getattr(main_entry, "comment", "")
                comment = raw_comment
                if isinstance(raw_comment, str) and raw_comment:
                    comment_lower = raw_comment.lower()
                    if "sl" in comment_lower or "stop" in comment_lower:
                        comment = "Stop Loss Hit 🔴"
                    elif "tp" in comment_lower or "profit" in comment_lower:
                        comment = "Take Profit Hit 🟢"
                    elif "manual" in comment_lower or "close" in comment_lower:
                        comment = "Manual Close 🔴"
                
                sl_p = getattr(main_entry, "sl", getattr(main_exit, "sl", 0.0))
                tp_p = getattr(main_entry, "tp", getattr(main_exit, "tp", 0.0))
                
                if not comment or comment == raw_comment:
                    is_sl = abs(exit_price - sl_p) < 0.02 if sl_p > 0 else False
                    is_tp = abs(exit_price - tp_p) < 0.02 if tp_p > 0 else False
                    if is_sl:
                        comment = "Stop Loss Hit 🔴"
                    elif is_tp:
                        comment = "Take Profit Hit 🟢"
                    else:
                        comment = "Manual Close 🔴" if not comment else comment

                created_at = datetime.utcfromtimestamp(main_entry.time)
                closed_at = datetime.utcfromtimestamp(main_exit.time)
                
                trade_data = {
                    "ticket": pos_id,
                    "symbol": main_entry.symbol,
                    "order_type": order_type,
                    "volume": round(total_entry_vol, 2),
                    "entry_price": round(entry_price, 2),
                    "sl_price": sl_p,
                    "tp_price": tp_p,
                    "exit_price": round(exit_price, 2),
                    "profit": round(profit, 2),
                    "swap": round(swap, 2),
                    "commission": round(commission, 2),
                    "status": "CLOSED",
                    "magic_number": magic,
                    "comment": comment,
                    "created_at": created_at,
                    "closed_at": closed_at
                }
                
                if existing_trade:
                    for key, val in trade_data.items():
                        setattr(existing_trade, key, val)
                else:
                    new_trade = Trade(**trade_data)
                    db.add(new_trade)
                    
        db.commit()
        app_logger.info(f"Synchronized closed trades from MT5. Total positions: {len(deals_by_pos)}")

    # Retrieve current active open positions
    try:
        mt5_positions = api.positions_get()
        active_tickets = set()
        if mt5_positions:
            for pos in mt5_positions:
                active_tickets.add(pos.ticket)
                existing_trade = db.query(Trade).filter(Trade.ticket == pos.ticket).first()
                order_type = "BUY" if pos.type == 0 else "SELL"
                
                trade_data = {
                    "ticket": pos.ticket,
                    "symbol": pos.symbol,
                    "order_type": order_type,
                    "volume": pos.volume,
                    "entry_price": pos.price_open,
                    "sl_price": getattr(pos, "sl", 0.0),
                    "tp_price": getattr(pos, "tp", 0.0),
                    "exit_price": None,
                    "status": "OPEN",
                    "magic_number": getattr(pos, "magic", settings.MT5_MAGIC_NUMBER),
                    "comment": getattr(pos, "comment", ""),
                    "created_at": datetime.utcfromtimestamp(pos.time),
                    "profit": round(pos.profit, 2),
                    "swap": round(getattr(pos, "swap", 0.0), 2),
                    "commission": round(getattr(pos, "commission", 0.0), 2)
                }
                
                if existing_trade:
                    for key, val in trade_data.items():
                        setattr(existing_trade, key, val)
                else:
                    new_trade = Trade(**trade_data)
                    db.add(new_trade)
                    
            db.commit()
            app_logger.info(f"Synchronized open positions from MT5. Total active: {len(mt5_positions)}")
        else:
            app_logger.info("No active open positions returned from MT5.")

        # Clean up stale open trades in local DB that are no longer active in MT5
        db_open_trades = db.query(Trade).filter(Trade.status == "OPEN").all()
        for t in db_open_trades:
            if t.ticket and t.ticket not in active_tickets:
                app_logger.info(f"Syncing closed/stale trade from MT5 for ticket {t.ticket}")
                pos_deals = api.history_deals_get(position=t.ticket)
                if pos_deals:
                    exit_deals = [d for d in pos_deals if getattr(d, "entry", None) == 1]
                    main_exit = exit_deals[-1] if exit_deals else pos_deals[-1]
                    entry_deals = [d for d in pos_deals if getattr(d, "entry", None) == 0]
                    main_entry = entry_deals[0] if entry_deals else pos_deals[0]
                    
                    total_exit_vol = sum(d.volume for d in exit_deals) if exit_deals else main_exit.volume
                    exit_price = (sum(d.price * d.volume for d in exit_deals) / total_exit_vol) if (exit_deals and total_exit_vol > 0) else main_exit.price
                    
                    profit = sum(getattr(d, "profit", 0.0) for d in pos_deals)
                    swap = sum(getattr(d, "swap", 0.0) for d in pos_deals)
                    commission = sum(getattr(d, "commission", 0.0) for d in pos_deals)
                    
                    raw_comment = getattr(main_exit, "comment", "") or getattr(main_entry, "comment", "")
                    comment = raw_comment
                    sl_p = getattr(main_entry, "sl", getattr(main_exit, "sl", 0.0))
                    tp_p = getattr(main_entry, "tp", getattr(main_exit, "tp", 0.0))
                    
                    if isinstance(raw_comment, str) and raw_comment:
                        comment_lower = raw_comment.lower()
                        if "sl" in comment_lower or "stop" in comment_lower:
                            comment = "Stop Loss Hit 🔴"
                        elif "tp" in comment_lower or "profit" in comment_lower:
                            comment = "Take Profit Hit 🟢"
                        elif "manual" in comment_lower or "close" in comment_lower:
                            comment = "Manual Close 🔴"
                            
                    if not comment or comment == raw_comment:
                        is_sl = abs(exit_price - sl_p) < 0.02 if sl_p > 0 else False
                        is_tp = abs(exit_price - tp_p) < 0.02 if tp_p > 0 else False
                        if is_sl:
                            comment = "Stop Loss Hit 🔴"
                        elif is_tp:
                            comment = "Take Profit Hit 🟢"
                        else:
                            comment = "Manual Close 🔴"
                    
                    t.status = "CLOSED"
                    t.exit_price = round(exit_price, 2)
                    t.profit = round(profit, 2)
                    t.swap = round(swap, 2)
                    t.commission = round(commission, 2)
                    t.comment = comment
                    t.closed_at = datetime.utcfromtimestamp(main_exit.time)
                else:
                    # If we couldn't find any history deals, let's mark it CLOSED as fallback (e.g. manually closed in terminal)
                    t.status = "CLOSED"
                    t.closed_at = datetime.utcnow()
                    t.comment = "Closed (Untracked)"
        db.commit()
    except Exception as e:
        app_logger.error(f"Failed to synchronize open positions from MT5: {e}")


def get_all_trades_json(db: Session) -> list:
    """
    Returns all logged trades serialized as a JSON-serializable list.
    """
    trades = db.query(Trade).order_by(Trade.created_at.desc()).all()
    results = []
    for t in trades:
        results.append({
            "ticket": t.ticket,
            "symbol": t.symbol,
            "order_type": t.order_type,
            "volume": t.volume,
            "entry_price": t.entry_price,
            "sl_price": t.sl_price,
            "tp_price": t.tp_price,
            "exit_price": t.exit_price,
            "profit": t.profit,
            "status": t.status,
            "comment": t.comment,
            "created_at": t.created_at.isoformat() + "Z" if t.created_at else None,
            "closed_at": t.closed_at.isoformat() + "Z" if t.closed_at else None
        })
    return results

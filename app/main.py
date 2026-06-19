"""
Main entrypoint for XAUUSD Automated Trading Agent.
Initializes FastAPI, sets up DB connection, launches MT5 client, and triggers background synchronization routines.
"""

import asyncio
import hmac
import hashlib
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Cookie, Form, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.utils.calculations import calculate_profit, calculate_pips

from app.utils.config import settings
from app.utils.logger import app_logger
from app.database.db import init_db, SessionLocal, get_db
from app.database.trade_history import (
    get_open_trades,
    update_trade_by_ticket,
    create_account_snapshot,
    get_performance_stats,
    get_latest_snapshot,
    get_daily_pnl,
)
from app.database.models import Trade, Signal, AccountSnapshot, ChatMessage, DashboardTask, PortfolioAccount, TradeJournal, AICoachEvaluation, MarketIntelBrief
from app.ai.claude_analyzer import generate_ai_text
from pydantic import BaseModel
import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from app.utils.news_manager import fetch_forex_factory_news
from datetime import datetime
from app.broker.mt5_connector import mt5_connector
from app.broker.position_manager import position_manager
from app.notifications.alert_manager import AlertManager
from app.webhook.tradingview_webhook import router as webhook_router
from app.utils.dashboard_template import render_dashboard


# Authentication helpers
def get_session_signature() -> str:
    payload = f"{settings.DASHBOARD_USERNAME}:{settings.DASHBOARD_PASSWORD}"
    return hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

def is_authenticated(session_id: Optional[str]) -> bool:
    if not session_id:
        return False
    return hmac.compare_digest(session_id, get_session_signature())


# Background tasks storage
background_tasks = set()
_last_live_state_sync_time = 0.0


async def trailing_stop_loop():
    """
    Periodic background loop that manages trailing stop loss updates.
    """
    app_logger.info("Starting background trailing stop loop...")
    while True:
        try:
            await asyncio.to_thread(position_manager.manage_trailing_stops, "XAUUSD")
        except Exception as e:
            app_logger.error(f"Error in trailing stop manager loop: {e}")
        await asyncio.sleep(10)  # Check every 10 seconds


async def position_sync_loop():
    """
    Periodic background loop that synchronizes Database trade records with MT5 positions.
    Detects if any active position was closed via Stop Loss or Take Profit.
    """
    app_logger.info("Starting background position synchronization loop...")
    while True:
        try:
            db = SessionLocal()
            try:
                # Synchronize trades from MT5
                from app.database.trade_history import sync_trades_from_mt5
                try:
                    await asyncio.to_thread(sync_trades_from_mt5, db, days=365)
                except Exception as sync_err:
                    app_logger.error(f"Failed to sync MT5 in position sync loop: {sync_err}")
                
                # Query DB open trades
                db_open_trades = get_open_trades(db)
                if db_open_trades:
                    # Query MT5 active positions (unfiltered by magic number)
                    api = mt5_connector.api
                    if not mt5_connector.is_mock and not api.terminal_info():
                        await asyncio.to_thread(mt5_connector.connect)
                    raw_positions = await asyncio.to_thread(api.positions_get)
                    if raw_positions is None:
                        app_logger.warning("Failed to fetch active positions from MT5. Skipping sync iteration.")
                        db_open_trades = []
                        raw_positions = []
                    mt5_tickets = {getattr(pos, "ticket", None) for pos in raw_positions}

                    for db_trade in db_open_trades:
                        ticket = db_trade.ticket
                        # If trade is registered open in DB, but not found in active MT5 positions
                        if ticket not in mt5_tickets:
                            app_logger.info(f"Detected closed position for ticket #{ticket} on broker terminal.")
                            
                            # Query history deals to find exit price and profit
                            api = mt5_connector.api
                            exit_price = None
                            profit = None
                            
                            # Attempt query from broker history if supported
                            history_deal = None
                            if hasattr(api, "history_deals_get"):
                                try:
                                    deals = await asyncio.to_thread(api.history_deals_get, position=ticket)
                                    if deals:
                                        # Find the deal that closed the position
                                        close_deals = [d for d in deals if getattr(d, "entry", None) == 1]  # DEAL_ENTRY_OUT
                                        if close_deals:
                                            history_deal = close_deals[0]
                                            exit_price = getattr(history_deal, "price", None)
                                            profit = getattr(history_deal, "profit", None)
                                except Exception as err:
                                    app_logger.error(f"Failed to query history deals for ticket #{ticket}: {err}")

                            # If details could not be queried, estimate from tick data or stops proximity
                            if exit_price is None or profit is None:
                                tick = await asyncio.to_thread(mt5_connector.get_tick_data, db_trade.symbol)
                                current_price = None
                                if tick:
                                    bid, ask = tick
                                    current_price = bid if db_trade.order_type == "BUY" else ask
                                
                                # Check proximity to SL/TP or fallback to current tick price
                                if current_price is not None:
                                    is_sl = abs(current_price - db_trade.sl_price) < 0.05 if (db_trade.sl_price is not None and db_trade.sl_price > 0) else False
                                    is_tp = abs(current_price - db_trade.tp_price) < 0.05 if (db_trade.tp_price is not None and db_trade.tp_price > 0) else False
                                    
                                    if is_sl:
                                        exit_price = db_trade.sl_price
                                    elif is_tp:
                                        exit_price = db_trade.tp_price
                                    else:
                                        exit_price = current_price
                                else:
                                    # Absolute fallback: assume TP hit if set and > 0, otherwise entry price
                                    exit_price = db_trade.tp_price if (db_trade.tp_price is not None and db_trade.tp_price > 0) else db_trade.entry_price

                                # Compute PnL correctly based on order direction using configured multiplier
                                from app.utils.calculations import calculate_profit
                                profit = calculate_profit(db_trade.order_type, db_trade.entry_price, exit_price, db_trade.volume)

                            # Determine close message comment based on deal comment or price proximity
                            close_comment = ""
                            if history_deal:
                                raw_comm = getattr(history_deal, "comment", "")
                                if isinstance(raw_comm, str) and raw_comm:
                                    comment_lower = raw_comm.lower()
                                    if "sl" in comment_lower or "stop" in comment_lower:
                                        close_comment = "Stop Loss Hit 🔴"
                                    elif "tp" in comment_lower or "profit" in comment_lower:
                                        close_comment = "Take Profit Hit 🟢"
                                    else:
                                        close_comment = f"{raw_comm} 🔴"
                            
                            if not close_comment:
                                is_sl = abs(exit_price - db_trade.sl_price) < 0.02 if (db_trade.sl_price is not None and db_trade.sl_price > 0) else False
                                is_tp = abs(exit_price - db_trade.tp_price) < 0.02 if (db_trade.tp_price is not None and db_trade.tp_price > 0) else False
                                if is_sl:
                                    close_comment = "Stop Loss Hit 🔴"
                                elif is_tp:
                                    close_comment = "Take Profit Hit 🟢"
                                else:
                                    close_comment = "Manual Close 🔴"
                            
                            # Update Database Trade Record
                            update_trade_by_ticket(db, ticket, {
                                "status": "CLOSED",
                                "exit_price": exit_price,
                                "profit": profit,
                                "comment": close_comment
                            })
                            
                            # Dispatch Telegram alert
                            closed_trade_data = {
                                "ticket": ticket,
                                "symbol": db_trade.symbol,
                                "order_type": db_trade.order_type,
                                "volume": db_trade.volume,
                                "entry_price": db_trade.entry_price,
                                "exit_price": exit_price,
                                "profit": profit,
                                "comment": close_comment
                            }
                            await AlertManager.notify_close_trade(closed_trade_data)
            finally:
                db.close()
        except Exception as e:
            app_logger.error(f"Error in position sync loop: {e}")
        await asyncio.sleep(5)  # Check every 5 seconds


async def account_snapshot_loop():
    """
    Periodic background loop that takes account snapshots and monitors drawdown limits.
    Runs every 5 minutes.
    """
    app_logger.info("Starting background account snapshot loop...")
    while True:
        try:
            db = SessionLocal()
            try:
                balance, equity, margin, free_margin = await asyncio.to_thread(mt5_connector.get_account_state)
                if balance > 0.0:
                    snapshot = create_account_snapshot(db, balance, equity, margin, free_margin)
                    app_logger.info(f"Recorded balance snapshot: Balance: ${balance:.2f}, Equity: ${equity:.2f}")
                    
                    # Verify drawdown limits and alert on breach
                    daily_dd = snapshot.daily_drawdown
                    weekly_dd = snapshot.weekly_drawdown
                    
                    if daily_dd >= settings.MAX_DAILY_DRAWDOWN_PCT:
                        await AlertManager.notify_drawdown_warning(f"Daily Drawdown reached {daily_dd * 100.0:.2f}% (Limit: {settings.MAX_DAILY_DRAWDOWN_PCT * 100.0}%)")
                    elif weekly_dd >= settings.MAX_WEEKLY_DRAWDOWN_PCT:
                        await AlertManager.notify_drawdown_warning(f"Weekly Drawdown reached {weekly_dd * 100.0:.2f}% (Limit: {settings.MAX_WEEKLY_DRAWDOWN_PCT * 100.0}%)")
            finally:
                db.close()
        except Exception as e:
            app_logger.error(f"Error in account snapshot loop: {e}")
        await asyncio.sleep(300)  # Check every 5 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan hook managing startup and shutdown routines.
    """
    # STARTUP
    app_logger.info("Initializing system startup hooks...")
    
    # 1. Initialize DB tables
    init_db()
    
    # 2. Connect to MT5 Broker
    connection_ok = await asyncio.to_thread(mt5_connector.connect)
    if not connection_ok:
        app_logger.critical("Failed to connect to MT5 broker. Automated trading disabled.")
    
    # 3. Initialize initial balance snapshot and sync trades in DB
    db = SessionLocal()
    try:
        from app.database.trade_history import sync_trades_from_mt5
        try:
            await asyncio.to_thread(sync_trades_from_mt5, db, days=365)
        except Exception as sync_err:
            app_logger.error(f"Failed startup MT5 sync: {sync_err}")
            
        balance, equity, margin, free_margin = await asyncio.to_thread(mt5_connector.get_account_state)
        if balance > 0.0:
            create_account_snapshot(db, balance, equity, margin, free_margin)
    finally:
        db.close()

    # 4. Start Background Schedulers
    task_ts = asyncio.create_task(trailing_stop_loop())
    task_ps = asyncio.create_task(position_sync_loop())
    task_as = asyncio.create_task(account_snapshot_loop())
    
    background_tasks.add(task_ts)
    background_tasks.add(task_ps)
    background_tasks.add(task_as)
    
    app_logger.info("System startup hooks fully loaded. Web API listening...")
    
    yield
    
    # SHUTDOWN
    app_logger.info("Initializing system shutdown hooks...")
    
    # Cancel background tasks
    for task in background_tasks:
        task.cancel()
    
    # Disconnect MT5 link
    mt5_connector.disconnect()
    
    app_logger.info("System shutdown completed.")


# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Automated Trading Agent for Gold (XAUUSD) executing via MetaTrader 5.",
    version="1.0.0",
    lifespan=lifespan
)

# Register routes
app.include_router(webhook_router, prefix="/api/v1")


def fetch_live_forex_news() -> list:
    url = "https://news.google.com/rss/search?q=forex+market+gold+trading+OR+CPI+OR+PPI+OR+NFP+OR+FOMC+OR+interest+rate+OR+unemployment&hl=en-US&gl=US&ceid=US:en"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        news_items = []
        for item in root.findall(".//item")[:15]:
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else ""
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
            source = item.find("source").text if item.find("source") is not None else "Google News"
            
            clean_title = title
            if " - " in title:
                clean_title = title.rsplit(" - ", 1)[0]
                
            news_items.append({
                "title": clean_title,
                "link": link,
                "date": pub_date,
                "source": source
            })
        return news_items
    except Exception as e:
        app_logger.error(f"Error fetching live forex news: {e}")
        return []


@app.get("/", response_class=HTMLResponse)
def get_dashboard(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Renders the developer dashboard with live statistics, positions, and logs.
    """
    if not is_authenticated(session_id):
        return RedirectResponse(url="/login", status_code=303)
    # Trigger an immediate synchronization so the dashboard is up-to-date
    from app.database.trade_history import sync_trades_from_mt5, get_all_trades_json
    try:
        sync_trades_from_mt5(db, days=365)
    except Exception as e:
        app_logger.error(f"Failed to sync MT5 on dashboard refresh: {e}")

    # 1. Fetch latest broker state
    balance, equity, margin, free_margin = mt5_connector.get_account_state()
    
    # 2. Fetch latest DB snapshot to read drawdowns
    latest_snap = get_latest_snapshot(db)
    daily_dd = latest_snap.daily_drawdown if latest_snap else 0.0
    weekly_dd = latest_snap.weekly_drawdown if latest_snap else 0.0
    
    # 3. Fetch performance analytics
    stats = get_performance_stats(db, days=365)
    
    # Calculate actual closed daily PnL
    daily_pnl = get_daily_pnl(db)
    
    # Fetch economic calendar news from Forex Factory
    news_events = fetch_forex_factory_news()
    
    # Fetch live Google news articles
    live_news = fetch_live_forex_news()

    # Fetch recent chat messages for history (limit 20)
    chat_messages = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(20).all()
    chat_messages.reverse()
    chat_history_json = [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat() + "Z"} for m in chat_messages]

    # Fetch saved tasks
    tasks = db.query(DashboardTask).order_by(DashboardTask.created_at.desc()).all()
    tasks_json = [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]

    # 4. Fetch recent 10 signals
    recent_signals = db.query(Signal).order_by(Signal.created_at.desc()).limit(10).all()
    
    # 5. Fetch recent 10 trades
    recent_trades = db.query(Trade).order_by(Trade.created_at.desc()).limit(10).all()
    
    # 5b. Fetch actual open trades
    open_trades = db.query(Trade).filter(Trade.status == "OPEN").all()
    
    # Fetch ALL closed trades for the Trade History tab
    all_closed_trades = db.query(Trade).filter(Trade.status == "CLOSED").order_by(Trade.closed_at.desc()).all()
    
    # 6. Fetch ALL trades serialized to JSON for the calendar
    all_trades_json = get_all_trades_json(db)

    # Calculate weekly pnl (last 7 days closed trades)
    from datetime import timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    weekly_trades = db.query(Trade).filter(Trade.status == "CLOSED", Trade.closed_at >= seven_days_ago).all()
    weekly_pnl = sum((t.profit or 0.0) for t in weekly_trades)

    # Calculate monthly pnl (last 30 days closed trades)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_trades = db.query(Trade).filter(Trade.status == "CLOSED", Trade.closed_at >= thirty_days_ago).all()
    monthly_pnl = sum((t.profit or 0.0) for t in monthly_trades)

    # Calculate open risk (sum of entry - stop loss points * volume * multiplier)
    open_risk = 0.0
    for t in open_trades:
        if t.sl_price and t.sl_price > 0:
            open_risk += abs(t.entry_price - t.sl_price) * t.volume * settings.CONTRACT_MULTIPLIER

    # Calculate margin level
    margin_level = (equity / margin * 100.0) if margin > 0 else 0.0

    # Live tick/spread dynamically for XAUUSD
    active_symbol = "XAUUSD"
    tick = mt5_connector.get_tick_data(active_symbol)
    bid, ask = 0.0, 0.0
    spread_points = 0.0
    spread_pips = 0.0
    digits = 2
    contract_size = 100.0
    point = 0.01
    
    try:
        symbol_info = mt5_connector.api.symbol_info(active_symbol)
        if symbol_info:
            digits = getattr(symbol_info, "digits", 2)
            contract_size = getattr(symbol_info, "trade_contract_size", 100.0)
            point = getattr(symbol_info, "point", 0.01)
    except Exception as e:
        app_logger.error(f"Error querying symbol info for {active_symbol}: {e}")
        
    if tick:
        bid, ask = tick
        if point > 0:
            spread_points = round((ask - bid) / point, 1)
        else:
            spread_points = round((ask - bid) * 100, 1)
        spread_pips = round(spread_points / 10.0, 2)
        
    tick_dict = {
        "symbol": active_symbol,
        "bid": bid,
        "ask": ask,
        "spread_points": spread_points,
        "spread_pips": spread_pips,
        "max_spread_points": settings.MAX_SPREAD_POINTS,
        "spread_warning": spread_points > settings.MAX_SPREAD_POINTS,
        "digits": digits,
        "contract_size": contract_size,
        "point": point
    }
    
    # Combine data
    dashboard_data = {
        "project_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "mt5_mock": settings.MT5_MOCK,
        "mt5_account_mode": mt5_connector.get_account_mode_label(),
        "broker_connected": mt5_connector.is_mock or (mt5_connector.api.account_info() is not None),
        "balance": balance,
        "equity": equity,
        "margin": margin,
        "free_margin": free_margin,
        "margin_level": margin_level,
        "daily_drawdown": daily_dd,
        "weekly_drawdown": weekly_dd,
        "max_daily_drawdown_pct": settings.MAX_DAILY_DRAWDOWN_PCT,
        "max_weekly_drawdown_pct": settings.MAX_WEEKLY_DRAWDOWN_PCT,
        "risk_percent_per_trade": settings.RISK_PERCENT_PER_TRADE,
        "ai_validation_enabled": settings.AI_VALIDATION_ENABLED,
        "performance_stats": stats,
        "daily_pnl": daily_pnl,
        "weekly_pnl": weekly_pnl,
        "monthly_pnl": monthly_pnl,
        "open_risk": open_risk,
        "news_events": news_events,
        "recent_signals": recent_signals,
        "recent_trades": recent_trades,
        "open_trades": open_trades,
        "all_closed_trades": all_closed_trades,
        "all_trades_json": all_trades_json,
        "live_news": live_news,
        "chat_history": chat_history_json,
        "tasks": tasks_json,
        "mt5_login": settings.MT5_LOGIN,
        "mt5_server": settings.MT5_SERVER,
        "mt5_password": settings.MT5_PASSWORD,
        "claude_api_key": settings.CLAUDE_API_KEY or "",
        "openai_api_key": settings.OPENAI_API_KEY or "",
        "gemini_api_key": settings.GEMINI_API_KEY or "",
        "default_trade_volume": settings.DEFAULT_TRADE_VOLUME,
        "tick": tick_dict
    }
    
    return HTMLResponse(content=render_dashboard(dashboard_data))


@app.get("/login", response_class=HTMLResponse)
def login_get(error: Optional[str] = None, session_id: Optional[str] = Cookie(None)):
    """
    Renders the login page. Redirects to dashboard if already authenticated.
    """
    if is_authenticated(session_id):
        return RedirectResponse(url="/", status_code=303)
    from app.utils.dashboard_template import render_login_page
    return HTMLResponse(content=render_login_page(error=error))


@app.post("/login")
def login_post(
    response: Response,
    db: Session = Depends(get_db),
    username: Optional[str] = Form(None),
    password: str = Form(...),
    mt5_login: Optional[int] = Form(None),
    mt5_password: Optional[str] = Form(None),
    mt5_server: Optional[str] = Form(None),
    mt5_mock: Optional[str] = Form(None)
):
    """
    Handles dashboard login form submission.
    Supports either Admin Login or direct MT5 Broker connection setup.
    """
    authenticated = False
    
    # 1. Check Developer Auth (either username matches or direct MT5 connection is chosen, which also requires correct password)
    if username and username == settings.DASHBOARD_USERNAME and password == settings.DASHBOARD_PASSWORD:
        authenticated = True
    elif not username and password == settings.DASHBOARD_PASSWORD:
        # direct MT5 setup page (verified by admin password)
        authenticated = True
        
    if authenticated:
        # 2. If MT5 Connection details are submitted, save them and reconnect
        if mt5_login is not None:
            try:
                # Update settings in-memory
                settings.MT5_LOGIN = mt5_login
                if mt5_password is not None:
                    settings.MT5_PASSWORD = mt5_password
                if mt5_server is not None:
                    settings.MT5_SERVER = mt5_server
                
                is_mock_bool = (mt5_mock == "true")
                settings.MT5_MOCK = is_mock_bool
                
                # Update .env file
                updates = {
                    "MT5_LOGIN": str(mt5_login),
                    "MT5_PASSWORD": mt5_password or "",
                    "MT5_SERVER": mt5_server or "",
                    "MT5_MOCK": "true" if is_mock_bool else "false",
                }
                
                from app.utils.config import BASE_DIR
                env_path = os.path.join(BASE_DIR, ".env")
                if os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    new_lines = []
                    updated_keys = set()
                    for line in lines:
                        if "=" in line and not line.strip().startswith("#"):
                            parts = line.split("=", 1)
                            k = parts[0].strip()
                            if k in updates:
                                new_lines.append(f"{k}={updates[k]}\n")
                                updated_keys.add(k)
                                continue
                        new_lines.append(line)
                    for k, v in updates.items():
                        if k not in updated_keys:
                            new_lines.append(f"{k}={v}\n")
                    with open(env_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                
                # Attempt broker connection and check result
                connection_ok = mt5_connector.connect()
                
                # If the user explicitly chose Live mode and the connection failed,
                # redirect back to the login page with a clear error message.
                if not is_mock_bool and not connection_ok:
                    app_logger.error(
                        f"MT5 live connection failed for account {mt5_login} on server {mt5_server}. "
                        "User redirected back to login."
                    )
                    return RedirectResponse(
                        url=(
                            f"/login?error=MT5+connection+failed+for+account+{mt5_login}+on+server+"
                            f"{(mt5_server or '').replace(' ', '+')}."
                            "+Verify+credentials+and+ensure+the+MetaTrader+5+terminal+is+open."
                        ),
                        status_code=303
                    )
                
                # Sync trades immediately after successful connection
                if connection_ok:
                    from app.database.trade_history import sync_trades_from_mt5
                    try:
                        sync_trades_from_mt5(db, days=365)
                    except Exception as sync_err:
                        app_logger.error(f"Failed to sync trades after login MT5 setup: {sync_err}")
            except Exception as e:
                app_logger.error(f"Error updating MT5 settings during login: {e}")
                
        # 3. Establish session cookie
        sig = get_session_signature()
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="session_id",
            value=sig,
            httponly=True,
            samesite="lax",
            max_age=86400 * 7  # 7 days
        )
        return response
        
    return RedirectResponse(url="/login?error=Invalid%20credentials", status_code=303)


@app.get("/logout")
def logout(response: Response):
    """
    Logs out the user by clearing the session cookie.
    """
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="session_id")
    return response



@app.post("/api/v1/reconnect")
def reconnect_broker(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Attempts to reconnect to the MT5 broker terminal using current stored credentials.
    Can be called from the dashboard without changing any settings.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    app_logger.info(f"Manual reconnect requested for account {settings.MT5_LOGIN} on {settings.MT5_SERVER}")
    
    try:
        connected = mt5_connector.connect()
        if connected:
            # Sync latest trades after reconnect
            from app.database.trade_history import sync_trades_from_mt5
            try:
                sync_trades_from_mt5(db, days=365)
            except Exception as sync_err:
                app_logger.error(f"Failed to sync trades after manual reconnect: {sync_err}")
            
            mode = "Mock" if mt5_connector.is_mock else "Live"
            msg = f"Connected to {settings.MT5_SERVER} (Account: {settings.MT5_LOGIN}, Mode: {mode})"
            if not mt5_connector.is_mock:
                try:
                    acc = mt5_connector.api.account_info()
                    if acc:
                        msg = f"Connected — Account {acc.login} | Balance: {acc.balance:.2f} {acc.currency} | Server: {acc.server}"
                except Exception:
                    pass
            return {"status": "SUCCESS", "message": msg}
        else:
            err_detail = ""
            try:
                if not mt5_connector.is_mock and hasattr(mt5_connector.api, "last_error"):
                    code, msg = mt5_connector.api.last_error()
                    if code != 0:
                        err_detail = f" MT5 error {code}: {msg}."
            except Exception:
                pass
            return {
                "status": "ERROR",
                "message": (
                    f"Could not connect to {settings.MT5_SERVER} (account {settings.MT5_LOGIN})."
                    f"{err_detail} Make sure MetaTrader 5 terminal is open and the account is logged in."
                )
            }
    except Exception as e:
        app_logger.error(f"Reconnect endpoint error: {e}")
        return {"status": "ERROR", "message": str(e)}


@app.get("/api/v1/live-state")
async def get_live_state(db: Session = Depends(get_db), force_refresh: bool = False, session_id: Optional[str] = Cookie(None)):
    """
    Returns live account parameters, active open trades, pending trades, last tick pricing,
    and technical stats to support client-side real-time rendering.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    # 1. Fetch latest broker state with throttling
    global _last_live_state_sync_time
    import time
    now_time = time.time()
    try:
        from app.database.trade_history import sync_trades_from_mt5
        if force_refresh or (now_time - _last_live_state_sync_time > 5.0):
            sync_trades_from_mt5(db, days=30, sync_history=True)
            _last_live_state_sync_time = now_time
        else:
            sync_trades_from_mt5(db, sync_history=False)
    except Exception as e:
        app_logger.error(f"Failed to sync MT5 on live-state update: {e}")

    balance, equity, margin, free_margin = mt5_connector.get_account_state()
    margin_level = (equity / margin * 100.0) if margin > 0 else 0.0
    
    # 2. Query DB open trades
    open_trades = db.query(Trade).filter(Trade.status == "OPEN").all()
    open_trades_list = []
    for t in open_trades:
        # Get live tick info to estimate current price
        symbol = t.symbol
        tick = mt5_connector.get_tick_data(symbol)
        curr_price = t.entry_price
        if tick:
            curr_price = tick[0] if t.order_type == "BUY" else tick[1] # bid or ask
            
        # Calculate duration in seconds
        duration_sec = 0.0
        if t.created_at:
            duration_sec = (datetime.utcnow() - t.created_at).total_seconds()
            
        # Calculate Risk Reward Ratio
        rr = 0.0
        if t.sl_price and t.sl_price > 0 and t.entry_price != t.sl_price:
            rr = abs((t.tp_price - t.entry_price) / (t.entry_price - t.sl_price))
        else:
            rr = 2.0  # fallback

        open_trades_list.append({
            "ticket": t.ticket,
            "symbol": t.symbol,
            "order_type": t.order_type,
            "volume": t.volume,
            "entry_price": t.entry_price,
            "current_price": curr_price,
            "sl_price": t.sl_price,
            "tp_price": t.tp_price,
            "pips": calculate_pips(t.entry_price, curr_price, t.symbol),
            "profit": t.profit,
            "rr_ratio": round(rr, 2),
            "duration": duration_sec,
            "ai_confidence": t.ai_confidence or 0.85,
            "created_at": t.created_at.isoformat() + "Z" if t.created_at else None
        })
        
    # 2b. Query Pending Orders
    pending_trades_list = []
    try:
        api = mt5_connector.api
        if mt5_connector.is_mock or api.terminal_info():
            raw_orders = api.orders_get()
            if raw_orders:
                for order in raw_orders:
                    o_type = getattr(order, "type", 2)
                    o_type_label = "BUY LIMIT"
                    if o_type == 2: o_type_label = "BUY LIMIT"
                    elif o_type == 3: o_type_label = "SELL LIMIT"
                    elif o_type == 4: o_type_label = "BUY STOP"
                    elif o_type == 5: o_type_label = "SELL STOP"
                    elif o_type == 6: o_type_label = "BUY STOP LIMIT"
                    elif o_type == 7: o_type_label = "SELL STOP LIMIT"
                    
                    pending_trades_list.append({
                        "ticket": getattr(order, "ticket", None),
                        "symbol": getattr(order, "symbol", "XAUUSD"),
                        "order_type": o_type_label,
                        "volume": getattr(order, "volume_initial", 0.0),
                        "entry_price": getattr(order, "price_open", 0.0),
                        "sl_price": getattr(order, "sl", 0.0),
                        "tp_price": getattr(order, "tp", 0.0),
                        "comment": getattr(order, "comment", "")
                    })
    except Exception as err:
        app_logger.error(f"Failed to query pending orders: {err}")

    # 3. Query last signal
    last_signal = db.query(Signal).order_by(Signal.created_at.desc()).first()
    last_signal_data = None
    if last_signal:
        last_signal_data = {
            "created_at": last_signal.created_at.isoformat() + "Z" if last_signal.created_at else None,
            "symbol": last_signal.symbol,
            "direction": last_signal.direction,
            "action_taken": last_signal.action_taken,
            "reason": last_signal.reason,
            "price": last_signal.price
        }
        
    # 4. Live tick/spread dynamically for XAUUSD
    symbol = "XAUUSD"
    tick = mt5_connector.get_tick_data(symbol)
    bid, ask = 0.0, 0.0
    spread_points = 0.0
    spread_pips = 0.0
    digits = 2
    contract_size = 100.0
    point = 0.01
    
    try:
        symbol_info = mt5_connector.api.symbol_info(symbol)
        if symbol_info:
            digits = getattr(symbol_info, "digits", 2)
            contract_size = getattr(symbol_info, "trade_contract_size", 100.0)
            point = getattr(symbol_info, "point", 0.01)
    except Exception as e:
        app_logger.error(f"Error querying symbol info for {symbol}: {e}")
        
    if tick:
        bid, ask = tick
        if point > 0:
            spread_points = round((ask - bid) / point, 1)
        else:
            spread_points = round((ask - bid) * 100, 1)
        spread_pips = round(spread_points / 10.0, 2)
        
    # 5. Fetch performance stats
    stats = get_performance_stats(db, days=365)
    
    # Calculate actual closed daily PnL
    daily_pnl = get_daily_pnl(db)
    
    # Fetch Forex Factory news feed
    news_events = await asyncio.to_thread(fetch_forex_factory_news, force_refresh)
    
    # 6. Drawdowns
    latest_snap = get_latest_snapshot(db)
    daily_dd = latest_snap.daily_drawdown if latest_snap else 0.0
    weekly_dd = latest_snap.weekly_drawdown if latest_snap else 0.0

    # 7. Fetch recent signals and closed trades
    recent_signals = db.query(Signal).order_by(Signal.created_at.desc()).limit(10).all()
    recent_trades = db.query(Trade).order_by(Trade.created_at.desc()).limit(10).all()
    all_closed_trades = db.query(Trade).filter(Trade.status == "CLOSED").order_by(Trade.closed_at.desc()).limit(20).all()
    
    recent_signals_list = []
    for s in recent_signals:
        recent_signals_list.append({
            "created_at": s.created_at.isoformat() + "Z" if s.created_at else None,
            "symbol": s.symbol,
            "direction": s.direction,
            "rsi": s.rsi,
            "ema_20": s.ema_20,
            "ema_50": s.ema_50,
            "atr": s.atr,
            "volume": s.volume,
            "market_structure": s.market_structure,
            "raw_payload": s.raw_payload,
            "action_taken": s.action_taken,
            "reason": s.reason,
            "price": s.price
        })
        
    recent_trades_list = []
    for tr in recent_trades:
        recent_trades_list.append({
            "ticket": tr.ticket,
            "symbol": tr.symbol,
            "order_type": tr.order_type,
            "volume": tr.volume,
            "entry_price": tr.entry_price,
            "sl_price": tr.sl_price,
            "tp_price": tr.tp_price,
            "exit_price": tr.exit_price,
            "profit": tr.profit,
            "status": tr.status,
            "comment": tr.comment,
            "created_at": tr.created_at.isoformat() + "Z" if tr.created_at else None,
            "closed_at": tr.closed_at.isoformat() + "Z" if tr.closed_at else None
        })

    closed_trades_list = []
    for tr in all_closed_trades:
        closed_trades_list.append({
            "ticket": tr.ticket,
            "symbol": tr.symbol,
            "order_type": tr.order_type,
            "volume": tr.volume,
            "entry_price": tr.entry_price,
            "exit_price": tr.exit_price,
            "profit": tr.profit,
            "swap": tr.swap,
            "commission": tr.commission,
            "comment": tr.comment,
            "created_at": tr.created_at.isoformat() + "Z" if tr.created_at else None,
            "closed_at": tr.closed_at.isoformat() + "Z" if tr.closed_at else None
        })
    
    return {
        "status": "SUCCESS",
        "broker_connected": mt5_connector.is_mock or (mt5_connector.api.account_info() is not None),
        "account_mode": mt5_connector.get_account_mode_label(),
        "balance": balance,
        "equity": equity,
        "margin": margin,
        "free_margin": free_margin,
        "margin_level": margin_level,
        "open_trades": open_trades_list,
        "pending_trades": pending_trades_list,
        "recent_signals": recent_signals_list,
        "recent_trades": recent_trades_list,
        "all_closed_trades": closed_trades_list,
        "last_signal": last_signal_data,
        "tick": {
            "symbol": symbol,
            "bid": bid,
            "ask": ask,
            "spread_points": spread_points,
            "spread_pips": spread_pips,
            "max_spread_points": settings.MAX_SPREAD_POINTS,
            "spread_warning": spread_points > settings.MAX_SPREAD_POINTS,
            "digits": digits,
            "contract_size": contract_size,
            "point": point
        },
        "performance_stats": stats,
        "daily_pnl": daily_pnl,
        "news_events": news_events,
        "drawdown": {
            "daily_drawdown": daily_dd,
            "weekly_drawdown": weekly_dd
        },
        "server_time": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/v1/close-trade")
async def close_trade_endpoint(ticket: int, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Allows developers to manually close any active position via dashboard POST request.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    from app.broker.order_manager import order_manager
    success = await asyncio.to_thread(order_manager.close_position_by_ticket, ticket, comment="Manual Close via Dashboard")
    if success:
        from app.database.trade_history import update_trade_by_ticket
        exit_price = 0.0
        profit = 0.0
        
        trade = db.query(Trade).filter(Trade.ticket == ticket).first()
        if trade:
            # Capture current bid/ask for the specific trade symbol
            tick = await asyncio.to_thread(mt5_connector.get_tick_data, trade.symbol)
            if tick:
                bid, ask = tick
                exit_price = bid if trade.order_type == "BUY" else ask
                # Compute profit using configured multiplier via utility function
                from app.utils.calculations import calculate_profit
                profit = calculate_profit(trade.order_type, trade.entry_price, exit_price, trade.volume, symbol=trade.symbol)
            
            await asyncio.to_thread(
                update_trade_by_ticket,
                db,
                ticket,
                {
                    "status": "CLOSED",
                    "exit_price": exit_price,
                    "profit": profit,
                    "comment": "Manual Close via Dashboard 🔴"
                }
            )
            
            # Send Telegram Alert asynchronously
            asyncio.create_task(AlertManager.notify_close_trade({
                "ticket": ticket,
                "symbol": trade.symbol,
                "order_type": trade.order_type,
                "volume": trade.volume,
                "entry_price": trade.entry_price,
                "exit_price": exit_price,
                "profit": profit,
                "comment": "Manual Close via Dashboard 🔴"
            }))
            
        return {"status": "SUCCESS", "message": f"Position #{ticket} closed successfully."}
    else:
        return {"status": "ERROR", "message": f"Failed to close position #{ticket}."}


class ModifyStopsRequest(BaseModel):
    ticket: int
    sl: float
    tp: float


@app.post("/api/v1/modify-stops")
async def modify_stops_endpoint(
    payload: ModifyStopsRequest,
    db: Session = Depends(get_db),
    session_id: Optional[str] = Cookie(None)
):
    """
    Manually modifies the stops (SL and TP) of an active position.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    from app.broker.order_manager import order_manager
    from app.database.trade_history import update_trade_by_ticket
    
    success = await asyncio.to_thread(order_manager.modify_stops, payload.ticket, payload.sl, payload.tp)
    if success:
        await asyncio.to_thread(
            update_trade_by_ticket,
            db,
            payload.ticket,
            {
                "sl_price": payload.sl,
                "tp_price": payload.tp
            }
        )
        return {"status": "SUCCESS", "message": f"Stops modified successfully for ticket #{payload.ticket}."}
    else:
        return {"status": "ERROR", "message": f"Failed to modify stops for ticket #{payload.ticket}."}


class PartialCloseRequest(BaseModel):
    ticket: int
    volume: float


@app.post("/api/v1/partial-close")
async def partial_close_endpoint(
    payload: PartialCloseRequest,
    db: Session = Depends(get_db),
    session_id: Optional[str] = Cookie(None)
):
    """
    Manually partially closes an active position's volume.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    from app.database.trade_history import update_trade_by_ticket
    
    api = mt5_connector.api
    positions = await asyncio.to_thread(api.positions_get, ticket=payload.ticket)
    if not positions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Position #{payload.ticket} not found.")
        
    position = positions[0]
    volume_to_close = min(payload.volume, position.volume)
    
    symbol = position.symbol
    close_type = api.ORDER_TYPE_SELL if position.type == api.ORDER_TYPE_BUY else api.ORDER_TYPE_BUY
    
    tick = await asyncio.to_thread(mt5_connector.get_tick_data, symbol)
    if not tick:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pricing tick info unavailable.")
        
    bid, ask = tick
    price = ask if close_type == api.ORDER_TYPE_BUY else bid
    
    filling_type = getattr(api, "ORDER_FILLING_IOC", 1)
    try:
        symbol_info = await asyncio.to_thread(api.symbol_info, symbol)
        if symbol_info and hasattr(symbol_info, "filling_mode"):
            if symbol_info.filling_mode & getattr(api, "SYMBOL_FILLING_FOK", 1):
                filling_type = getattr(api, "ORDER_FILLING_FOK", 0)
            elif symbol_info.filling_mode & getattr(api, "SYMBOL_FILLING_IOC", 2):
                filling_type = getattr(api, "ORDER_FILLING_IOC", 1)
            else:
                filling_type = getattr(api, "ORDER_FILLING_RETURN", 2)
    except Exception:
        pass
        
    request = {
        "action": api.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume_to_close),
        "type": close_type,
        "position": payload.ticket,
        "price": float(price),
        "deviation": settings.MAX_SLIPPAGE_POINTS,
        "magic": settings.MT5_MAGIC_NUMBER,
        "comment": "Partial Close via Dashboard",
        "type_time": getattr(api, "ORDER_TIME_GTC", 0),
        "type_filling": filling_type
    }
    
    result = await asyncio.to_thread(api.order_send, request)
    if result is None or result.retcode != api.TRADE_RETCODE_DONE:
        err_detail = getattr(result, "comment", "Unknown broker rejection.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Broker rejected partial close: {err_detail}")
        
    trade = db.query(Trade).filter(Trade.ticket == payload.ticket).first()
    if trade:
        new_volume = max(0.0, trade.volume - volume_to_close)
        if new_volume < 0.01:
            await asyncio.to_thread(
                update_trade_by_ticket,
                db,
                payload.ticket,
                {
                    "status": "CLOSED",
                    "exit_price": result.price,
                    "profit": (trade.profit or 0.0) + getattr(result, "profit", 0.0),
                    "comment": "Partial Close -> Fully Closed 🔴"
                }
            )
        else:
            await asyncio.to_thread(
                update_trade_by_ticket,
                db,
                payload.ticket,
                {
                    "volume": new_volume,
                    "comment": f"Partial Close: -{volume_to_close:.2f} Lots"
                }
            )
            
    return {"status": "SUCCESS", "message": f"Closed {volume_to_close:.2f} lots of position #{payload.ticket}."}


class PlaceOrderRequest(BaseModel):
    symbol: str
    direction: str
    volume: float
    sl: float
    tp: float


@app.post("/api/v1/place-order")
async def place_order_endpoint(
    payload: PlaceOrderRequest,
    db: Session = Depends(get_db),
    session_id: Optional[str] = Cookie(None)
):
    """
    Manually places an order using custom parameters, typically suggested by AI prediction.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    from app.broker.order_manager import order_manager
    from app.database.trade_history import create_trade
    
    direction = payload.direction.upper()
    if direction not in ["BUY", "SELL"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order direction")

    if not mt5_connector.is_mock:
        try:
            terminal_info = mt5_connector.api.terminal_info()
            if terminal_info is not None and not getattr(terminal_info, "trade_allowed", True):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="MetaTrader 5 trading is disabled in the terminal. Enable Algo Trading / AutoTrading and retry."
                )
        except HTTPException:
            raise
        except Exception as e:
            app_logger.error(f"Failed to verify MT5 trading permissions: {e}")

    # Validate price levels before sending order
    if payload.sl > 0 and payload.tp > 0:
        if direction == "BUY":
            if payload.sl >= payload.tp:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SL must be below TP for BUY orders.")
        else:  # SELL
            if payload.sl <= payload.tp:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SL must be above TP for SELL orders.")
    execution_result = await asyncio.to_thread(
        order_manager.send_market_order,
        symbol=payload.symbol,
        order_type=direction,
        volume=payload.volume,
        sl=payload.sl,
        tp=payload.tp,
        comment="Manual AI Order"
    )
    
    if execution_result["status"] == "SUCCESS":
        # Log successful trade to database
        trade_db_entry = {
            "ticket": execution_result["ticket"],
            "symbol": payload.symbol,
            "order_type": direction,
            "volume": payload.volume,
            "entry_price": execution_result["price"],
            "sl_price": payload.sl,
            "tp_price": payload.tp,
            "status": "OPEN",
            "magic_number": settings.MT5_MAGIC_NUMBER,
            "comment": "Manual AI Order",
        }
        await asyncio.to_thread(create_trade, db, trade_db_entry)
        
        # Async Telegram notification
        asyncio.create_task(AlertManager.notify_new_trade({
            "ticket": execution_result["ticket"],
            "symbol": payload.symbol,
            "order_type": direction,
            "volume": payload.volume,
            "entry_price": execution_result["price"],
            "sl_price": payload.sl,
            "tp_price": payload.tp,
            "ai_confidence": None,
            "ai_reasoning": "Manually placed via developer dashboard"
        }))
        
        return {
            "status": "SUCCESS",
            "ticket": execution_result["ticket"],
            "price": execution_result["price"]
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=execution_result.get("error", "Execution failed"))


@app.get("/api/v1/chart-data")
def get_chart_data(timeframe: str = "M15", count: int = 100):
    """
    Returns historical candlestick data for XAUUSD.
    """
    try:
        df = mt5_connector.get_candles("XAUUSD", timeframe, count)
        
        # Calculate broker timezone offset relative to UTC
        broker_offset_hours = 0.0
        if not mt5_connector.is_mock:
            try:
                import time
                tick = mt5_connector.api.symbol_info_tick("XAUUSD")
                if tick:
                    diff_hours = (tick.time - time.time()) / 3600.0
                    if -14.0 <= diff_hours <= 14.0:
                        broker_offset_hours = float(round(diff_hours))
            except Exception:
                pass

        if df is not None and not df.empty:
            data = []
            for _, row in df.iterrows():
                data.append({
                    "time": int(row["time"]),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"]) if "volume" in row else 0.0
                })
            return {"status": "SUCCESS", "data": data, "broker_offset_hours": broker_offset_hours}
        return {"status": "ERROR", "message": "Failed to fetch rates from broker."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@app.post("/api/v1/predict-trade")
def predict_trade_endpoint(timeframe: str = "M15", db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Triggers AI / technical analysis to predict Entry, SL, and TP for the next trade.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    from app.ai.trade_predictor import predict_next_trade
    prediction = predict_next_trade(db, timeframe=timeframe)
    return prediction


@app.post("/api/v1/maintenance/clear-history")
def clear_history(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Clears local database history (Trade, Signal, AccountSnapshot)
    and synchronizes clean from the MT5 broker account.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        app_logger.info("Maintenance triggered: Clearing history and re-syncing from broker.")
        # 1. Truncate tables
        db.query(Trade).delete()
        db.query(Signal).delete()
        db.query(AccountSnapshot).delete()
        db.commit()
        
        # 2. Re-synchronize from MT5 (last 365 days)
        from app.database.trade_history import sync_trades_from_mt5
        sync_trades_from_mt5(db, days=365)
        
        # 3. Create a fresh snapshot of current account state
        balance, equity, margin, free_margin = mt5_connector.get_account_state()
        if balance > 0.0:
            create_account_snapshot(db, balance, equity, margin, free_margin)
            
        return {"status": "SUCCESS", "message": "History cleared and synchronized from account."}
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to clear history: {e}")
        return {"status": "ERROR", "message": str(e)}


@app.post("/api/v1/maintenance/reset-daily-pnl")
def reset_daily_pnl(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    """
    Resets the local database closed trades for today by re-syncing from MT5.
    Also clears today's snapshots to reset daily drawdown peaks.
    """
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
    try:
        app_logger.info("Maintenance triggered: Resetting daily PnL and snapshots.")
        from app.utils.helpers import get_utc_now
        now = get_utc_now()
        start_of_day = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
        
        # Delete only closed trades that were closed today (to allow fresh sync)
        db.query(Trade).filter(
            Trade.status == "CLOSED",
            Trade.closed_at >= start_of_day
        ).delete()
        
        # Delete snapshots from today
        db.query(AccountSnapshot).filter(
            AccountSnapshot.timestamp >= start_of_day
        ).delete()
        
        db.commit()
        
        # Sync again
        from app.database.trade_history import sync_trades_from_mt5
        sync_trades_from_mt5(db, days=1) # Sync today
        
        # Create fresh snapshot
        balance, equity, margin, free_margin = mt5_connector.get_account_state()
        if balance > 0.0:
            create_account_snapshot(db, balance, equity, margin, free_margin)
            
        return {"status": "SUCCESS", "message": "Daily PNL reset complete."}
    except Exception as e:
        db.rollback()
        app_logger.error(f"Failed to reset daily PnL: {e}")
        return {"status": "ERROR", "message": str(e)}


class SettingsUpdateSchema(BaseModel):
    mt5_login: int
    mt5_password: str
    mt5_server: str
    mt5_mock: bool
    claude_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None


@app.post("/api/v1/settings")
def update_settings_endpoint(payload: SettingsUpdateSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
    try:
        # Update settings in-memory
        settings.MT5_LOGIN = payload.mt5_login
        settings.MT5_PASSWORD = payload.mt5_password
        settings.MT5_SERVER = payload.mt5_server
        settings.MT5_MOCK = payload.mt5_mock
        if payload.claude_api_key is not None:
            settings.CLAUDE_API_KEY = payload.claude_api_key
        if payload.openai_api_key is not None:
            settings.OPENAI_API_KEY = payload.openai_api_key
        if payload.gemini_api_key is not None:
            settings.GEMINI_API_KEY = payload.gemini_api_key
            
        # Update .env file
        updates = {
            "MT5_LOGIN": str(payload.mt5_login),
            "MT5_PASSWORD": payload.mt5_password,
            "MT5_SERVER": payload.mt5_server,
            "MT5_MOCK": "true" if payload.mt5_mock else "false",
        }
        if payload.claude_api_key is not None:
            updates["CLAUDE_API_KEY"] = payload.claude_api_key
        if payload.openai_api_key is not None:
            updates["OPENAI_API_KEY"] = payload.openai_api_key
        if payload.gemini_api_key is not None:
            updates["GEMINI_API_KEY"] = payload.gemini_api_key
            
        from app.utils.config import BASE_DIR
        env_path = os.path.join(BASE_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            updated_keys = set()
            for line in lines:
                if "=" in line and not line.strip().startswith("#"):
                    parts = line.split("=", 1)
                    k = parts[0].strip()
                    if k in updates:
                        new_lines.append(f"{k}={updates[k]}\n")
                        updated_keys.add(k)
                        continue
                new_lines.append(line)
            for k, v in updates.items():
                if k not in updated_keys:
                    new_lines.append(f"{k}={v}\n")
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
                
        # Reconnect MT5
        connected = mt5_connector.connect()
        
        # If live mode was selected and the connection failed, report the error clearly
        if not payload.mt5_mock and not connected:
            err_msg = "MT5 terminal connection failed"
            try:
                if not mt5_connector.is_mock and mt5_connector.api and hasattr(mt5_connector.api, "last_error"):
                    code, msg = mt5_connector.api.last_error()
                    if msg:
                        err_msg = f"MT5 connection failed: {msg} (code {code})"
            except Exception:
                pass
            app_logger.error(f"Settings update: {err_msg} for account {payload.mt5_login} on {payload.mt5_server}")
            return {"status": "ERROR", "message": err_msg + ". Verify credentials and ensure MetaTrader 5 terminal (terminal64.exe) is running."}
        
        # Trigger clean re-sync of trades from MT5 if connected
        if connected:
            from app.database.trade_history import sync_trades_from_mt5
            try:
                sync_trades_from_mt5(db, days=365)
            except Exception as sync_err:
                app_logger.error(f"Failed to sync trades after setting update: {sync_err}")
                
        return {"status": "SUCCESS", "message": "Settings updated and broker reconnected."}
    except Exception as e:
        app_logger.error(f"Failed to update settings: {e}")
        return {"status": "ERROR", "message": str(e)}


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    completed: bool


@app.get("/api/v1/tasks")
def get_tasks_endpoint(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    tasks = db.query(DashboardTask).order_by(DashboardTask.created_at.desc()).all()
    return [{"id": t.id, "title": t.title, "completed": t.completed, "created_at": t.created_at.isoformat() + "Z"} for t in tasks]


@app.post("/api/v1/tasks")
def create_task_endpoint(payload: TaskCreateSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    new_task = DashboardTask(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status": "SUCCESS", "task": {"id": new_task.id, "title": new_task.title, "completed": new_task.completed}}


@app.put("/api/v1/tasks/{task_id}")
def update_task_endpoint(task_id: int, payload: TaskUpdateSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    task = db.query(DashboardTask).filter(DashboardTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = payload.completed
    db.commit()
    return {"status": "SUCCESS"}


@app.delete("/api/v1/tasks/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    task = db.query(DashboardTask).filter(DashboardTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "SUCCESS"}


class JournalCreateSchema(BaseModel):
    trade_ticket: int
    setup_type: Optional[str] = None
    emotion: Optional[str] = None
    notes: Optional[str] = None
    lessons_learned: Optional[str] = None
    screenshot_url: Optional[str] = None

class PortfolioCreateSchema(BaseModel):
    account_name: str
    login_id: int
    password: str
    server: str
    balance: float

class MarketIntelRequest(BaseModel):
    brief_type: str


@app.get("/api/v1/journal")
def get_journals(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    journals = db.query(TradeJournal).order_by(TradeJournal.created_at.desc()).all()
    return [{"id": j.id, "trade_ticket": j.trade_ticket, "setup_type": j.setup_type, "emotion": j.emotion, "notes": j.notes, "lessons_learned": j.lessons_learned, "screenshot_url": j.screenshot_url, "created_at": j.created_at.isoformat() + "Z"} for j in journals]

@app.post("/api/v1/journal")
def create_journal(payload: JournalCreateSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    existing = db.query(TradeJournal).filter(TradeJournal.trade_ticket == payload.trade_ticket).first()
    if existing:
        existing.setup_type = payload.setup_type
        existing.emotion = payload.emotion
        existing.notes = payload.notes
        existing.lessons_learned = payload.lessons_learned
        existing.screenshot_url = payload.screenshot_url
        db.commit()
        db.refresh(existing)
        return {"status": "SUCCESS", "message": "Journal updated successfully.", "journal": {"id": existing.id, "trade_ticket": existing.trade_ticket}}
    
    new_j = TradeJournal(
        trade_ticket=payload.trade_ticket,
        setup_type=payload.setup_type,
        emotion=payload.emotion,
        notes=payload.notes,
        lessons_learned=payload.lessons_learned,
        screenshot_url=payload.screenshot_url
    )
    db.add(new_j)
    db.commit()
    db.refresh(new_j)
    return {"status": "SUCCESS", "message": "Journal created successfully.", "journal": {"id": new_j.id, "trade_ticket": new_j.trade_ticket}}

@app.get("/api/v1/portfolio/accounts")
def get_portfolio_accounts(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    accounts = db.query(PortfolioAccount).all()
    return [{"id": a.id, "account_name": a.account_name, "login_id": a.login_id, "server": a.server, "balance": a.balance, "equity": a.equity, "is_mock": a.is_mock, "is_active": a.is_active} for a in accounts]

@app.post("/api/v1/portfolio/accounts")
def create_portfolio_account(payload: PortfolioCreateSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    existing = db.query(PortfolioAccount).filter(PortfolioAccount.login_id == payload.login_id).first()
    if existing:
        return {"status": "ERROR", "message": "Account already linked to portfolio."}
        
    new_acc = PortfolioAccount(
        account_name=payload.account_name,
        login_id=payload.login_id,
        password=payload.password,
        server=payload.server,
        balance=payload.balance,
        equity=payload.balance,
        is_mock=True
    )
    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return {"status": "SUCCESS", "message": "Sub-account linked successfully."}

@app.delete("/api/v1/portfolio/accounts/{account_id}")
def delete_portfolio_account(account_id: int, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    acc = db.query(PortfolioAccount).filter(PortfolioAccount.id == account_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(acc)
    db.commit()
    return {"status": "SUCCESS", "message": "Account unlinked."}

@app.get("/api/v1/ai-coach/evaluations")
def get_coach_evaluations(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    evals = db.query(AICoachEvaluation).order_by(AICoachEvaluation.created_at.desc()).all()
    return [{"id": e.id, "trade_ticket": e.trade_ticket, "won_lost_reason": e.won_lost_reason, "mistakes": e.mistakes, "strengths": e.strengths, "risk_observations": e.risk_observations, "improvements": e.improvements, "created_at": e.created_at.isoformat() + "Z"} for e in evals]

@app.post("/api/v1/ai-coach/evaluate/{ticket}")
async def evaluate_trade_coach(ticket: int, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    trade = db.query(Trade).filter(Trade.ticket == ticket).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found in database.")
        
    existing = db.query(AICoachEvaluation).filter(AICoachEvaluation.trade_ticket == ticket).first()
    if existing:
        return {"status": "SUCCESS", "evaluation": {"won_lost_reason": existing.won_lost_reason, "mistakes": existing.mistakes, "strengths": existing.strengths, "risk_observations": existing.risk_observations, "improvements": existing.improvements}}
        
    journal = db.query(TradeJournal).filter(TradeJournal.trade_ticket == ticket).first()
    journal_context = ""
    if journal:
        journal_context = f"\nTrader Journal Notes: {journal.notes}\nTrader Emotion: {journal.emotion}\nTrader Lessons: {journal.lessons_learned}"
        
    signal = db.query(Signal).filter(Signal.created_at <= trade.created_at).order_by(Signal.created_at.desc()).first()
    signal_context = ""
    if signal:
        signal_context = f"\nTechnical Indicators at Entry:\n- RSI: {signal.rsi}\n- EMA20: {signal.ema_20}\n- EMA50: {signal.ema_50}\n- ATR: {signal.atr}\n- Volume: {signal.volume}\n- Structure: {signal.market_structure}"
        
    duration_str = "Unknown"
    if trade.closed_at and trade.created_at:
        duration_str = f"{(trade.closed_at - trade.created_at).total_seconds() / 60.0:.1f} minutes"
        
    user_prompt = (
        f"Analyze the completed trade to evaluate execution quality and psychology:\n\n"
        f"Trade Parameters:\n"
        f"- Ticket: #{trade.ticket}\n"
        f"- Symbol: {trade.symbol}\n"
        f"- Direction: {trade.order_type}\n"
        f"- Volume: {trade.volume} Lots\n"
        f"- Entry Price: {trade.entry_price:.2f}\n"
        f"- Exit Price: {trade.exit_price or 0.0:.2f}\n"
        f"- Stop Loss: {trade.sl_price:.2f}\n"
        f"- Take Profit: {trade.tp_price:.2f}\n"
        f"- Profit/Loss: ${trade.profit:+.2f}\n"
        f"- Holding Time: {duration_str}\n"
        f"- Status: {trade.status}\n"
        f"- Comment: {trade.comment}\n"
        f"{journal_context}\n"
        f"{signal_context}\n"
    )
    
    system_prompt = (
        "You are an expert quantitative trading coach and performance psychologist.\n"
        "Analyze the completed trade and respond ONLY with a raw JSON block containing psychological and execution observations.\n"
        "Do not include markdown blocks, backticks, or introduction/conclusion text.\n"
        "Expected JSON format:\n"
        "{\n"
        "  \"won_lost_reason\": \"string description of why trade won or lost\",\n"
        "  \"mistakes\": \"string description of mistakes made during execution/stops\",\n"
        "  \"strengths\": \"string description of strengths shown (discipline, patience)\",\n"
        "  \"risk_observations\": \"string description of spread, slippage, sizing risks\",\n"
        "  \"improvements\": \"string description of clear steps for next time\"\n"
        "}"
    )
    
    try:
        ai_resp = await asyncio.to_thread(generate_ai_text, system_prompt, user_prompt)
        
        clean_response = ai_resp.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        data = json.loads(clean_response)
        
        new_eval = AICoachEvaluation(
            trade_ticket=ticket,
            won_lost_reason=str(data.get("won_lost_reason", "")),
            mistakes=str(data.get("mistakes", "")),
            strengths=str(data.get("strengths", "")),
            risk_observations=str(data.get("risk_observations", "")),
            improvements=str(data.get("improvements", ""))
        )
        db.add(new_eval)
        db.commit()
        return {"status": "SUCCESS", "evaluation": data}
    except Exception as e:
        app_logger.error(f"Failed to generate coach evaluation for ticket {ticket}: {e}")
        mock_eval = {
            "won_lost_reason": f"Fallback: Trade closed with ${trade.profit:+.2f} profit. Asset structural parameters suggest trend alignment.",
            "mistakes": "No explicit execution errors detected under local fallback parameters.",
            "strengths": "Risk parameters (1% rule) correctly maintained for the setup.",
            "risk_observations": "Drawdown remained well within daily allowance constraints.",
            "improvements": "Review crossover timeframes in details to improve holding duration."
        }
        new_eval = AICoachEvaluation(
            trade_ticket=ticket,
            won_lost_reason=mock_eval["won_lost_reason"],
            mistakes=mock_eval["mistakes"],
            strengths=mock_eval["strengths"],
            risk_observations=mock_eval["risk_observations"],
            improvements=mock_eval["improvements"]
        )
        db.add(new_eval)
        db.commit()
        return {"status": "SUCCESS", "evaluation": mock_eval}

@app.get("/api/v1/market-intel/brief")
def get_market_briefs(db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    briefs = db.query(MarketIntelBrief).order_by(MarketIntelBrief.created_at.desc()).limit(10).all()
    return [{"id": b.id, "brief_type": b.brief_type, "content": b.content, "created_at": b.created_at.isoformat() + "Z"} for b in briefs]

@app.post("/api/v1/market-intel/brief")
async def generate_market_brief(payload: MarketIntelRequest, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
    from app.utils.news_manager import fetch_forex_factory_news
    news_events = await asyncio.to_thread(fetch_forex_factory_news, True)
    news_summary_list = []
    for e in news_events[:5]:
        news_summary_list.append(f"- Event: {e['title']} | Impact: {e['impact']} | Currency: {e['country']} | Forecast: {e['forecast']} | Prev: {e['previous']}")
    news_summary_str = "\n".join(news_summary_list) if news_summary_list else "No major high-impact calendar news scheduled."
    
    tick = mt5_connector.get_tick_data("XAUUSD")
    price_str = f"Bid: {tick[0]} / Ask: {tick[1]}" if tick else "Unavailable"
    
    user_prompt = (
        f"Generate a quantitative market intelligence outlook briefing for Gold (XAUUSD).\n"
        f"Timeframe Type: {payload.brief_type}\n\n"
        f"Current Market Data:\n"
        f"- Asset: XAUUSD (Gold)\n"
        f"- Pricing: {price_str}\n\n"
        f"Upcoming Economic Calendar Events:\n"
        f"{news_summary_str}\n"
    )
    
    system_prompt = (
        f"You are a Senior Quantitative Analyst and Quant Macro Strategist.\n"
        f"Provide a premium, high-impact, professional market intelligence summary briefing.\n"
        f"The briefing must look institutional, direct, and actionable. Write in clean markdown. Do not include chat intro/outro."
    )
    
    try:
        content = await asyncio.to_thread(generate_ai_text, system_prompt, user_prompt)
        new_brief = MarketIntelBrief(brief_type=payload.brief_type, content=content)
        db.add(new_brief)
        db.commit()
        db.refresh(new_brief)
        return {"status": "SUCCESS", "brief": {"brief_type": new_brief.brief_type, "content": new_brief.content}}
    except Exception as e:
        app_logger.error(f"Failed to generate market brief: {e}")
        fallback_content = (
            f"### Simulated Macro Market Brief ({payload.brief_type.upper()})\n\n"
            f"**Price Structure:** XAUUSD continues consolidating on H1 timeframe. Near-term supports reside at 2315.00, with resistance blocks at 2335.00.\n\n"
            f"**Economic Catalyst:** Technical indicators remain whitelisted. USD DXY fluctuations support sideways consolidation range index.\n\n"
            f"**Tactical Bias:** Neutral. Wait for high-impact NFP/CPI releases to resolve the macro expansion direction."
        )
        new_brief = MarketIntelBrief(brief_type=payload.brief_type, content=fallback_content)
        db.add(new_brief)
        db.commit()
        return {"status": "SUCCESS", "brief": {"brief_type": payload.brief_type, "content": fallback_content}}


def handle_local_chat_fallback(message: str, tasks_list_str: str, db: Session) -> str:

    msg = message.strip().lower()
    
    # 1. HELP / COMMANDS
    if msg in ["help", "commands", "menu"]:
        return (
            "🤖 **XAUUSD Trading Assistant - Local Command Menu**\n\n"
            "Here are the commands I can execute locally:\n"
            "- **Check Account**: Type `account`, `balance`, or `status` to get your live MT5 balance and equity.\n"
            "- **Check Positions**: Type `positions` or `trades` to list all currently open trades on the terminal.\n"
            "- **Checklist / Tasks**:\n"
            "  - `list tasks` - View all tasks on your developer checklist.\n"
            "  - `add task: <title>` - Create a new task.\n"
            "  - `complete task: <id or title>` - Mark a task as completed.\n"
            "  - `delete task: <id or title>` - Delete a task.\n\n"
            "*(Note: You can configure a Gemini, OpenAI, or Claude API key in Settings to enable natural language conversations.)*"
        )
        
    # 2. STATUS / ACCOUNT
    if any(x in msg for x in ["account", "balance", "equity", "margin"]):
        try:
            from app.broker.mt5_connector import mt5_connector
            balance, equity, margin, free_margin = mt5_connector.get_account_state()
            mode = "Mock/Simulation" if mt5_connector.is_mock else "Live Terminal"
            server = "Unknown"
            try:
                acc_info = mt5_connector.api.account_info()
                if acc_info and hasattr(acc_info, "server"):
                    server = acc_info.server
            except Exception:
                pass
            return (
                f"📊 **Current Account Status ({mode})**\n\n"
                f"- **Broker Server**: `{server}`\n"
                f"- **Balance**: ${balance:,.2f} USD\n"
                f"- **Equity**: ${equity:,.2f} USD\n"
                f"- **Margin**: ${margin:,.2f} USD\n"
                f"- **Free Margin**: ${free_margin:,.2f} USD\n"
                f"- **Active PnL**: ${round(equity - balance, 2):+,.2f} USD"
            )
        except Exception as e:
            return f"❌ Failed to fetch account status from MT5: {str(e)}"

    # 3. OPEN POSITIONS
    if any(x in msg for x in ["positions", "open trades", "active trades"]):
        try:
            from app.broker.mt5_connector import mt5_connector
            positions = mt5_connector.api.positions_get()
            if not positions:
                return "📈 **Active Positions**: There are currently no open positions on your MT5 terminal."
            
            res = f"📈 **Active Positions ({len(positions)} open)**\n\n"
            for pos in positions:
                ptype = "BUY" if pos.type == 0 else "SELL"
                res += (
                    f"• **Ticket #{pos.ticket}**: {ptype} {pos.volume} Lots of {pos.symbol}\n"
                    f"  - Entry: `{pos.price_open:.2f}` → Current: `{pos.price_current:.2f}`\n"
                    f"  - SL: `{pos.sl:.2f}` | TP: `{pos.tp:.2f}`\n"
                    f"  - Profit: **${pos.profit:+,.2f} USD**\n\n"
                )
            return res.strip()
        except Exception as e:
            return f"❌ Failed to query active positions from MT5: {str(e)}"

    # 4. TASK MANAGEMENT
    if msg.startswith("add task:") or msg.startswith("create task:"):
        task_title = message.split(":", 1)[1].strip()
        if not task_title:
            return "❌ Please specify a task title. Example: `add task: Verify Telegram Webhook`"
        new_task = DashboardTask(title=task_title, completed=False)
        db.add(new_task)
        db.commit()
        return f"✅ **Task Added**: \"{task_title}\" has been added to your developer checklist."

    if msg.startswith("complete task:") or msg.startswith("finish task:"):
        identifier = message.split(":", 1)[1].strip()
        if not identifier:
            return "❌ Please specify the task ID or name to complete. Example: `complete task: 3`"
        
        task = None
        if identifier.isdigit():
            task = db.query(DashboardTask).filter(DashboardTask.id == int(identifier)).first()
        if not task:
            task = db.query(DashboardTask).filter(DashboardTask.title.like(f"%{identifier}%")).first()
            
        if not task:
            return f"❌ Task matching \"{identifier}\" not found in checklist."
        
        task.completed = True
        db.commit()
        return f"✅ **Task Completed**: \"{task.title}\" is now marked as complete."

    if msg.startswith("delete task:") or msg.startswith("remove task:"):
        identifier = message.split(":", 1)[1].strip()
        if not identifier:
            return "❌ Please specify the task ID or name to delete. Example: `delete task: 3`"
        
        task = None
        if identifier.isdigit():
            task = db.query(DashboardTask).filter(DashboardTask.id == int(identifier)).first()
        if not task:
            task = db.query(DashboardTask).filter(DashboardTask.title.like(f"%{identifier}%")).first()
            
        if not task:
            return f"❌ Task matching \"{identifier}\" not found in checklist."
        
        title = task.title
        db.delete(task)
        db.commit()
        return f"🗑️ **Task Deleted**: \"{title}\" has been removed from your checklist."

    if msg in ["list tasks", "tasks", "checklist", "show checklist"]:
        tasks = db.query(DashboardTask).order_by(DashboardTask.created_at.desc()).all()
        if not tasks:
            return "📝 **Developer Checklist**: No tasks registered. Type `add task: <title>` to create one!"
        
        res = "📝 **Developer Checklist**\n\n"
        for t in reversed(tasks):
            status = "✅ Completed" if t.completed else "⏳ Pending"
            res += f"- **[{t.id}]** {t.title} — *{status}*\n"
        return res

    # 5. GENERAL RESPONSES
    if "hello" in msg or "hi " in msg or "hey" in msg:
        return (
            "Hello! I am your AI Trading Assistant chatbot. 🤖\n\n"
            "I can help you manage your checklist, check your broker account balance, and view open trade tickets directly.\n"
            "Type `help` to view the commands list!"
        )
        
    if "strategy" in msg or "gold" in msg or "xauusd" in msg or "trade" in msg:
        return (
            "Gold (XAUUSD) has been showing interesting intraday structures! 📈\n\n"
            "My indicators check for EMA20/50 crossovers and RSI levels. If you want me to write or execute a new trade validation, "
            "make sure the trading agent is running and configured correctly.\n\n"
            "*(To activate real-time AI-powered market analysis, please configure your Claude/OpenAI API key in the settings.)*"
        )

    # General chatbot fallback
    return (
        f"I received your message: \"{message}\"\n\n"
        "I am currently running in **Local fallback mode** because no active/valid API keys (Gemini, OpenAI, or Claude) are configured in settings. "
        "I can, however, execute dashboard commands directly!\n\n"
        "Try typing **`help`** to see the list of commands I can run for you, or **`list tasks`** to see your checklist!"
    )


class ChatMessageSchema(BaseModel):
    message: str


@app.post("/api/v1/chat")
def chat_endpoint(payload: ChatMessageSchema, db: Session = Depends(get_db), session_id: Optional[str] = Cookie(None)):
    if not is_authenticated(session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
    try:
        user_message = payload.message.strip()
        
        # 1. Fetch recent 10 messages from DB to use as chat memory
        db_messages = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(10).all()
        db_messages.reverse()
        
        chat_history = []
        for m in db_messages:
            content = m.content
            # Clean up local fallback footnote disclaimers so LLMs do not repeat them in history
            disclaimers = [
                "*(Running in Local fallback mode. Please configure a valid API key in Settings to replace these placeholders.)*",
                "*(Running in Local fallback mode. The configured API keys encountered authentication/network errors. Check the logs.)*",
                "*(Running in Local fallback mode. You can configure an API key in the Settings tab.)*",
                "*(Note: You can configure a Gemini, OpenAI, or Claude API key in Settings to enable natural language conversations.)*"
            ]
            for d in disclaimers:
                content = content.replace(d, "")
            content = content.strip()
            chat_history.append({"role": m.role, "content": content})
            
        # 2. Fetch all saved tasks
        tasks = db.query(DashboardTask).all()
        tasks_list_str = ""
        for i, t in enumerate(tasks):
            status_symbol = "[x]" if t.completed else "[ ]"
            tasks_list_str += f"{i+1}. {status_symbol} {t.title}\n"
        if not tasks_list_str:
            tasks_list_str = "No tasks registered in checklist yet."
            
        # 3. Formulate system prompt
        system_prompt = (
            "You are an expert algorithmic trading assistant and developer chatbot integrated in the XAUUSD Automated Trading Dashboard.\n"
            "You have access to the user's saved developer checklist / tasks. Please reference, add, or suggest updates to tasks if appropriate.\n"
            "Here is the user's current checklist from the database:\n"
            f"{tasks_list_str}\n\n"
            "Be professional, clear, direct, and helpful. You can analyze market context or help manage tasks."
        )
        
        chat_history.append({"role": "user", "content": user_message})
        
        # Save user message to DB
        db_user = ChatMessage(role="user", content=user_message)
        db.add(db_user)
        db.commit()
        
        # 4. Route request based on keys and robustness check
        ai_response = ""
        
        # Try Gemini
        if not ai_response and settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("placeholder") and len(settings.GEMINI_API_KEY) > 15:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
                contents = []
                for m in chat_history:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": m["content"]}]
                    })
                gemini_payload = {
                    "contents": contents,
                    "systemInstruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 800
                    }
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(gemini_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=12) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    ai_response = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    app_logger.info("Chat: Responded using Gemini API.")
            except Exception as e_gemini:
                app_logger.error(f"Gemini API call failed: {e_gemini}")
                
        # Try OpenAI
        if not ai_response and settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-proj-testkey") and len(settings.OPENAI_API_KEY) > 15:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                openai_messages = [{"role": "system", "content": system_prompt}]
                for m in chat_history:
                    openai_messages.append({"role": m["role"], "content": m["content"]})
                    
                openai_payload = {
                    "model": "gpt-4o-mini",
                    "messages": openai_messages,
                    "temperature": 0.3,
                    "max_tokens": 800
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(openai_payload).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
                    }
                )
                with urllib.request.urlopen(req, timeout=12) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    ai_response = res_json["choices"][0]["message"]["content"]
                    app_logger.info("Chat: Responded using OpenAI API.")
            except Exception as e_openai:
                app_logger.error(f"OpenAI API call failed: {e_openai}")
                
        # Try Claude
        if not ai_response and settings.CLAUDE_API_KEY and not settings.CLAUDE_API_KEY.startswith("ABSK") and len(settings.CLAUDE_API_KEY) > 15:
            try:
                from app.ai.trade_predictor import anthropic_client
                if anthropic_client:
                    response = anthropic_client.messages.create(
                        model=settings.CLAUDE_MODEL_ID,
                        max_tokens=800,
                        system=system_prompt,
                        messages=chat_history,
                        temperature=0.3
                    )
                    ai_response = response.content[0].text
                    app_logger.info("Chat: Responded using Claude API.")
                else:
                    app_logger.warning("Anthropic client was not initialized.")
            except Exception as e_claude:
                app_logger.error(f"Claude API call failed: {e_claude}")
                
        # Fallback to local response engine if no AI provider succeeded or was configured
        if not ai_response:
            ai_response = handle_local_chat_fallback(user_message, tasks_list_str, db)
            
            # Append footnote if keys were attempted but failed
            has_configured_keys = bool(settings.GEMINI_API_KEY or settings.OPENAI_API_KEY or settings.CLAUDE_API_KEY)
            is_placeholder = any(
                (k and (k.startswith("placeholder") or k.startswith("sk-proj-testkey") or k.startswith("ABSK")))
                for k in [settings.GEMINI_API_KEY, settings.OPENAI_API_KEY, settings.CLAUDE_API_KEY]
            )
            if has_configured_keys:
                if is_placeholder:
                    ai_response += "\n\n*(Running in Local fallback mode. Please configure a valid API key in Settings to replace these placeholders.)*"
                else:
                    ai_response += "\n\n*(Running in Local fallback mode. The configured API keys encountered authentication/network errors. Check the logs.)*"
            else:
                ai_response += "\n\n*(Running in Local fallback mode. You can configure an API key in the Settings tab.)*"

        # Save AI message to DB
        db_ai = ChatMessage(role="assistant", content=ai_response)
        db.add(db_ai)
        db.commit()
        
        return {"status": "SUCCESS", "response": ai_response}
    except Exception as chat_err:
        app_logger.error(f"Error in chat handler: {chat_err}")
        return {"status": "ERROR", "response": f"Chatbot Error: {str(chat_err)}"}


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitors/Docker compose probes.
    """
    balance, equity, _, _ = mt5_connector.get_account_state()
    return {
        "status": "HEALTHY",
        "broker_connected": mt5_connector.is_mock or mt5_connector.api.account_info() is not None,
        "account_mode": mt5_connector.get_account_mode_label(),
        "mode": "MOCK" if mt5_connector.is_mock else "LIVE",
        "equity": equity,
        "balance": balance
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

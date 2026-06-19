import sys
import os
from sqlalchemy.orm import Session

# Add the workspace root to python path so we can import app modules
sys.path.insert(0, os.path.abspath("."))

from app.database.db import SessionLocal, init_db
from app.utils.dashboard_template import render_dashboard
from app.main import fetch_live_forex_news
from app.utils.news_manager import fetch_forex_factory_news
from app.database.models import Trade, Signal, AccountSnapshot, ChatMessage, DashboardTask
from app.database.trade_history import get_latest_snapshot, get_performance_stats, get_daily_pnl, get_all_trades_json

def main():
    db = SessionLocal()
    try:
        # Fetch dummy or real data for rendering
        balance = 50000.0
        equity = 50000.0
        margin = 1000.0
        free_margin = 49000.0
        daily_dd = 0.0
        weekly_dd = 0.0
        
        latest_snap = get_latest_snapshot(db)
        if latest_snap:
            daily_dd = latest_snap.daily_drawdown
            weekly_dd = latest_snap.weekly_drawdown
            
        stats = get_performance_stats(db, days=30)
        daily_pnl = get_daily_pnl(db)
        news_events = []
        live_news = []
        
        chat_messages = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(20).all()
        chat_messages.reverse()
        chat_history_json = [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat() + "Z"} for m in chat_messages]
        
        tasks = db.query(DashboardTask).order_by(DashboardTask.created_at.desc()).all()
        tasks_json = [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
        
        recent_signals = db.query(Signal).order_by(Signal.created_at.desc()).limit(10).all()
        recent_trades = db.query(Trade).order_by(Trade.created_at.desc()).limit(10).all()
        open_trades = db.query(Trade).filter(Trade.status == "OPEN").all()
        all_closed_trades = db.query(Trade).filter(Trade.status == "CLOSED").order_by(Trade.closed_at.desc()).all()
        all_trades_json = get_all_trades_json(db)
        
        dashboard_data = {
            "project_name": "XAUUSD Trading Agent",
            "environment": "development",
            "mt5_mock": False,
            "broker_connected": True,
            "balance": balance,
            "equity": equity,
            "margin": margin,
            "free_margin": free_margin,
            "daily_drawdown": daily_dd,
            "weekly_drawdown": weekly_dd,
            "max_daily_drawdown_pct": 0.05,
            "max_weekly_drawdown_pct": 0.10,
            "risk_percent_per_trade": 0.01,
            "ai_validation_enabled": True,
            "performance_stats": stats,
            "daily_pnl": daily_pnl,
            "news_events": news_events,
            "recent_signals": recent_signals,
            "recent_trades": recent_trades,
            "open_trades": open_trades,
            "all_closed_trades": all_closed_trades,
            "all_trades_json": all_trades_json,
            "live_news": live_news,
            "chat_history": chat_history_json,
            "tasks": tasks_json,
            "mt5_login": "212105700",
            "mt5_server": "AtlasFunded-Server",
            "mt5_password": "fake_password",
            "claude_api_key": "fake_key",
            "openai_api_key": "fake_key",
            "gemini_api_key": "fake_key"
        }
        
        html = render_dashboard(dashboard_data)
        with open("rendered_dashboard.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Successfully rendered dashboard to rendered_dashboard.html")
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

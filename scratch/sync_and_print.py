import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.db import SessionLocal
from app.database.models import Trade
from app.database.trade_history import sync_trades_from_mt5
from app.broker.mt5_connector import mt5_connector

db = SessionLocal()
print("Connecting to MT5...")
if mt5_connector.connect():
    print("Connected. Synchronizing trades from MT5...")
    sync_trades_from_mt5(db)
else:
    print("Failed to connect to MT5.")

print("\nCURRENT OPEN TRADES IN DATABASE:")
open_trades = db.query(Trade).filter(Trade.status == "OPEN").all()
if open_trades:
    for t in open_trades:
        print(f"Ticket: {t.ticket} | Symbol: {t.symbol} | Type: {t.order_type} | Entry: {t.entry_price} | SL: {t.sl_price} | TP: {t.tp_price} | Profit: {t.profit} | Status: {t.status}")
else:
    print("No open trades in database.")

db.close()

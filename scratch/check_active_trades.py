import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.db import SessionLocal
from app.database.models import Trade
from app.broker.mt5_connector import mt5_connector

db = SessionLocal()
print("DATABASE TRADES:")
trades = db.query(Trade).all()
for t in trades:
    print(f"Ticket: {t.ticket}, Symbol: {t.symbol}, Status: {t.status}, Entry: {t.entry_price}, Profit: {t.profit}")

print("\nMT5 ACTIVE POSITIONS:")
if mt5_connector.connect():
    positions = mt5_connector.api.positions_get()
    print(f"Positions returned: {positions}")
    if positions:
        for p in positions:
            print(f"Ticket: {getattr(p, 'ticket', None)}, Symbol: {getattr(p, 'symbol', None)}, Type: {getattr(p, 'type', None)}, Volume: {getattr(p, 'volume', None)}, Price Open: {getattr(p, 'price_open', None)}, Profit: {getattr(p, 'profit', None)}")
else:
    print("Failed to connect to MT5")

db.close()

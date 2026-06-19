import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup path so it can import app
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database.models import Trade
from app.broker.mt5_connector import mt5_connector
from app.utils.config import settings

def main():
    print("=== Config Settings ===")
    print(f"MT5_MOCK: {settings.MT5_MOCK}")
    print(f"MT5_LOGIN: {settings.MT5_LOGIN}")
    print(f"MT5_SERVER: {settings.MT5_SERVER}")
    print(f"MT5_PATH: {settings.MT5_PATH}")
    
    # 1. Connect to MT5
    print("\n=== Connecting to MT5 Broker ===")
    conn_ok = mt5_connector.connect()
    print(f"Connection status: {conn_ok}")
    print(f"Connector is_mock: {mt5_connector.is_mock}")
    
    # 2. Get tick data
    tick = mt5_connector.get_tick_data("XAUUSD")
    print(f"XAUUSD Tick data: {tick}")
    
    # 3. Connect to DB and check open trades
    print("\n=== Open Trades from DB ===")
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        open_trades = session.query(Trade).filter(Trade.status == "OPEN").all()
        print(f"Found {len(open_trades)} open trades in DB:")
        for t in open_trades:
            print(f"Ticket: {t.ticket} | Symbol: {t.symbol} | Type: {t.order_type} | Volume: {t.volume} | Entry Price: {t.entry_price} | SL: {t.sl_price} | TP: {t.tp_price} | Profit: {t.profit} | Status: {t.status}")
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()

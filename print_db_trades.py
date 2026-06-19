import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.database.models import Trade
from app.utils.config import settings

def main():
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        trades = session.query(Trade).order_by(Trade.created_at.desc()).all()
        print(f"Total trades in DB: {len(trades)}")
        for t in trades[:10]:
            print(f"Ticket: {t.ticket} | Symbol: {t.symbol} | Type: {t.order_type} | Entry: {t.entry_price} | Exit: {t.exit_price} | Profit: {t.profit} | Status: {t.status} | Comment: {t.comment}")
    finally:
        session.close()

if __name__ == "__main__":
    main()

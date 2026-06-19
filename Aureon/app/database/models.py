"""
Database Models for XAUUSD Automated Trading System.
Defines ORM models for trades, signals, and account equity snapshots.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from app.database.db import Base
from app.utils.helpers import get_utc_now


class Trade(Base):
    """
    Represents an execution order / open or closed trade position.
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    ticket = Column(Integer, unique=True, index=True, nullable=True)  # MT5 Ticket ID
    symbol = Column(String(20), default="XAUUSD", nullable=False)
    order_type = Column(String(10), nullable=False)  # BUY or SELL
    volume = Column(Float, nullable=False)  # Lot size
    entry_price = Column(Float, nullable=False)
    sl_price = Column(Float, nullable=False)
    tp_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    profit = Column(Float, default=0.0)  # PnL in account currency
    swap = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    status = Column(String(20), default="OPEN", index=True)  # OPEN, CLOSED, FAILED, CANCELLED
    comment = Column(String(255), nullable=True)
    magic_number = Column(Integer, nullable=False)
    
    # AI Confluence Metrics
    ai_confidence = Column(Float, nullable=True)
    ai_validation_reasoning = Column(Text, nullable=True)

    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    closed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Trade ticket={self.ticket} symbol={self.symbol} type={self.order_type} profit={self.profit}>"


class Signal(Base):
    """
    Represents an incoming TradingView signal and its validation status.
    """
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # BUY or SELL
    timeframe = Column(String(10), default="H1", nullable=False)
    price = Column(Float, nullable=False)
    
    # Technical Indicators captured at alert time
    rsi = Column(Float, nullable=True)
    ema_20 = Column(Float, nullable=True)
    ema_50 = Column(Float, nullable=True)
    atr = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    avg_volume = Column(Float, nullable=True)
    market_structure = Column(String(20), nullable=True)  # BULLISH or BEARISH

    raw_payload = Column(Text, nullable=True)  # Store original TV JSON string
    processed = Column(Boolean, default=False)
    action_taken = Column(String(30), default="PENDING")  # EXECUTED, REJECTED_RISK, REJECTED_AI, ERROR
    reason = Column(String(255), nullable=True)  # Explanation of why it was rejected/failed
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        return f"<Signal direction={self.direction} symbol={self.symbol} action={self.action_taken}>"


class AccountSnapshot(Base):
    """
    Maintains historical snapshots of account performance metrics.
    Used for drawdown protection calculations and reports.
    """
    __tablename__ = "account_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    margin = Column(Float, default=0.0)
    free_margin = Column(Float, default=0.0)
    daily_drawdown = Column(Float, default=0.0)
    weekly_drawdown = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=get_utc_now, index=True, nullable=False)

    def __repr__(self):
        return f"<AccountSnapshot balance={self.balance} equity={self.equity} time={self.timestamp}>"


class ChatMessage(Base):
    """
    Represents an AI chatbot conversation message.
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(10), nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        return f"<ChatMessage role={self.role} content={self.content[:30]}>"


class DashboardTask(Base):
    """
    Represents a checklist task saved in the developer dashboard.
    """
    __tablename__ = "dashboard_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        return f"<DashboardTask title={self.title} completed={self.completed}>"


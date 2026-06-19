"""
Configuration Module for XAUUSD Automated Trading System.
Uses pydantic-settings to manage and validate environment variables.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Inject environment variables from .env into os.environ
load_dotenv(os.path.join(BASE_DIR, ".env"))



class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    """
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General Settings
    ENVIRONMENT: str = Field(default="development", description="System environment (development/production)")
    DEBUG: bool = Field(default=True, description="Enable debug level logs")
    PROJECT_NAME: str = Field(default="AUREON", description="Name of the application")
    PORT: int = Field(default=8000, description="FastAPI Server port")
    HOST: str = Field(default="0.0.0.0", description="FastAPI Server host")
    DASHBOARD_USERNAME: str = Field(default="admin", description="Dashboard Admin Username")
    DASHBOARD_PASSWORD: str = Field(default="admin", description="Dashboard Admin Password")

    # Security
    WEBHOOK_SECRET: str = Field(
        default="SUPER_SECRET_TOKEN_CHANGE_ME",
        description="Secret key to validate TradingView webhook payload headers"
    )
    # Default TradingView Webhook IP Whitelist (AWS regions for TV alerts)
    ALLOWED_IPS: List[str] = Field(
        default=[
            "52.89.214.238",
            "34.212.75.30",
            "54.112.32.21",
            "54.112.32.22",
            "127.0.0.1",
            "localhost"
        ],
        description="List of IPs allowed to send webhook requests"
    )

    # MetaTrader 5 Configuration
    MT5_LOGIN: int = Field(default=0, description="MT5 Account Number")
    MT5_PASSWORD: str = Field(default="", description="MT5 Investor/Trader Password")
    MT5_SERVER: str = Field(default="", description="MT5 Broker Server Name")
    MT5_PATH: Optional[str] = Field(default=None, description="Path to terminal64.exe (optional)")
    MT5_MOCK: bool = Field(default=True, description="Use Mock Broker instead of connecting to real MT5")
    MT5_MAGIC_NUMBER: int = Field(default=20260609, description="Magic number to identify agent trades")

    # Database Configuration
    DATABASE_URL: str = Field(
        default=f"sqlite:///{BASE_DIR}/trading.db",
        description="Database connection URL (SQLite or PostgreSQL)"
    )

    # Risk Management Settings
    RISK_PERCENT_PER_TRADE: float = Field(default=0.01, description="Percentage of balance to risk per trade (e.g. 0.01 = 1%)")
    MAX_TRADES_PER_DAY: int = Field(default=3, description="Maximum number of trade executions allowed per day")
    MAX_DAILY_DRAWDOWN_PCT: float = Field(default=0.05, description="Maximum allowable daily drawdown (e.g. 0.05 = 5%)")
    MAX_WEEKLY_DRAWDOWN_PCT: float = Field(default=0.10, description="Maximum allowable weekly drawdown (e.g. 0.10 = 10%)")
    MAX_SPREAD_POINTS: int = Field(default=50, description="Maximum allowed spread in points for Gold (e.g. 50 points = 5.0 pips / $0.50)")
    MAX_SLIPPAGE_POINTS: int = Field(default=30, description="Maximum allowable slippage in points for order execution")
    
    # Session Filtering (UTC Hours)
    SESSION_START_HOUR: int = Field(default=7, description="UTC Hour to start trading (e.g. London opening prep)")
    SESSION_END_HOUR: int = Field(default=21, description="UTC Hour to stop trading (e.g. New York close prep)")

    # Claude AI Validation Settings
    CLAUDE_API_KEY: Optional[str] = Field(default=None, description="Anthropic API Key")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Gemini API Key")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS Access Key for Bedrock")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS Secret Key for Bedrock")
    AWS_REGION: str = Field(default="us-east-1", description="AWS Bedrock Region")
    
    AI_VALIDATION_ENABLED: bool = Field(default=False, description="Enable/Disable Claude AI trade validation")
    AI_PROVIDER: str = Field(default="anthropic", description="AI Provider: 'anthropic' or 'bedrock'")
    CLAUDE_MODEL_ID: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Model identifier for Anthropic Claude validation"
    )
    MIN_CONFIDENCE_SCORE: float = Field(default=0.70, description="Minimum confidence score needed from AI (0.0 to 1.0)")

    # Telegram Notification Settings
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, description="Telegram Bot API Token")
    TELEGRAM_CHAT_ID: Optional[str] = Field(default=None, description="Telegram Channel/Chat ID")
    TELEGRAM_ENABLED: bool = Field(default=False, description="Enable/Disable Telegram notifications")


# Instantiate settings singleton
settings = Settings()

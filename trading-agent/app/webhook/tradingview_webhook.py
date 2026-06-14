"""
TradingView Webhook Router Module.
Receives signal payloads, validates source IP addresses, and authenticates secret tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.strategy.signal_processor import process_incoming_signal
from app.utils.config import settings
from app.utils.logger import app_logger

router = APIRouter()


class TradingViewSignal(BaseModel):
    """
    Pydantic model representing expected JSON payload from TradingView alerts.
    """
    secret: str = Field(description="Secret passphrase to authenticate the payload source.")
    symbol: str = Field(default="XAUUSD", description="Symbol name (e.g. XAUUSD)")
    direction: str = Field(description="Trade direction: BUY or SELL")
    timeframe: str = Field(default="H1", description="Signal timeframe (e.g. M15, H1, H4)")
    price: float = Field(description="Current market price at the alert moment")


def verify_client_ip(request: Request):
    """
    Validates client IP address against settings.ALLOWED_IPS whitelist.
    Handles proxy headers (X-Forwarded-For) if running behind Nginx/Cloudflare.
    """
    # Check X-Forwarded-For header if behind reverse proxy
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # Get client IP (first address in proxy chain list)
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Fallback to direct client host
        client_ip = request.client.host if request.client else None

    if not client_ip:
        app_logger.warning("Rejecting request: client IP address resolved to None.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client IP resolution failed."
        )

    # Bypass whitelist check if '*' is configured (for open local tests, not recommended for prod)
    if "*" in settings.ALLOWED_IPS:
        return

    # Check if client IP is whitelisted
    if client_ip not in settings.ALLOWED_IPS:
        app_logger.warning(f"Unauthorized Webhook Access Attempt blocked. Client IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden: Client IP {client_ip} is not in the whitelist."
        )


@router.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def handle_tradingview_alert(
    payload: TradingViewSignal,
    request: Request,
    db: Session = Depends(get_db),
    _ip_check = Depends(verify_client_ip)
):
    """
    Endpoint receiving TradingView webhook alerts.
    Authenticates secret passphrase, parses signal indicators, and hands off execution.
    """
    # Authenticate webhook secret passphrase
    if payload.secret != settings.WEBHOOK_SECRET:
        app_logger.warning(f"Invalid secret passphrase submitted by client.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Webhook token mismatch."
        )

    # Convert Pydantic object back to dict for processing pipeline
    signal_data = payload.model_dump()
    
    # Hand off signal to processing pipeline in a background task or process directly
    # As it calculates indicators and sends order synchronously, we process it and return result.
    try:
        result = await process_incoming_signal(db, signal_data)
        if result["status"] == "EXECUTED":
            return {
                "message": "Signal processed and executed.",
                "ticket": result.get("ticket"),
                "price": result.get("price")
            }
        else:
            return {
                "message": f"Signal processed but not executed: {result.get('reason')}"
            }
    except Exception as e:
        app_logger.error(f"Error handling webhook signal: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signal processing error: {str(e)}"
        )

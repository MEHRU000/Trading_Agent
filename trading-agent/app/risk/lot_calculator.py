"""
Lot Sizing Calculator.
Computes position sizing dynamically to restrict risk to 1% per trade.
"""

from app.utils.config import settings
from app.utils.logger import app_logger
from app.utils.helpers import round_lot_size, calculate_sl_distance_in_points


def calculate_lot_size(
    account_balance: float,
    entry_price: float,
    sl_price: float,
    symbol: str = "XAUUSD"
) -> float:
    """
    Computes lot size based on account balance, entry price, stop loss, and risk parameters.
    
    Formula:
        Risk Amount = Balance * Risk Percent (1%)
        SL Distance = abs(Entry - SL) * 100 (for Gold point scale of 0.01)
        Value of 1 point for 1 lot of XAUUSD = 1.00 USD
        Lot Size = Risk Amount / (SL Distance * 1.00)
    
    Args:
        account_balance: Current account balance (USD)
        entry_price: Planned entry price
        sl_price: Planned stop loss price
        symbol: Instrument symbol
        
    Returns:
        float: Rounded position size in lots
    """
    if sl_price == 0.0 or entry_price == sl_price:
        app_logger.warning("Stop loss price is invalid or matches entry. Returning minimum lot size.")
        return 0.01

    # Calculate cash risk budget
    risk_amount = account_balance * settings.RISK_PERCENT_PER_TRADE
    
    # Calculate SL distance in broker points
    sl_points = calculate_sl_distance_in_points(entry_price, sl_price)
    
    if sl_points <= 0:
        app_logger.warning(f"Calculated SL distance points {sl_points} is invalid. Returning minimum lot size.")
        return 0.01

    # Point value is $1.00 USD per 1 lot per 1 point for XAUUSD (Gold contract size = 100)
    # 1 standard lot = 100 units. 1 point move (0.01) = 100 * 0.01 = $1.00 PnL.
    point_value_per_lot = 1.00
    
    # Calculate raw position size
    raw_lot = risk_amount / (sl_points * point_value_per_lot)
    
    # Round to conform with broker lot step parameters (normally step 0.01, min 0.01)
    final_lot = round_lot_size(raw_lot)
    
    app_logger.info(
        f"Lot Calculation Details - Balance: {account_balance:.2f} USD | Risk Budget: {risk_amount:.2f} USD "
        f"| SL Price: {sl_price:.2f} | SL Distance: {sl_points:.0f} points | Raw Lots: {raw_lot:.4f} | Final Lots: {final_lot}"
    )
    
    return final_lot

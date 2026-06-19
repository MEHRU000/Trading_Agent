"""
Unit Tests for Risk Management Calculations.
"""

import pytest
from app.risk.lot_calculator import calculate_lot_size
from app.utils.helpers import round_lot_size, calculate_sl_distance_in_points


def test_round_lot_size():
    # Test standard lot rounding values
    assert round_lot_size(0.123) == 0.12
    assert round_lot_size(0.004) == 0.01  # Min lot limit
    assert round_lot_size(150.0) == 100.0  # Max lot limit
    assert round_lot_size(0.555) == 0.56


def test_calculate_sl_distance_in_points():
    # Gold scale is normally 2 digits. 1 point = 0.01 price diff.
    assert calculate_sl_distance_in_points(2000.00, 1990.00) == 1000.0  # 10.00 price diff = 1000 points
    assert calculate_sl_distance_in_points(2000.00, 2005.50) == 550.0   # 5.50 price diff = 550 points


def test_calculate_lot_size():
    # Setup test parameters
    balance = 10000.0
    risk_pct = 0.01  # 1% of 10000 = $100 risk amount
    
    # 1. Test case: Buy Entry at 2000.00, SL at 1990.00 (1000 points SL)
    # Risk Amount = 100 USD. SL distance = 1000 points.
    # Point Value = 1.00 USD. Risk per Lot = 1000 * 1.00 = 1000 USD.
    # Lot Size = 100 / 1000 = 0.10 standard lots.
    lot1 = calculate_lot_size(balance, entry_price=2000.00, sl_price=1990.00)
    assert lot1 == 0.10

    # 2. Test case: Entry at 2000.00, SL at 1995.00 (500 points SL)
    # Risk Amount = 100 USD. SL distance = 500 points.
    # Lot Size = 100 / 500 = 0.20 standard lots.
    lot2 = calculate_lot_size(balance, entry_price=2000.00, sl_price=1995.00)
    assert lot2 == 0.20

    # 3. Test case: Entry at 2000.00, SL at 2000.00 (invalid SL)
    # Should fallback to minimum lot size (0.01)
    lot3 = calculate_lot_size(balance, entry_price=2000.00, sl_price=2000.00)
    assert lot3 == 0.01

"""
Unit Tests for Trade Synchronization and Connection Failure Handling.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch
from app.database.models import Trade
from app.main import position_sync_loop


@pytest.mark.anyio
async def test_position_sync_loop_connection_failure():
    # Mock database session
    mock_db = MagicMock()
    mock_trade = Trade(
        ticket=12345,
        symbol="XAUUSD",
        order_type="BUY",
        volume=0.03,
        entry_price=2000.0,
        status="OPEN"
    )
    
    # Mock mt5_connector api
    mock_api = MagicMock()
    mock_api.positions_get.return_value = None  # Simulates MT5 connection failure/timeout
    mock_api.terminal_info.return_value = False
    
    with patch("app.main.SessionLocal", return_value=mock_db), \
         patch("app.main.get_open_trades", return_value=[mock_trade]), \
         patch("app.database.trade_history.sync_trades_from_mt5") as mock_sync, \
         patch("app.broker.mt5_connector.mt5_connector.connect", return_value=True), \
         patch("app.broker.mt5_connector.mt5_connector.api", mock_api), \
         patch("app.main.update_trade_by_ticket") as mock_update_trade, \
         patch("asyncio.sleep", side_effect=asyncio.CancelledError):
        
        # Run the loop. It should raise CancelledError on the sleep, terminating the loop
        with pytest.raises(asyncio.CancelledError):
            await position_sync_loop()
            
        # Since positions_get returned None, it should have hit the failure branch and NEVER called update_trade_by_ticket
        mock_update_trade.assert_not_called()
        

@pytest.mark.anyio
async def test_position_sync_loop_position_closed():
    # Mock database session
    mock_db = MagicMock()
    mock_trade = Trade(
        ticket=12345,
        symbol="XAUUSD",
        order_type="BUY",
        volume=0.03,
        entry_price=2000.0,
        tp_price=2010.0,
        status="OPEN"
    )
    
    # Mock mt5_connector api
    mock_api = MagicMock()
    # Return empty list of positions (meaning position is closed)
    mock_api.positions_get.return_value = []
    mock_api.terminal_info.return_value = True
    
    # Mock history deal query
    mock_deal = MagicMock()
    mock_deal.entry = 1
    mock_deal.price = 2010.0
    mock_deal.profit = 30.0
    mock_api.history_deals_get.return_value = [mock_deal]
    
    with patch("app.main.SessionLocal", return_value=mock_db), \
         patch("app.main.get_open_trades", return_value=[mock_trade]), \
         patch("app.database.trade_history.sync_trades_from_mt5") as mock_sync, \
         patch("app.broker.mt5_connector.mt5_connector.connect", return_value=True), \
         patch("app.broker.mt5_connector.mt5_connector.api", mock_api), \
         patch("app.main.update_trade_by_ticket") as mock_update_trade, \
         patch("app.notifications.alert_manager.AlertManager.notify_close_trade") as mock_notify, \
         patch("asyncio.sleep", side_effect=asyncio.CancelledError):
        
        with pytest.raises(asyncio.CancelledError):
            await position_sync_loop()
            
        # Verify it queried deals with position=ticket
        mock_api.history_deals_get.assert_called_with(position=12345)
        
        # Verify it updated database trade record as CLOSED
        mock_update_trade.assert_called_once()
        args, _ = mock_update_trade.call_args
        assert args[1] == 12345  # ticket
        assert args[2]["status"] == "CLOSED"
        assert args[2]["exit_price"] == 2010.0
        assert args[2]["profit"] == 30.0
        assert "Take Profit Hit" in args[2]["comment"]


def test_mock_mt5_sl_tp_close():
    from app.broker.mt5_connector import MockMT5
    
    # 1. Reset mock state
    MockMT5._positions.clear()
    MockMT5._closed_deals.clear()
    MockMT5._balance = 10000.0
    MockMT5._mock_last_price = 2000.0
    
    # 2. Open BUY position
    MockMT5.order_send({
        "action": MockMT5.TRADE_ACTION_DEAL,
        "symbol": "XAUUSD",
        "volume": 0.1,
        "type": MockMT5.ORDER_TYPE_BUY,
        "price": 2000.0,
        "sl": 1990.0,
        "tp": 2020.0
    })
    
    # Ensure position is active
    positions = MockMT5.positions_get(symbol="XAUUSD")
    assert len(positions) == 1
    ticket = positions[0].ticket
    
    # 3. Fluctuate price to hit SL (e.g. 1989.0)
    MockMT5._mock_last_price = 1989.0
    
    # Check SL trigger
    MockMT5._check_sl_tp()
    
    # Check position closed
    active_positions = MockMT5.positions_get(symbol="XAUUSD")
    assert len(active_positions) == 0
    
    # Verify deal exists in history with correct profit
    deals = MockMT5.history_deals_get(position=ticket)
    assert len(deals) == 2  # Entry and Exit
    exit_deal = [d for d in deals if d.entry == 1][0]
    assert exit_deal.price == 1990.0  # Exited at SL price
    assert exit_deal.profit == -100.0  # (1990 - 2000) * 0.1 * 100 = -100
    assert "Stop Loss Hit" in exit_deal.comment


import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app, get_db
from app.database.models import TradeJournal, PortfolioAccount, AICoachEvaluation, MarketIntelBrief, Trade

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture(autouse=True)
def override_db_dependency(mock_db_session):
    app.dependency_overrides[get_db] = lambda: mock_db_session
    yield
    app.dependency_overrides.pop(get_db, None)

@patch("app.main.is_authenticated", return_value=True)
def test_journal_endpoints(mock_auth, mock_db_session):
    # 1. Test GET /api/v1/journal
    mock_journal = TradeJournal(
        id=1,
        trade_ticket=1001,
        setup_type="Breakout",
        emotion="Calm",
        notes="Clean notes",
        lessons_learned="No mistakes",
        screenshot_url="http://img.com"
    )
    mock_journal.created_at = datetime.utcnow()

    mock_db_session.query.return_value.order_by.return_value.all.return_value = [mock_journal]
    
    response = client.get("/api/v1/journal")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["trade_ticket"] == 1001
    assert data[0]["setup_type"] == "Breakout"

    # 2. Test POST /api/v1/journal
    mock_db_session.query.return_value.filter.return_value.first.return_value = None # new entry
    
    payload = {
        "trade_ticket": 1002,
        "setup_type": "Retest",
        "emotion": "Confident",
        "notes": "Retest of EMA50",
        "lessons_learned": "Great exit execution",
        "screenshot_url": "http://image.png"
    }
    response = client.post("/api/v1/journal", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "SUCCESS"
    assert "created successfully" in res_data["message"]


@patch("app.main.is_authenticated", return_value=True)
def test_portfolio_endpoints(mock_auth, mock_db_session):
    # 1. Test GET /api/v1/portfolio/accounts
    mock_acc = PortfolioAccount(
        id=1,
        account_name="Funded Acc 1",
        login_id=50001,
        server="DemoServer",
        balance=50000.0,
        equity=50000.0,
        is_mock=True,
        is_active=True
    )
    mock_db_session.query.return_value.all.return_value = [mock_acc]
    
    response = client.get("/api/v1/portfolio/accounts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["account_name"] == "Funded Acc 1"
    assert data[0]["login_id"] == 50001

    # 2. Test POST /api/v1/portfolio/accounts
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    
    payload = {
        "account_name": "Funded Acc 2",
        "login_id": 50002,
        "password": "investor_pass",
        "server": "DemoServer2",
        "balance": 10000.0
    }
    response = client.post("/api/v1/portfolio/accounts", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "SUCCESS"

    # 3. Test DELETE /api/v1/portfolio/accounts/{account_id}
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_acc
    
    response = client.delete("/api/v1/portfolio/accounts/1")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "SUCCESS"
    assert res_data["message"] == "Account unlinked."


@patch("app.main.is_authenticated", return_value=True)
def test_ai_coach_endpoints(mock_auth, mock_db_session):
    # 1. Test GET /api/v1/ai-coach/evaluations
    mock_eval = AICoachEvaluation(
        id=1,
        trade_ticket=1001,
        won_lost_reason="Win",
        mistakes="None",
        strengths="Patience",
        risk_observations="Perfect sizing",
        improvements="None"
    )
    mock_eval.created_at = datetime.utcnow()

    mock_db_session.query.return_value.order_by.return_value.all.return_value = [mock_eval]
    
    response = client.get("/api/v1/ai-coach/evaluations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["trade_ticket"] == 1001

    # 2. Test POST /api/v1/ai-coach/evaluate/{ticket}
    mock_trade = Trade(
        ticket=1001,
        symbol="XAUUSD",
        order_type="BUY",
        volume=0.1,
        entry_price=2300.0,
        exit_price=2310.0,
        sl_price=2290.0,
        tp_price=2320.0,
        profit=100.0,
        status="CLOSED"
    )
    mock_trade.created_at = datetime.utcnow() - timedelta(minutes=30)
    mock_trade.closed_at = datetime.utcnow()

    mock_db_session.query.return_value.filter.return_value.first.side_effect = [
        mock_trade,  # for trade lookup
        None,        # for existing evaluation lookup (None = not yet evaluated)
        None,        # for journal lookup
        None         # for signal lookup
    ]
    
    with patch("app.main.generate_ai_text") as mock_ai:
        mock_ai.return_value = '{"won_lost_reason": "Win", "mistakes": "None", "strengths": "Patience", "risk_observations": "Good size", "improvements": "None"}'
        
        response = client.post("/api/v1/ai-coach/evaluate/1001")
        assert response.status_code == 200
        res_data = response.json()
        assert res_data["status"] == "SUCCESS"
        assert res_data["evaluation"]["won_lost_reason"] == "Win"


@patch("app.main.is_authenticated", return_value=True)
def test_market_intel_endpoints(mock_auth, mock_db_session):
    # 1. Test GET /api/v1/market-intel/brief
    mock_brief = MarketIntelBrief(
        id=1,
        brief_type="daily",
        content="Bullish structure holds."
    )
    mock_brief.created_at = datetime.utcnow()

    mock_db_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_brief]
    
    response = client.get("/api/v1/market-intel/brief")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["brief_type"] == "daily"
    assert data[0]["content"] == "Bullish structure holds."

    # 2. Test POST /api/v1/market-intel/brief
    with patch("app.main.generate_ai_text") as mock_ai, \
         patch("app.main.fetch_forex_factory_news") as mock_news, \
         patch("app.main.mt5_connector.get_tick_data", return_value=(2320.0, 2321.0)):
        
        mock_ai.return_value = "Daily market intelligence outlook report."
        mock_news.return_value = []
        
        payload = {
            "brief_type": "daily"
        }
        response = client.post("/api/v1/market-intel/brief", json=payload)
        assert response.status_code == 200
        res_data = response.json()
        assert res_data["status"] == "SUCCESS"
        assert res_data["brief"]["brief_type"] == "daily"
        assert res_data["brief"]["content"] == "Daily market intelligence outlook report."

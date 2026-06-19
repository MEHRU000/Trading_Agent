# Production-Grade XAUUSD (Gold) Automated Trading System

This platform is a fully modular algorithmic trading system built from scratch in Python. It is designed to run 24/7 on a Windows VPS or local workstation, receiving signals from TradingView alerts via FastAPI webhooks, applying strict multi-layer risk management, validating trade confluence using Claude AI (Anthropic/AWS Bedrock), and executing orders on MetaTrader 5 (MT5).

---

## Architecture Overview

```
                          ┌───────────────────────┐
                          │  TradingView Alert    │
                          └──────────┬────────────┘
                                     │ (JSON Webhook)
                                     ▼
                          ┌───────────────────────┐
                          │    FastAPI Server     │◄─── [Security Whitelist Check]
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │   Signal Processor    │
                          └────┬──────────────┬───┘
                               │              │
        [Calculates indicators │              │ [Calculates structure]
         EMA/RSI/ATR via df]   │              │
                               ▼              ▼
                          ┌───────────────────────┐
                          │   Confluence Guard    │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │   Risk Manager Gate   │◄─── [Session / Spread / Duplicate / Limit Checks]
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │  Claude AI Confluence │◄─── [Checks technical setups and context]
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │   Lot Size Calculator │◄─── [Dynamic 1% cash risk sizing]
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌───────────────────────┐
                          │  MT5 Execution Dealer │◄─── [Active trailing stops & positions tracking]
                          └────┬──────────────┬───┘
                               │              │
                               ▼              ▼
                    ┌─────────────┐        ┌─────────────┐
                    │ Telegram Bot│        │ SQLite DB   │
                    └─────────────┘        └─────────────┘
```

---

## Project Structure

```
trading-agent/
│
├── app/
│   ├── main.py                    # Application lifecycles and background loops
│   │
│   ├── strategy/
│   │   ├── signal_processor.py    # Coordinates data, strategy checks, AI, and order placing
│   │   ├── indicators.py          # EMA 20/50, RSI 14, ATR 14 using Pandas
│   │   ├── market_structure.py    # Swings peaks highs/lows structures (BOS)
│   │   ├── xauusd_strategy.py     # Strategy rules evaluate logic
│   │   └── backtester.py          # Backtester simulation engine
│   │
│   ├── broker/
│   │   ├── mt5_connector.py       # Live MT5 terminal connection & Mock simulations
│   │   ├── order_manager.py       # Placing BUY/SELL orders & modifying targets
│   │   └── position_manager.py    # Trailing stop calculations & positions tracking
│   │
│   ├── ai/
│   │   ├── claude_analyzer.py     # Anthropic/AWS Bedrock integration client
│   │   ├── market_reasoning.py    # Formulates rich markdown prompts for Claude
│   │   └── trade_predictor.py     # Triggers AI predictions and manages OpenAI/Claude APIs
│   │
│   ├── risk/
│   │   ├── risk_manager.py        # Safety validation gateway
│   │   ├── lot_calculator.py      # Sizing lot calculations (1% account balance)
│   │   └── drawdown_protection.py # Daily/weekly drawdown monitors
│   │
│   ├── webhook/
│   │   └── tradingview_webhook.py # Ingests TV HTTP POST alerts
│   │
│   ├── notifications/
│   │   ├── telegram_bot.py        # Asynchronous bot message sender
│   │   └── alert_manager.py       # Formats HTML notification templates
│   │
│   ├── database/
│   │   ├── db.py                  # SQLAlchemy engine & session generators
│   │   ├── models.py              # DB schemas (Trade, Signal, Snapshot)
│   │   └── trade_history.py       # CRUD operations & performance statistics
│   │
│   └── utils/
│       ├── config.py              # Pydantic Settings loaders
│       ├── logger.py              # Rotating file and console logger
│       ├── helpers.py             # Rounding, conversions, session time helper
│       ├── news_manager.py        # Fetches economic calendar and news events
│       └── dashboard_template.py  # Render dashboard templates and UI layouts
│
├── tests/                         # Unit tests directory (test_risk, test_strategy, test_sync)
├── logs/                          # System log output directory
├── trading.db                     # Persistent SQLite database file
├── Dockerfile                     # Containerization instructions
├── docker-compose.yml             # Docker infrastructure setup
├── requirements.txt               # Dependencies listing
├── check_rendered_html.py         # Helper script to test rendered HTML templates
├── parse_transcript.py            # Log parser script
├── rendered_dashboard.html        # Rendered HTML dashboard preview
└── README.md                      # Project documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.12 or newer.
- MetaTrader 5 Terminal installed (required for live execution).
- Windows OS (if executing live trades on MT5). Linux/Docker is fully supported for testing and backtesting utilizing the built-in **Mock Broker Fallback**.

### Virtual Environment Setup
1. Clone or copy the project files to your directory.
2. Initialize virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
4. Install package dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure environment variables in `.env` (refer to the [Configuration Guide](#configuration-guide-env)).

---

## Running the Server

To start the FastAPI server locally:

### Option 1: Running as a Python module (Recommended)
From the project root directory, run:
```bash
python -m app.main
```
This is the recommended method because running Python as a module automatically adds the root directory to the search path (`sys.path`), preventing `ModuleNotFoundError: No module named 'app'`.

### Option 2: Running with Uvicorn CLI
Alternatively, you can launch the application directly using the Uvicorn CLI:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 7999 --reload
```

### Option 3: Running the script file directly
If you want to run the script file directly via `python app/main.py`, you must set the `PYTHONPATH` environment variable so Python knows where to locate the `app` package:
- **Windows (PowerShell)**:
  ```powershell
  $env:PYTHONPATH="."
  python app/main.py
  ```
- **Windows (Command Prompt)**:
  ```cmd
  set PYTHONPATH=.
  python app/main.py
  ```
- **Linux / macOS**:
  ```bash
  PYTHONPATH=. python app/main.py
  ```

Once started, the developer dashboard will be accessible at: `http://localhost:7999` (or the port specified in your `.env` file).

---

## Deployment Guide

Deploying this automated trading system involves two main environments depending on whether you want to execute live orders on a broker account or run in simulation (mock) mode.

### 1. Live Deployment (Windows VPS)
Because the `MetaTrader5` Python library interacts directly with the desktop MetaTrader 5 terminal, **live execution requires a Windows environment** where the MT5 client is installed and logged in.

#### Step 1: VPS Provisioning
- Obtain a Windows Server VPS (recommended: 2+ vCPUs, 4GB+ RAM) located near your broker's server (e.g., London or New York) to minimize execution latency.

#### Step 2: Install Prerequisites
- Download and install **Python 3.12+**. Make sure to check "Add Python to PATH" during installation.
- Download and install the **MetaTrader 5 Terminal** from your broker. Log in to your trading account, check "Allow Algorithmic Trading", and keep the MT5 terminal running 24/7.

#### Step 3: Application Setup
- Copy or clone the project folder to the VPS.
- Create a virtual environment, activate it, and run `pip install -r requirements.txt`.
- Configure environment variables in `.env`. Set `MT5_MOCK=false` and input your MT5 login credentials (`MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER`).

#### Step 4: Process Management (24/7 Runtime)
To ensure the FastAPI server runs continuously in the background and restarts automatically on crash or server reboot, use a process manager like **PM2**:
1. Install [Node.js](https://nodejs.org/).
2. Open PowerShell as Administrator and install PM2 globally:
   ```bash
   npm install pm2 -g
   ```
3. Start the trading agent:
   ```bash
   pm2 start "python -m app.main" --name "trading-agent"
   ```
4. Save the PM2 list to persist across reboots:
   ```bash
   pm2 save
   ```

#### Step 5: Webhook Routing & Security
- To receive alerts from TradingView, expose port `7999` (or your configured port).
- Set up a reverse proxy like **Nginx** or use **IIS** to handle SSL (HTTPS) traffic.
- Ensure the `ALLOWED_IPS` list in your `.env` contains TradingView's webhook IP ranges to prevent unauthorized requests, and set a long, secure `WEBHOOK_SECRET`.

### 2. Simulation / Mock Deployment (Docker / Linux Cloud)
If you do not require live MT5 execution (e.g., for backtesting, demoing, or running paper trading in mock simulation mode), you can deploy the system to any standard Linux server using Docker.

Make sure `MT5_MOCK=true` is set in your `.env` file before running.

#### Deploy with Docker Compose:
```bash
docker-compose up -d --build
```
This builds the container image and runs the FastAPI server in the background.

- **Ports**: By default, Docker maps the container's port `8000` to port `8000` on the host machine (configured in `docker-compose.yml`). You can access the dashboard at `http://your-server-ip:8000`.
- **Logs**: Monitor system logs with:
  ```bash
  docker-compose logs -f
  ```
- **Persistency**: The container mounts `./logs` and `./data` to the host directory to persist application logs and the SQLite `trading.db` file.
### MetaTrader 5 Broker Connection & Account Sync

The platform features a dual-tab **MT5 Broker Login** interface. This enables developers and traders to connect directly to any broker (such as AtlasFunded, FTMO, or standard retail brokers like IC Markets) right from the web login page or settings panel.

#### Connecting to a Live MT5 Account
1. Open the dashboard login page at `http://localhost:8000/login`.
2. Select the **MT5 Broker Login** tab.
3. Input your **MT5 Login ID** (e.g. `212105700`), **MT5 Password** (Investor/Master password), and your broker's **MT5 Server** (e.g., `AtlasFunded-Server`).
4. Enter the **Admin Verification Password** (corresponds to the `DASHBOARD_PASSWORD` configured in your `.env` file) and submit.
5. The system will securely update the `.env` settings, initiate a connection with the local MT5 terminal, and automatically download your historical deals list.

#### Fixing History Counts & Re-Syncing
If the local database contains stale mock records (e.g., showing 34/35 trades instead of your actual 19 trades):
1. Navigate to the **System Settings** panel (the settings icon in the sidebar).
2. Scroll down to **Database & History Maintenance**.
3. Click **🧹 Clear History & Re-Sync**. This will purge all local mock entries from the SQLite database, retrieve a clean list of the last 30 days of actual executions from the connected MT5 account, and create a fresh balance/equity snapshot.

---

## Configuration Guide (.env)

| Environment Key | Default Value | Description |
| :--- | :--- | :--- |
| `MT5_MOCK` | `true` | Set to `false` to connect to a real MetaTrader 5 client. |
| `WEBHOOK_SECRET` | `SUPER_SECRET_TOKEN_CHANGE_ME` | Custom token that TradingView alerts must include for validation. |
| `ALLOWED_IPS` | `["52.89.214.238", ...]` | IP whitelist for incoming alerts. |
| `AI_VALIDATION_ENABLED` | `false` | Enable/Disable Claude AI verification before executions. |
| `AI_PROVIDER` | `anthropic` | Set to `anthropic` or `bedrock`. |
| `TELEGRAM_ENABLED` | `true` | Set to `true` to dispatch transaction logs to Telegram. |

---

## TradingView Integration Setup

Configure your TradingView Alert strategy to send an HTTP POST request to your webhook endpoint:
`http://your-server-ip:8000/api/v1/webhook`

### Webhook JSON Payload Schema
The JSON payload must strictly match the following schema:

```json
{
  "secret": "SUPER_SECRET_TOKEN_CHANGE_ME",
  "symbol": "XAUUSD",
  "direction": "BUY",
  "timeframe": "H1",
  "price": 2005.50
}
```

*Replace `direction` with `SELL` for short setups, and make sure `secret` matches the value configured in your `.env` file.*

---

## Running the Backtester

The platform includes a robust backtester to simulate strategy rules on historical M15 or H1 OHLCV candlestick data downloaded in CSV format.

1. Ensure your historical CSV file includes the following header columns: `datetime`, `open`, `high`, `low`, `close`, `volume`.
2. Place your CSV in the project folder (e.g., `data/XAUUSD_H1_2025.csv`).
3. Run the backtester via Python terminal (Create a scratch script or invoke the runner):
   ```python
   # Example script to run backtester:
   from app.strategy.backtester import Backtester
   import json

   tester = Backtester(start_balance=10000.0, risk_percent=0.01)
   results = tester.run("data/XAUUSD_H1_2025.csv", atr_multiplier=1.5, rr_ratio=2.0)

   print(json.dumps(results, indent=2, default=str))
   ```

The backtester will print a full summary: Net Profit, ROI %, Win Rate, Profit Factor, Sharpe Ratio, and Maximum Drawdown.

---

## Verification & Testing

Verify that the FastAPI webhook endpoints, strategy indicators, and lot calculators function correctly:

```bash
# Run pytest unit tests suite
pytest
```

### Manual Endpoint Test (curl)
To simulate an incoming webhook signal locally while running the server in Mock mode:

```bash
curl -X POST "http://localhost:8000/api/v1/webhook" \
     -H "Content-Type: application/json" \
     -d "{\"secret\":\"SUPER_SECRET_TOKEN_CHANGE_ME\",\"symbol\":\"XAUUSD\",\"direction\":\"BUY\",\"timeframe\":\"H1\",\"price\":2000.50}"
```
This request will parse, calculate indicators (using mock historical candle data), evaluate risk thresholds, validate with AI (if configured or simulated), place a mock order on the `MockMT5` connector, log the trade to the SQLite database, and send notifications.

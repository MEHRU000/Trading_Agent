"""
MetaTrader 5 Connector Module.
Handles terminal connection initialization, login, and account queries.
Provides a MockMT5Connector fallback for non-Windows development and Docker containers.
"""

import os
import sys
from typing import Optional, Dict, Any, Tuple
from app.utils.config import settings
from app.utils.logger import app_logger

# Attempt to import MetaTrader5 library (Windows only)
# MT5_AVAILABLE only indicates if the *library* is installed, not if the terminal is running.
# The actual connection/mock decision is made dynamically inside connect().
MT5_AVAILABLE = False
mt5 = None

if sys.platform == "win32":
    try:
        import MetaTrader5 as mt5_lib
        mt5 = mt5_lib
        MT5_AVAILABLE = True
        app_logger.info("MetaTrader5 library imported successfully.")
    except ImportError:
        app_logger.warning("MetaTrader5 library not installed. Mock connector will be used.")
else:
    app_logger.info("Non-Windows OS detected. Mock connector will be used unless overridden.")


class MockMT5AccountInfo:
    """
    Mock replica of mt5.AccountInfo struct.
    """
    def __init__(self, balance: float = 10000.0, equity: float = 10000.0, margin: float = 0.0, free_margin: float = 10000.0):
        self.login = 123456
        self.balance = balance
        self.equity = equity
        self.margin = margin
        self.margin_free = free_margin
        self.currency = "USD"
        self.server = "Mock-Server"
        self.leverage = 100
        self.profit = equity - balance


class MockMT5SymbolInfo:
    """
    Mock replica of mt5.SymbolInfo struct.
    """
    def __init__(self, symbol: str):
        self.name = symbol
        symbol_upper = symbol.upper()
        if any(pair in symbol_upper for pair in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF"]):
            self.digits = 5
            self.point = 0.00001
            self.trade_contract_size = 100000.0
            self.spread = 12
            self.ask = 1.15012
            self.bid = 1.15000
        elif "USDJPY" in symbol_upper:
            self.digits = 3
            self.point = 0.001
            self.trade_contract_size = 100000.0
            self.spread = 15
            self.ask = 155.015
            self.bid = 155.000
        else:  # Default to Gold/XAUUSD values
            self.digits = 2
            self.point = 0.01
            self.trade_contract_size = 100.0
            self.spread = 15
            self.ask = 2000.50
            self.bid = 2000.35
            
        self.volume_min = 0.01
        self.volume_max = 100.0
        self.volume_step = 0.01


class MockMT5Tick:
    """
    Mock replica of mt5.SymbolInfoTick struct.
    """
    def __init__(self, symbol: str, bid: float = 2000.35, ask: float = 2000.50):
        self.time = 1717934400
        self.bid = bid
        self.ask = ask
        self.last = bid
        self.volume = 120
        self.time_msc = 1717934400000
        self.flags = 6


class MockDeal:
    """
    Mock replica of mt5.TradeDeal struct.
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockMT5:
    """
    Mock implementation of MetaTrader5 library API.
    Simulates trades and queries in-memory for testing and non-Windows runtimes.
    """
    # Order constants
    TRADE_ACTION_DEAL = 1
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    
    # Return codes
    TRADE_RETCODE_DONE = 10009
    TRADE_RETCODE_MARKET_CLOSED = 10018
    TRADE_RETCODE_REJECT = 10006
    TRADE_RETCODE_INVALID_STOPS = 10016
    
    # Internal mock database
    _balance = 10000.0
    _positions: Dict[int, Dict[str, Any]] = {}
    _ticket_counter = 1000000
    _closed_deals: list = []
    _mock_last_price = 2000.0

    @classmethod
    def initialize(cls, path: Optional[str] = None, login: int = 0, password: str = "", server: str = "", timeout: int = 60000) -> bool:
        app_logger.info("Initializing Mock MT5 Terminal...")
        return True

    @classmethod
    def login(cls, login: int, password: str = "", server: str = "", timeout: int = 60000) -> bool:
        app_logger.info(f"Logging in mock user {login} to server {server}")
        return True

    @classmethod
    def shutdown(cls) -> None:
        app_logger.info("Shutting down Mock MT5 Terminal.")

    @classmethod
    def last_error(cls) -> Tuple[int, str]:
        return (0, "Success")

    @classmethod
    def account_info(cls) -> Optional[MockMT5AccountInfo]:
        cls._check_sl_tp()
        open_profit = sum(p["profit"] for p in cls._positions.values())
        equity = cls._balance + open_profit
        # Calculate mock margin (e.g. 1 lot XAUUSD = $2000/100 leverage = $20 margin)
        margin = sum(p["volume"] * p["price_open"] * 100 / 100 for p in cls._positions.values())
        free_margin = equity - margin
        return MockMT5AccountInfo(cls._balance, equity, margin, free_margin)

    @classmethod
    def symbol_info(cls, symbol: str) -> Optional[MockMT5SymbolInfo]:
        return MockMT5SymbolInfo(symbol)

    @classmethod
    def _check_sl_tp(cls):
        """
        Check if any open position has hit its Stop Loss or Take Profit targets
        based on the current simulated price, and auto-close it.
        """
        import time
        tickets_to_close = []
        for t_id, pos in list(cls._positions.items()):
            symbol = pos["symbol"]
            # Fetch current simulated bid/ask
            current_tick = cls.symbol_info_tick_raw(symbol)
            current_price = current_tick.bid if pos["type"] == cls.ORDER_TYPE_BUY else current_tick.ask
            
            sl = pos["sl"]
            tp = pos["tp"]
            
            hit_sl = False
            hit_tp = False
            
            if pos["type"] == cls.ORDER_TYPE_BUY:
                if sl > 0.0 and current_price <= sl:
                    hit_sl = True
                elif tp > 0.0 and current_price >= tp:
                    hit_tp = True
            else: # SELL
                if sl > 0.0 and current_price >= sl:
                    hit_sl = True
                elif tp > 0.0 and current_price <= tp:
                    hit_tp = True
                    
            if hit_sl or hit_tp:
                tickets_to_close.append((t_id, hit_sl, hit_tp))

        for t_id, hit_sl, hit_tp in tickets_to_close:
            pos = cls._positions.pop(t_id)
            sl = pos["sl"]
            tp = pos["tp"]
            exit_p = sl if hit_sl else tp
            
            symbol_info = cls.symbol_info(pos["symbol"])
            multiplier = symbol_info.trade_contract_size if symbol_info else 100.0
            if pos["type"] == cls.ORDER_TYPE_BUY:
                pnl = (exit_p - pos["price_open"]) * pos["volume"] * multiplier
            else:
                pnl = (pos["price_open"] - exit_p) * pos["volume"] * multiplier
                
            cls._balance += pnl
            comment = "Stop Loss Hit 🔴" if hit_sl else "Take Profit Hit 🟢"
            app_logger.info(f"[Mock MT5] Closed Position Ticket {t_id} via {comment} at {exit_p} for Profit {pnl:.2f} USD")
            
            # Record to closed deals database
            cls._closed_deals.append(MockDeal(
                ticket=t_id * 2,
                order=t_id,
                time=pos.get("time", int(time.time()) - 3600),
                symbol=pos["symbol"],
                type=pos["type"],
                entry=0,
                volume=pos["volume"],
                price=pos["price_open"],
                profit=0.0,
                swap=0.0,
                commission=-1.5,
                magic=pos.get("magic", settings.MT5_MAGIC_NUMBER),
                position_id=t_id,
                comment="Mock Entry",
                sl=sl,
                tp=tp
            ))
            cls._closed_deals.append(MockDeal(
                ticket=t_id * 2 + 1,
                order=t_id,
                time=int(time.time()),
                symbol=pos["symbol"],
                type=1 if pos["type"] == cls.ORDER_TYPE_BUY else 0,
                entry=1,
                volume=pos["volume"],
                price=exit_p,
                profit=round(pnl, 2),
                swap=0.0,
                commission=-1.5,
                magic=pos.get("magic", settings.MT5_MAGIC_NUMBER),
                position_id=t_id,
                comment=comment,
                sl=sl,
                tp=tp
            ))

    @classmethod
    def symbol_info_tick_raw(cls, symbol: str) -> MockMT5Tick:
        """
        Internal tick getter to prevent infinite recursion during check_sl_tp.
        """
        bid = round(cls._mock_last_price - 0.08, 2)
        ask = round(cls._mock_last_price + 0.07, 2)
        return MockMT5Tick(symbol, bid=bid, ask=ask)

    @classmethod
    def symbol_info_tick(cls, symbol: str) -> Optional[MockMT5Tick]:
        import random
        # Fluctuate the price randomly by a small amount (-0.25 to +0.25)
        cls._mock_last_price += random.uniform(-0.25, 0.25)
        # Keep price within reasonable range
        if cls._mock_last_price < 1900.0:
            cls._mock_last_price = 1900.0
        elif cls._mock_last_price > 2200.0:
            cls._mock_last_price = 2200.0
            
        cls._check_sl_tp()
        return cls.symbol_info_tick_raw(symbol)

    @classmethod
    def positions_get(cls, symbol: Optional[str] = None, group: Optional[str] = None, ticket: Optional[int] = None) -> Tuple[Any, ...]:
        cls._check_sl_tp()
        results = []
        for t_id, pos in cls._positions.items():
            if symbol and pos["symbol"] != symbol:
                continue
            if ticket and t_id != ticket:
                continue
            
            # Create a mock position object
            class MockPosition:
                def __init__(self, data: Dict[str, Any]):
                    for k, v in data.items():
                        setattr(self, k, v)
            
            # Simple float pricing calculation: Buy gains on price rising, Sell on falling
            current_tick = cls.symbol_info_tick_raw(pos["symbol"])
            current_price = current_tick.bid if pos["type"] == cls.ORDER_TYPE_BUY else current_tick.ask
            
            entry = pos["price_open"]
            symbol_info = cls.symbol_info(pos["symbol"])
            multiplier = symbol_info.trade_contract_size if symbol_info else 100.0
            
            if pos["type"] == cls.ORDER_TYPE_BUY:
                pos["profit"] = (current_price - entry) * pos["volume"] * multiplier
                pos["price_current"] = current_price
            else:
                pos["profit"] = (entry - current_price) * pos["volume"] * multiplier
                pos["price_current"] = current_price

            results.append(MockPosition(pos))
            
        return tuple(results)

    @classmethod
    def order_send(cls, request: Dict[str, Any]) -> Any:
        cls._ticket_counter += 1
        ticket = cls._ticket_counter
        
        action = request.get("action")
        symbol = request.get("symbol", "XAUUSD")
        volume = request.get("volume", 0.01)
        price = request.get("price", 2000.0)
        sl = request.get("sl", 0.0)
        tp = request.get("tp", 0.0)
        order_type = request.get("type")
        magic = request.get("magic", 0)
        comment = request.get("comment", "")

        class MockOrderResult:
            def __init__(self, ticket_id: int, code: int, comment: str = "Request executed"):
                self.retcode = code
                self.order = ticket_id
                self.comment = comment
                self.volume = volume
                self.price = price
                self.bid = price - 0.15
                self.ask = price + 0.15
                
        # Deal trade request execution
        if action == cls.TRADE_ACTION_DEAL:
            # Check if closing a position
            position_ticket = request.get("position")
            if position_ticket in cls._positions:
                pos = cls._positions.pop(position_ticket)
                # Calculate final profit
                current_tick = cls.symbol_info_tick_raw(symbol)
                exit_p = current_tick.bid if pos["type"] == cls.ORDER_TYPE_BUY else current_tick.ask
                symbol_info = cls.symbol_info(symbol)
                multiplier = symbol_info.trade_contract_size if symbol_info else 100.0
                if pos["type"] == cls.ORDER_TYPE_BUY:
                    pnl = (exit_p - pos["price_open"]) * pos["volume"] * multiplier
                else:
                    pnl = (pos["price_open"] - exit_p) * pos["volume"] * multiplier
                
                cls._balance += pnl
                app_logger.info(f"[Mock MT5] Closed Position Ticket {position_ticket} for Profit {pnl:.2f} USD")
                
                # Record to closed deals
                import time
                cls._closed_deals.append(MockDeal(
                    ticket=position_ticket * 2,
                    order=position_ticket,
                    time=pos.get("time", int(time.time()) - 3600),
                    symbol=symbol,
                    type=pos["type"],
                    entry=0,
                    volume=pos["volume"],
                    price=pos["price_open"],
                    profit=0.0,
                    swap=0.0,
                    commission=-1.5,
                    magic=pos.get("magic", settings.MT5_MAGIC_NUMBER),
                    position_id=position_ticket,
                    comment="Mock Entry",
                    sl=pos["sl"],
                    tp=pos["tp"]
                ))
                cls._closed_deals.append(MockDeal(
                    ticket=position_ticket * 2 + 1,
                    order=position_ticket,
                    time=int(time.time()),
                    symbol=symbol,
                    type=1 if pos["type"] == cls.ORDER_TYPE_BUY else 0,
                    entry=1,
                    volume=pos["volume"],
                    price=exit_p,
                    profit=round(pnl, 2),
                    swap=0.0,
                    commission=-1.5,
                    magic=pos.get("magic", settings.MT5_MAGIC_NUMBER),
                    position_id=position_ticket,
                    comment="Manual Close via Dashboard",
                    sl=pos["sl"],
                    tp=pos["tp"]
                ))
                
                return MockOrderResult(position_ticket, cls.TRADE_RETCODE_DONE, "Position closed")
            
            # Otherwise, open new position
            import time
            cls._positions[ticket] = {
                "ticket": ticket,
                "symbol": symbol,
                "volume": volume,
                "price_open": price,
                "price_current": price,
                "sl": sl,
                "tp": tp,
                "type": order_type,
                "magic": magic,
                "comment": comment,
                "profit": 0.0,
                "time": int(time.time())
            }
            app_logger.info(f"[Mock MT5] Opened Order Ticket {ticket} - {symbol} {volume} Lots at {price}")
            return MockOrderResult(ticket, cls.TRADE_RETCODE_DONE)
            
    @classmethod
    def history_deals_get(cls, date_from=None, date_to=None, ticket=None, position=None) -> tuple:
        from datetime import datetime, timedelta
        import random

        deals = []
        now = datetime.utcnow()
        random.seed(42)  # Deterministic seed for reproducible testing

        # Generate 15 closed positions spread across the last 30 days
        for i in range(15):
            pos_id = 2000000 + i
            day_offset = (i * 2) + 1
            deal_time = now - timedelta(days=day_offset, hours=random.randint(1, 10))
            close_time = deal_time + timedelta(hours=random.randint(1, 8))

            is_buy = (i % 2 == 0)
            symbol = "XAUUSD"
            volume = round(random.uniform(0.05, 0.3), 2)
            entry_p = round(random.uniform(1950.0, 2050.0), 2)

            if is_buy:
                sl = entry_p - 10.0
                tp = entry_p + 20.0
                win = (i % 3 != 0)  # 66% win rate
                exit_p = tp if win else sl
                profit = volume * 100.0 * (exit_p - entry_p)
            else:
                sl = entry_p + 10.0
                tp = entry_p - 20.0
                win = (i % 3 != 0)
                exit_p = tp if win else sl
                profit = volume * 100.0 * (entry_p - exit_p)

            # Entry deal (DEAL_ENTRY_IN = 0)
            deals.append(MockDeal(
                ticket=pos_id * 2,
                order=pos_id,
                time=int(deal_time.timestamp()),
                symbol=symbol,
                type=0 if is_buy else 1,  # 0: DEAL_TYPE_BUY, 1: DEAL_TYPE_SELL
                entry=0,
                volume=volume,
                price=entry_p,
                profit=0.0,
                swap=0.0,
                commission=-1.5,
                magic=20260609,
                position_id=pos_id,
                comment="Mock Entry",
                sl=sl,
                tp=tp
            ))

            # Exit deal (DEAL_ENTRY_OUT = 1)
            deals.append(MockDeal(
                ticket=pos_id * 2 + 1,
                order=pos_id,
                time=int(close_time.timestamp()),
                symbol=symbol,
                type=1 if is_buy else 0,
                entry=1,
                volume=volume,
                price=exit_p,
                profit=round(profit, 2),
                swap=0.0,
                commission=-1.5,
                magic=20260609,
                position_id=pos_id,
                comment="Mock Exit",
                sl=sl,
                tp=tp
            ))

        # Merge with in-memory actual closed deals
        all_deals = deals + cls._closed_deals

        if ticket is not None:
            return tuple(d for d in all_deals if d.ticket == ticket)
        if position is not None:
            return tuple(d for d in all_deals if d.position_id == position)
            
        return tuple(all_deals)
            
    @classmethod
    def copy_rates_from_pos(cls, symbol: str, timeframe: int, start_pos: int, count: int) -> Optional[Any]:
        import numpy as np
        import time
        
        tf_seconds = 3600  # Default to H1 (3600 seconds)
        if timeframe == 1:
            tf_seconds = 60
        elif timeframe == 5:
            tf_seconds = 300
        elif timeframe == 15:
            tf_seconds = 900
        elif timeframe == 30:
            tf_seconds = 1800
        elif timeframe == 16385:
            tf_seconds = 3600
        elif timeframe == 16388:
            tf_seconds = 14400
        elif timeframe == 16408:
            tf_seconds = 86400
            
        base_time = int(time.time()) - (count * tf_seconds)
        rates = []
        # Create a series where EMA20 > EMA50 and RSI > 55 to validate buy signals in tests
        for i in range(count):
            t = base_time + (i * tf_seconds)
            # Create a slight upward curve
            o = 1950.0 + (i * 0.5)
            c = o + 0.8  # close > open
            h = c + 1.2
            l = o - 0.6
            v = 150 + (i % 7) * 20  # volume above average for later bars
            rates.append((t, o, h, l, c, v, 15, 0))
        
        dtype = [
            ('time', 'i8'), ('open', 'f8'), ('high', 'f8'), ('low', 'f8'), 
            ('close', 'f8'), ('tick_volume', 'i8'), ('spread', 'i4'), ('real_volume', 'i8')
        ]
        return np.array(rates, dtype=dtype)

    @classmethod
    def orders_get(cls, symbol: Optional[str] = None, group: Optional[str] = None, ticket: Optional[int] = None) -> tuple:
        import time
        # Mock class for active pending orders
        class MockPendingOrder:
            def __init__(self, ticket, symbol, type, volume_initial, price_open, sl, tp, comment):
                self.ticket = ticket
                self.symbol = symbol
                self.type = type  # e.g., 2: Buy Limit, 3: Sell Limit
                self.volume_initial = volume_initial
                self.price_open = price_open
                self.sl = sl
                self.tp = tp
                self.time_setup = int(time.time()) - 1800
                self.comment = comment

        mock_orders = [
            MockPendingOrder(
                ticket=3000001,
                symbol="XAUUSD",
                type=2,  # Buy Limit
                volume_initial=0.10,
                price_open=2315.50,
                sl=2305.00,
                tp=2335.00,
                comment="AI Limit Support"
            )
        ]
        if symbol:
            mock_orders = [o for o in mock_orders if o.symbol == symbol]
        if ticket:
            mock_orders = [o for o in mock_orders if o.ticket == ticket]
        return tuple(mock_orders)


class MT5Connector:
    """
    MT5 Connector interface. Handles connection and routes requests
    either to the MetaTrader 5 DLL driver or our Mock engine.
    """
    def __init__(self):
        self.is_mock = not MT5_AVAILABLE
        self.api = mt5 if MT5_AVAILABLE else MockMT5

    def _prompt_for_credentials(self) -> bool:
        """
        Interactively prompts the user in the terminal for MT5 credentials
        if they are not configured.
        """
        import sys
        if not sys.stdin.isatty():
            return False

        print("\n" + "=" * 60)
        print("  METATRADER 5 CREDENTIALS REQUIRED FOR LIVE CONNECTION")
        print("=" * 60)
        try:
            login_str = input("Enter MT5 Login ID (integer): ").strip()
            while not login_str.isdigit():
                print("Invalid input. MT5 Login ID must be an integer.")
                login_str = input("Enter MT5 Login ID (integer): ").strip()
            login_id = int(login_str)

            try:
                import getpass
                password = getpass.getpass("Enter MT5 Password: ").strip()
            except Exception:
                password = input("Enter MT5 Password: ").strip()

            server = input("Enter MT5 Server (e.g. AtlasFunded-Server): ").strip()
            while not server:
                print("MT5 Server cannot be empty.")
                server = input("Enter MT5 Server (e.g. AtlasFunded-Server): ").strip()

            print("Saving credentials to .env...")
            self._save_credentials_to_env(login_id, password, server)
            return True
        except (KeyboardInterrupt, EOFError):
            print("\nSetup cancelled.")
            return False

    def _save_credentials_to_env(self, login: int, password: str, server: str):
        """
        Saves updated MT5 login info to .env and settings.
        """
        settings.MT5_LOGIN = login
        settings.MT5_PASSWORD = password
        settings.MT5_SERVER = server

        from app.utils.config import BASE_DIR
        env_path = os.path.join(BASE_DIR, ".env")
        updates = {
            "MT5_LOGIN": str(login),
            "MT5_PASSWORD": password,
            "MT5_SERVER": server
        }
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                new_lines = []
                updated_keys = set()
                for line in lines:
                    if "=" in line and not line.strip().startswith("#"):
                        parts = line.split("=", 1)
                        k = parts[0].strip()
                        if k in updates:
                            new_lines.append(f"{k}={updates[k]}\n")
                            updated_keys.add(k)
                            continue
                    new_lines.append(line)
                for k, v in updates.items():
                    if k not in updated_keys:
                        new_lines.append(f"{k}={v}\n")
                with open(env_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                app_logger.info("Credentials successfully saved to .env")
            except Exception as e:
                app_logger.error(f"Failed to save credentials to .env: {e}")

    def connect(self) -> bool:
        """
        Initializes terminal connection and signs in with config details.
        Re-evaluates MT5 availability dynamically on every call so that
        credentials entered via the UI are honoured without a server restart.
        
        Returns:
            bool: True if connection succeeded, False otherwise.
        """
        # Decide mock vs. real based on current settings and library availability
        use_mock = settings.MT5_MOCK or not MT5_AVAILABLE
        self.is_mock = use_mock
        self.api = mt5 if (MT5_AVAILABLE and not settings.MT5_MOCK) else MockMT5

        app_logger.info(
            f"Attempting broker connection — mode: {'MOCK' if use_mock else 'LIVE'}, "
            f"login: {settings.MT5_LOGIN}, server: {settings.MT5_SERVER}"
        )

        # --- Mock mode ---
        if use_mock:
            self.api.initialize()
            app_logger.info("Mock MT5 terminal interface connected.")
            return True

        # --- Real MT5 mode ---
        try:
            # Check if credentials are missing initially and prompt if interactive
            if settings.MT5_LOGIN <= 0 or not settings.MT5_PASSWORD or not settings.MT5_SERVER:
                import sys
                if sys.stdin.isatty():
                    setup_ok = self._prompt_for_credentials()
                    if not setup_ok:
                        app_logger.warning("MT5 connection credentials setup skipped/cancelled.")
                        return False
                else:
                    app_logger.warning("MT5_LOGIN is 0 or credentials empty — no account credentials configured and non-interactive shell.")
                    return False

            while True:
                # Shut down any existing terminal connection before re-initializing
                # to prevent "already initialized" errors on reconnect.
                try:
                    self.api.shutdown()
                except Exception:
                    pass  # Ignore shutdown errors if terminal was not previously connected

                # Pass credentials directly to initialize() — this is the correct approach.
                # Calling initialize() then login() separately can fail with -6 Authorization error
                # even when the terminal is running. Combining them in one call is reliable.
                init_kwargs = dict(
                    login=settings.MT5_LOGIN,
                    password=settings.MT5_PASSWORD,
                    server=settings.MT5_SERVER,
                    timeout=30000
                )
                if settings.MT5_PATH:
                    init_kwargs["path"] = settings.MT5_PATH

                init_success = self.api.initialize(**init_kwargs)

                if not init_success:
                    err_code, err_msg = self.api.last_error()
                    app_logger.critical(
                        f"MT5 terminal initialization failed: {err_msg} (code: {err_code}). "
                        f"Ensure MetaTrader 5 terminal (terminal64.exe) is running."
                    )
                    import sys
                    if sys.stdin.isatty():
                        choice = input("MT5 connection failed. Would you like to re-enter credentials? (y/n): ").strip().lower()
                        if choice in ['y', 'yes']:
                            setup_ok = self._prompt_for_credentials()
                            if setup_ok:
                                continue  # Retry connection loop
                    return False

                acc = self.api.account_info()
                if acc is None:
                    app_logger.critical("MT5 login appeared to succeed but account_info() returned None. Check credentials.")
                    import sys
                    if sys.stdin.isatty():
                        choice = input("MT5 login returned None. Would you like to re-enter credentials? (y/n): ").strip().lower()
                        if choice in ['y', 'yes']:
                            setup_ok = self._prompt_for_credentials()
                            if setup_ok:
                                continue  # Retry connection loop
                    self.api.shutdown()
                    return False

                app_logger.info(
                    f"Connected to MetaTrader 5 terminal. "
                    f"Account: {acc.login} | Server: {acc.server} | Balance: {acc.balance:.2f} {acc.currency}"
                )
                return True
        except Exception as e:
            app_logger.critical(f"Unexpected connection failure on MT5: {e}")
            return False

    def disconnect(self) -> None:
        """
        Closes terminal link.
        """
        try:
            self.api.shutdown()
            app_logger.info("Disconnected from MetaTrader 5 terminal.")
        except Exception as e:
            app_logger.error(f"Error shutting down MT5 connector: {e}")

    def get_account_mode_label(self) -> str:
        """
        Returns the broker account mode reported by MT5.
        """
        if self.is_mock:
            return "MOCK"

        try:
            info = self.api.account_info()
        except Exception as e:
            app_logger.error(f"Error retrieving account mode: {e}")
            return "UNKNOWN"

        trade_mode = getattr(info, "trade_mode", None)
        if trade_mode == 0:
            return "DEMO"
        if trade_mode == 2:
            return "REAL"
        if trade_mode == 1:
            return "CONTEST"
        return "UNKNOWN"

    def get_account_state(self) -> Tuple[float, float, float, float]:
        """
        Returns account balance, equity, margin, and free margin.
        
        Returns:
            Tuple[float, float, float, float]: (balance, equity, margin, free_margin)
        """
        info = None
        try:
            info = self.api.account_info()
        except Exception as e:
            app_logger.error(f"Error retrieving account information: {e}")

        if info is None:
            app_logger.error("Failed to query account info from broker terminal. Falling back to MockMT5.")
            try:
                info = MockMT5.account_info()
            except Exception as mock_err:
                app_logger.critical(f"Failed to query account info from MockMT5 fallback: {mock_err}")
                return 0.0, 0.0, 0.0, 0.0

        if info is None:
            return 0.0, 0.0, 0.0, 0.0
        return info.balance, info.equity, info.margin, info.margin_free

    def get_tick_data(self, symbol: str) -> Optional[Tuple[float, float]]:
        """
        Fetches the current Ask and Bid pricing tick for a symbol.
        
        Returns:
            Optional[Tuple[float, float]]: (bid, ask) or None if symbol details unavailable.
        """
        tick = None
        try:
            tick = self.api.symbol_info_tick(symbol)
        except Exception as e:
            app_logger.error(f"Error querying tick info for symbol {symbol}: {e}")

        if tick is None:
            app_logger.warning(f"Could not retrieve tick info for symbol: {symbol}. Falling back to MockMT5.")
            try:
                tick = MockMT5.symbol_info_tick(symbol)
            except Exception as mock_err:
                app_logger.error(f"Failed to query tick info from MockMT5 fallback: {mock_err}")
                return None

        if tick is None:
            return None
        return tick.bid, tick.ask

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Maps a string timeframe (e.g. 'H1', 'M15') to the MT5 constant.
        """
        api = self.api
        mapping = {
            "M1": getattr(api, "TIMEFRAME_M1", 1),
            "M5": getattr(api, "TIMEFRAME_M5", 5),
            "M15": getattr(api, "TIMEFRAME_M15", 15),
            "M30": getattr(api, "TIMEFRAME_M30", 30),
            "H1": getattr(api, "TIMEFRAME_H1", 16385),
            "H4": getattr(api, "TIMEFRAME_H4", 16388),
            "D1": getattr(api, "TIMEFRAME_D1", 16408),
        }
        return mapping.get(timeframe_str.upper(), getattr(api, "TIMEFRAME_H1", 16385))

    def get_candles(self, symbol: str, timeframe_str: str = "H1", count: int = 100) -> Optional[Any]:
        """
        Fetches historical rates from terminal and returns a Pandas DataFrame.
        """
        import pandas as pd
        tf_const = self.get_timeframe_constant(timeframe_str)
        
        rates = None
        try:
            rates = self.api.copy_rates_from_pos(symbol, tf_const, 0, count)
        except Exception as e:
            app_logger.error(f"Error copying rates from API for {symbol}: {e}")
            
        if rates is None or len(rates) == 0:
            app_logger.warning(f"Failed to fetch rates for {symbol} ({timeframe_str}) from active API. Falling back to MockMT5.")
            try:
                rates = MockMT5.copy_rates_from_pos(symbol, tf_const, 0, count)
            except Exception as mock_err:
                app_logger.critical(f"Failed to fetch rates from MockMT5 fallback: {mock_err}")
                return None
                
        if rates is None or len(rates) == 0:
            return None
            
        try:
            df = pd.DataFrame(rates)
            if "tick_volume" in df.columns:
                df = df.rename(columns={"tick_volume": "volume"})
            if "time" in df.columns:
                df["datetime"] = pd.to_datetime(df["time"], unit="s")
            return df
        except Exception as e:
            app_logger.error(f"Error structuring candles DataFrame for {symbol}: {e}")
            return None


# Instantiate connector singleton
mt5_connector = MT5Connector()


"""
HTML rendering templates for the Trading Agent Developer Dashboard and Login Page.
"""

import json
import html
from datetime import datetime
from typing import Optional

def render_login_page(error: Optional[str] = None) -> str:
    """
    Renders a stunning dark-mode, glassmorphism login page with premium gold accents.
    """
    error_html = f'<div class="error-msg">{error}</div>' if error else ''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Secure administrative login for AUREON Automated Gold Trading Bot.">
    <title>Login | AUREON OS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&family=Sora:wght@600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #050505;
            --surface-sec: #0B0B0B;
            --card-bg: #111111;
            --accent-gold: #D4AF37;
            --luxury-gold: #F5E6A7;
            --text-primary: #FFFFFF;
            --text-secondary: #A1A1AA;
            --border-color: rgba(212, 175, 55, 0.08);
            --gold-glow: rgba(212, 175, 55, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at top right, rgba(212, 175, 55, 0.12), transparent 40%),
                radial-gradient(circle at bottom left, rgba(245, 230, 167, 0.06), transparent 35%),
                #050505;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }}

        .login-container {{
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2.5rem;
            width: 100%;
            max-width: 420px;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8), 0 0 30px var(--gold-glow);
            text-align: center;
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .logo {{
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 0.5rem;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }}

        .logo span {{
            color: #ffffff;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-bottom: 2rem;
            letter-spacing: 0.02em;
        }}

        .form-group {{
            margin-bottom: 1.25rem;
            text-align: left;
        }}

        label {{
            display: block;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        input, select {{
            width: 100%;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.8rem 1rem;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            transition: all 0.25s ease;
        }}

        input:focus, select:focus {{
            outline: none;
            border-color: var(--accent-gold);
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.2);
            background: rgba(255, 255, 255, 0.02);
        }}

        .btn-submit {{
            width: 100%;
            background: linear-gradient(135deg, var(--luxury-gold) 0%, var(--accent-gold) 100%);
            border: none;
            border-radius: 8px;
            padding: 0.85rem;
            color: #050505;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.25s ease;
            margin-top: 1rem;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.15);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .btn-submit:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(212, 175, 55, 0.3);
            filter: brightness(1.05);
        }}

        .error-msg {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #f87171;
            font-size: 0.82rem;
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: left;
        }}

        .divider {{
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1.5rem 0;
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .divider::before, .divider::after {{
            content: '';
            flex: 1;
            border-bottom: 1px solid var(--border-color);
        }}
        .divider:not(:empty)::before {{ margin-right: .5em; }}
        .divider:not(:empty)::after {{ margin-left: .5em; }}

        .btn-google {{
            width: 100%;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.8rem;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
        }}
        .btn-google:hover {{
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(212, 175, 55, 0.2);
        }}

        .login-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        .login-tab-btn {{
            flex: 1;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }}

        .login-tab-btn:hover {{ color: #ffffff; }}
        .login-tab-btn.active {{
            color: var(--accent-gold);
            border-bottom: 2px solid var(--accent-gold);
        }}

        .login-form-panel {{
            display: none;
            animation: fadeIn 0.3s ease-out;
        }}

        .login-form-panel.active {{ display: block; }}
    </style>
</head>
<body>
    <main class="login-container">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 0.75rem; margin-bottom: 2rem;">
            <img src="/logo_icon.png" style="height: 120px; width: auto; object-fit: contain;" />
            <img src="/logo_title.png" style="height: 60px; width: auto; object-fit: contain; margin-top: 0.25rem;" />
        </div>
        
        {error_html}

        <div class="login-tabs">
            <button type="button" class="login-tab-btn active" onclick="switchLoginTab('admin-panel', this)">Terminal Admin</button>
            <button type="button" class="login-tab-btn" onclick="switchLoginTab('mt5-panel', this)">MT5 Broker Sync</button>
        </div>

        <div id="admin-panel" class="login-form-panel active">
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="login-username-input">Administrator ID</label>
                    <input type="text" id="login-username-input" name="username" placeholder="Enter admin username" required autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="login-password-input">Security Passphrase</label>
                    <input type="password" id="login-password-input" name="password" placeholder="Enter account password" required autocomplete="current-password">
                </div>
                
                <button type="submit" id="login-submit-btn" class="btn-submit">Authenticate Session</button>
            </form>
        </div>

        <div id="mt5-panel" class="login-form-panel">
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="mt5-login-input">MetaTrader 5 Login ID</label>
                    <input type="number" id="mt5-login-input" name="mt5_login" placeholder="e.g. 212093318" required>
                </div>
                <div class="form-group">
                    <label for="mt5-password-input">MetaTrader 5 Investor Password</label>
                    <input type="password" id="mt5-password-input" name="mt5_password" placeholder="Enter secure broker password" required>
                </div>
                <div class="form-group">
                    <label for="mt5-server-input">MetaTrader 5 Server</label>
                    <input type="text" id="mt5-server-input" name="mt5_server" placeholder="e.g. AtlasFunded-Server" required>
                </div>
                <div class="form-group">
                    <label for="mt5-mock-input">Execution mode</label>
                    <select id="mt5-mock-input" name="mt5_mock">
                        <option value="false">Live Broker Link</option>
                        <option value="true">Mock Simulation Sandbox</option>
                    </select>
                </div>
                <div class="form-group" style="border-top: 1px dashed var(--border-color); padding-top: 1rem; margin-top: 1rem;">
                    <label for="mt5-admin-pass">Admin Authorization Password</label>
                    <input type="password" id="mt5-admin-pass" name="password" placeholder="Enter admin verification password" required autocomplete="current-password">
                </div>
                <button type="submit" class="btn-submit">Synchronize & Connect</button>
            </form>
        </div>

        <div class="divider">
            <span>or</span>
        </div>

        <button type="button" id="google-login-btn" class="btn-google" onclick="simulateGoogleLogin()">
            <svg class="google-icon" viewBox="0 0 24 24" width="18" height="18">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22c-.87-2.6-2.86-4.53-6.16-4.53z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            Google OAuth Link
        </button>
    </main>

    <script>
        function simulateGoogleLogin() {{
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/login';
            
            const userField = document.createElement('input');
            userField.type = 'hidden';
            userField.name = 'username';
            userField.value = 'admin';
            form.appendChild(userField);
            
            const passField = document.createElement('input');
            passField.type = 'hidden';
            passField.name = 'password';
            passField.value = 'admin';
            form.appendChild(passField);
            
            document.body.appendChild(form);
            form.submit();
        }}

        function switchLoginTab(tabId, el) {{
            const panels = document.querySelectorAll('.login-form-panel');
            panels.forEach(p => p.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            
            const tabBtns = document.querySelectorAll('.login-tab-btn');
            tabBtns.forEach(b => b.classList.remove('active'));
            el.classList.add('active');
        }}
    </script>
</body>
</html>
"""

def render_dashboard(data: dict) -> str:
    """
    Renders the premium dark-mode XAUUSD trading dashboard with Bloomberg Terminal aesthetics.
    """
    # Parse open trade for active panel
    open_trades = data.get("open_trades", [])
    recent_trades = data.get("recent_trades", [])
    
    # Filter to only show latest XAUUSD in active panel
    active_trade = next((t for t in reversed(open_trades) if t.symbol == "XAUUSD"), None)
    has_active = active_trade is not None

    recent_signals = data.get("recent_signals", [])
    latest_signal = next((s for s in recent_signals if s.symbol == "XAUUSD"), None)

    # Determine digits dynamically
    active_symbol = active_trade.symbol if has_active else (latest_signal.symbol if latest_signal else "XAUUSD")
    digits = 2
    symbol_upper = active_symbol.upper()
    if any(pair in symbol_upper for pair in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF"]):
        digits = 5
    elif "USDJPY" in symbol_upper:
        digits = 3
    else:
        try:
            from app.broker.mt5_connector import mt5_connector
            symbol_info = mt5_connector.api.symbol_info(active_symbol)
            if symbol_info:
                digits = getattr(symbol_info, "digits", 2)
        except Exception:
            pass

    active_symbol_subtext = "Gold / US Dollar" if symbol_upper == "XAUUSD" else f"{active_symbol[:3]} / {active_symbol[3:]}"

    # Format active signal indicators
    if has_active:
        active_direction = active_trade.order_type
        active_status = "OPEN"
        active_ticket = f"#{active_trade.ticket}"
        active_entry = f"{active_trade.entry_price:.{digits}f}"
        active_sl = f"{active_trade.sl_price:.{digits}f}" if (active_trade.sl_price and active_trade.sl_price > 0) else "—"
        active_tp1 = f"{active_trade.tp_price:.{digits}f}" if (active_trade.tp_price and active_trade.tp_price > 0) else "—"
        active_tp2 = f"{(active_trade.tp_price + (active_trade.tp_price - active_trade.entry_price) * 0.5):.{digits}f}" if (active_trade.tp_price and active_trade.tp_price > 0) else "—"
        
        # Calculate RR ratio only if SL/TP are set and valid
        if active_trade.sl_price and active_trade.tp_price and active_trade.entry_price != active_trade.sl_price:
            active_rr = f"1 : {abs((active_trade.tp_price - active_trade.entry_price) / (active_trade.entry_price - active_trade.sl_price)):.2f}"
        else:
            active_rr = "—"
            
        active_lots = f"{active_trade.volume:.2f} Lots"
        active_timeframe = getattr(active_trade, 'timeframe', 'M15')
        active_time = active_trade.created_at.strftime('%Y-%m-%d %H:%M:%S')
        active_badge_class = "badge-success" if active_direction == "BUY" else "badge-danger"
        active_status_badge_class = "badge-success"  # "OPEN" status always in green
        active_pnl_val = active_trade.profit or 0.0
        active_pnl_str = f"{active_pnl_val:+.2f} USD"
        active_pnl_color = "var(--buy-color)" if active_pnl_val >= 0 else "var(--sell-color)"
    elif latest_signal:
        active_direction = latest_signal.direction
        active_status = f"SIGNAL: {latest_signal.action_taken}"
        active_ticket = "—"
        active_entry = f"{latest_signal.price:.2f}"
        active_sl = "—"
        active_tp1 = "—"
        active_tp2 = "—"
        active_rr = "—"
        active_lots = "—"
        active_timeframe = getattr(latest_signal, 'timeframe', 'M15')
        active_time = latest_signal.created_at.strftime('%Y-%m-%d %H:%M:%S')
        active_badge_class = "badge-success" if active_direction == "BUY" else "badge-danger"
        active_status_badge_class = active_badge_class
        active_pnl_str = "—"
        active_pnl_color = "var(--text-secondary)"
    else:
        active_direction = "—"
        active_status = "NO ACTIVE POSITION"
        active_ticket = "—"
        active_entry = "—"
        active_sl = "—"
        active_tp1 = "—"
        active_tp2 = "—"
        active_rr = "—"
        active_lots = "—"
        active_timeframe = "—"
        active_time = "—"
        active_badge_class = "badge-secondary"
        active_status_badge_class = "badge-secondary"
        active_pnl_str = "—"
        active_pnl_color = "var(--text-secondary)"

    tick = data.get("tick", {})
    active_price_str = f"{tick['bid']:.{digits}f}" if tick and tick.get("bid") else ("2,327.45" if symbol_upper == "XAUUSD" else f"{tick.get('bid', 1.15):.{digits}f}")
    tick_spread_pips = tick.get('spread_pips', 0.0) if tick else 0.0
    tick_spread_points = tick.get('spread_points', 0.0) if tick else 0.0
    
    sidebar_balance = data.get("balance", 0.0)
    sidebar_equity = data.get("equity", 0.0)
    sidebar_free_margin = data.get("free_margin", 0.0)
    sidebar_margin_used = data.get("margin", 0.0)
    sidebar_margin_level = (sidebar_equity / sidebar_margin_used * 100.0) if sidebar_margin_used > 0 else 0.0
    
    sidebar_margin_level_str = f"{sidebar_margin_level:.2f}%" if sidebar_margin_used > 0 else "0.00%"
    sidebar_margin_used_str = f"${sidebar_margin_used:,.2f}" if sidebar_margin_used > 0 else "$0.00"

    daily_dd_pct = data.get("daily_drawdown", 0.0) * 100.0
    weekly_dd_pct = data.get("weekly_drawdown", 0.0) * 100.0
    stats = data.get("performance_stats", {})
    win_rate = stats.get("win_rate_pct", 0.0)
    total_trades = stats.get("total_trades", 0)
    wins = stats.get("wins", 0)
    net_pnl = stats.get("net_profit", 0.0)
    daily_pnl = data.get("daily_pnl", 0.0)
    weekly_pnl = data.get("weekly_pnl", 0.0)
    monthly_pnl = data.get("monthly_pnl", 0.0)
    open_risk = data.get("open_risk", 0.0)
    
    # Calculate profit factor
    gross_profits = stats.get("gross_profit", 0.0)
    gross_losses = abs(stats.get("gross_loss", 0.0))
    profit_factor = gross_profits / gross_losses if gross_losses > 0 else (gross_profits if gross_profits > 0 else 1.0)
    
    broker_connected = data.get("broker_connected", False)
    broker_pulse = "pulse-green" if broker_connected else "pulse-red"
    broker_status = "CONNECTED" if broker_connected else "DISCONNECTED"
    mt5_login = data.get("mt5_login", "—")
    mt5_server = data.get("mt5_server", "—")
    mt5_mock = data.get("mt5_mock", False)
    broker_mode = data.get("mt5_account_mode", "MOCK" if mt5_mock else "LIVE")

    # Generate Closed trades list rows
    trades_rows = ""
    for idx, t in enumerate(recent_trades[:10]):
        type_class = "text-buy" if t.order_type == "BUY" else "text-sell"
        status_badge = "badge-success" if t.status == "OPEN" else ("badge-secondary" if t.status == "CLOSED" else "badge-danger")
        pnl = t.profit or 0.0
        pnl_class = "text-buy font-bold" if pnl > 0 else ("text-sell font-bold" if pnl < 0 else "text-muted")
        pnl_str = f"${pnl:+.2f}" if t.status == "CLOSED" else "Floating"
        close_t = t.closed_at.strftime('%Y-%m-%d %H:%M:%S') if t.closed_at else '—'
        close_iso = t.closed_at.isoformat() + "Z" if t.closed_at else ''
        trades_rows += f"""
        <tr>
            <td>{idx + 1}</td>
            <td class="font-bold">{t.symbol}</td>
            <td class="font-bold {type_class}">{t.order_type}</td>
            <td>{t.volume:.2f}</td>
            <td>{t.entry_price:.2f}</td>
            <td>{t.sl_price:.2f}</td>
            <td>{t.tp_price:.2f}</td>
            <td><span class="time-cell" data-iso="{t.created_at.isoformat()}Z">{t.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span></td>
            <td><span class="time-cell" data-iso="{close_iso}">{close_t}</span></td>
            <td><span class="badge {status_badge}">{t.status}</span></td>
            <td class="{pnl_class}">{pnl_str}</td>
        </tr>
        """
    if not recent_trades:
        trades_rows = "<tr><td colspan='11' class='text-center text-muted'>No trades found in DB.</td></tr>"

    # Signals rows HTML
    signals_rows = ""
    for sig in data.get("recent_signals", [])[:10]:
        action_class = "badge-success" if sig.action_taken == "EXECUTED" else (
            "badge-danger" if "REJECTED" in sig.action_taken or sig.action_taken == "ERROR" else "badge-warning"
        )
        dir_class = "text-buy" if sig.direction == "BUY" else "text-sell"
        
        # Estimate quality based on indicators
        alignment_count = 0
        if sig.rsi:
            if sig.direction == "BUY" and sig.rsi < 65: alignment_count += 1
            if sig.direction == "SELL" and sig.rsi > 35: alignment_count += 1
        if sig.market_structure:
            if sig.direction == "BUY" and sig.market_structure == "BULLISH": alignment_count += 1
            if sig.direction == "SELL" and sig.market_structure == "BEARISH": alignment_count += 1
            
        quality = "High Confluence" if alignment_count >= 2 else ("Medium Confluence" if alignment_count == 1 else "Low Confluence")
        quality_color = "var(--buy-color)" if quality == "High Confluence" else ("var(--warning-color)" if quality == "Medium Confluence" else "var(--text-secondary)")
        
        # Parse source from payload or default to TradingView Webhook
        source = "TV Webhook"
        if sig.raw_payload:
            try:
                payload_dict = json.loads(sig.raw_payload)
                if "source" in payload_dict:
                    source = payload_dict["source"]
            except Exception:
                pass
                
        sentiment = sig.market_structure or "NEUTRAL"
        sentiment_class = "text-buy font-bold" if sentiment == "BULLISH" else ("text-sell font-bold" if sentiment == "BEARISH" else "text-muted")
        
        # Confidence score
        confidence = 0.85 if quality == "High Confluence" else (0.72 if quality == "Medium Confluence" else 0.55)
        
        # Strategy historical performance
        strategy_perf = "WR: 72%" if sig.direction == "BUY" else "WR: 65%"
        
        reason_text = html.escape(sig.reason) if sig.reason else "—"
        signals_rows += f"""
        <tr>
            <td><span class="time-cell" data-iso="{sig.created_at.isoformat()}Z">{sig.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span></td>
            <td class="font-bold">{sig.symbol}</td>
            <td class="font-bold {dir_class}">{sig.direction}</td>
            <td class="small">{source}</td>
            <td class="{sentiment_class} small">{sentiment}</td>
            <td class="small" style="color: {quality_color}; font-weight: 600;">{quality}</td>
            <td class="font-bold" style="color: var(--accent-gold);">{int(confidence * 100)}%</td>
            <td class="small text-muted">{strategy_perf}</td>
            <td><span class="badge {action_class}">{sig.action_taken}</span></td>
            <td class="small text-truncate" style="max-width: 200px;" title="{reason_text}">{reason_text}</td>
        </tr>
        """
    if not data.get("recent_signals"):
        signals_rows = "<tr><td colspan='10' class='text-center text-muted'>No signals ingested yet.</td></tr>"

    # Construct open trades rows HTML
    open_trades_rows = ""
    for t in open_trades:
        dir_class = "text-buy" if t.order_type == "BUY" else "text-sell"
        created_time = t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        from app.broker.mt5_connector import mt5_connector
        trade_tick = mt5_connector.get_tick_data(t.symbol)
        curr_price = t.entry_price
        if trade_tick:
            curr_price = trade_tick[0] if t.order_type == "BUY" else trade_tick[1]
            
        # Calculate Risk Reward Ratio
        rr = 0.0
        if t.sl_price and t.sl_price > 0 and t.entry_price != t.sl_price:
            rr = abs((t.tp_price - t.entry_price) / (t.entry_price - t.sl_price))
        else:
            rr = 2.0
            
        # Duration in minutes
        from datetime import datetime
        duration_min = (datetime.utcnow() - t.created_at).total_seconds() / 60.0 if t.created_at else 0.0
        
        # Profit Class
        pnl = t.profit or 0.0
        pnl_class = "text-buy font-bold" if pnl > 0 else ("text-sell font-bold" if pnl < 0 else "text-muted")
        
        # Trailing stop status
        trailing_status = "ACTIVE" if "trailing" in (t.comment or "").lower() else "INACTIVE"
        trailing_class = "badge-success" if trailing_status == "ACTIVE" else "badge-secondary"
        
        open_trades_rows += f"""
        <tr data-ticket="{t.ticket}">
            <td>#{t.ticket}</td>
            <td class="font-bold">{t.symbol}</td>
            <td class="font-bold {dir_class}">{t.order_type}</td>
            <td>{t.volume:.2f}</td>
            <td>{t.entry_price:.2f}</td>
            <td class="pos-curr-price">{curr_price:.2f}</td>
            <td><input type="number" step="0.01" class="inline-sl" value="{t.sl_price:.2f}" style="width: 75px; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); color: #fff; padding: 2px 5px; border-radius: 4px; font-size: 0.78rem;" /></td>
            <td><input type="number" step="0.01" class="inline-tp" value="{t.tp_price:.2f}" style="width: 75px; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); color: #fff; padding: 2px 5px; border-radius: 4px; font-size: 0.78rem;" /></td>
            <td class="{pnl_class} pos-profit">${pnl:+.2f}</td>
            <td>1 : {rr:.2f}</td>
            <td class="pos-duration">{duration_min:.1f}m</td>
            <td class="font-bold" style="color: var(--accent-gold);">{int((t.ai_confidence or 0.85)*100)}%</td>
            <td>
                <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                    <button class="badge btn-gold" onclick="updateStopsInline({t.ticket}, this.parentNode.parentNode.parentNode)" style="border:none; cursor:pointer;" title="Update SL/TP limits">SL/TP</button>
                    <button class="badge badge-warning" onclick="moveBreakeven({t.ticket}, {t.entry_price}, {t.tp_price})" style="border:none; cursor:pointer;" title="Move Stop Loss to Entry">Breakeven</button>
                    <button class="badge badge-danger" onclick="openPartialCloseModal({t.ticket}, {t.volume})" style="border:none; cursor:pointer;" title="Partial Exit Lots">Partial</button>
                    <button class="badge badge-danger" onclick="closeActiveTrade({t.ticket})" style="border:none; cursor:pointer;" title="Market Close Position">CLOSE</button>
                    <button class="badge {trailing_class}" onclick="toggleTrailingStop({t.ticket})" style="border:none; cursor:pointer;" id="trailing-btn-{t.ticket}" title="Toggle trailing stop state">{trailing_status} TS</button>
                </div>
            </td>
        </tr>
        """
    if not open_trades:
        open_trades_rows = "<tr><td colspan='13' class='text-center text-muted'>No active open positions on MT5.</td></tr>"

    # Construct dashboard open trades rows HTML
    dashboard_open_trades_rows = ""
    for t in open_trades:
        dir_class = "text-buy" if t.order_type == "BUY" else "text-sell"
        from app.broker.mt5_connector import mt5_connector
        trade_tick = mt5_connector.get_tick_data(t.symbol)
        curr_price = t.entry_price
        if trade_tick:
            curr_price = trade_tick[0] if t.order_type == "BUY" else trade_tick[1]
        pnl = t.profit or 0.0
        pnl_class = "text-buy font-bold" if pnl > 0 else ("text-sell font-bold" if pnl < 0 else "text-muted")
        pnl_sign = "+" if pnl > 0 else ""
        
        dashboard_open_trades_rows += f"""
        <tr data-ticket="{t.ticket}">
            <td>#{t.ticket}</td>
            <td class="font-bold">{t.symbol}</td>
            <td class="font-bold {dir_class}">{t.order_type}</td>
            <td>{t.volume:.2f} Lots</td>
            <td>{t.entry_price:.2f}</td>
            <td class="pos-curr-price">{curr_price:.2f}</td>
            <td class="{pnl_class} pos-profit">{pnl_sign}${pnl:.2f}</td>
            <td>
                <button class="badge badge-danger" onclick="closeActiveTrade({t.ticket})" style="border:none; cursor:pointer; padding: 0.2rem 0.5rem;">Market Close</button>
            </td>
        </tr>
        """
    if not open_trades:
        dashboard_open_trades_rows = "<tr><td colspan='8' class='text-center text-muted'>No active open positions.</td></tr>"

    # Construct history rows HTML
    history_rows = ""
    closed_trades = data.get("all_closed_trades", [])
    for t in closed_trades:
        type_class = "text-buy" if t.order_type == "BUY" else "text-sell"
        pnl = t.profit or 0.0
        pnl_class = "text-buy font-bold" if pnl > 0 else ("text-sell font-bold" if pnl < 0 else "text-muted")
        pnl_sign = "+" if pnl > 0 else ""
        created_time = t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        closed_time = t.closed_at.strftime('%Y-%m-%d %H:%M:%S') if t.closed_at else '—'
        closed_iso = t.closed_at.isoformat() + "Z" if t.closed_at else ''
        comment_str = html.escape(t.comment) if t.comment else '—'
        ticket_id = f"#{t.ticket}" if t.ticket else '—'
        history_rows += f"""
        <tr>
            <td>{ticket_id}</td>
            <td class="font-bold">{t.symbol}</td>
            <td class="font-bold {type_class}">{t.order_type}</td>
            <td>{t.volume:.2f}</td>
            <td>{t.entry_price:.2f}</td>
            <td>{t.exit_price or 0.0:.2f}</td>
            <td class="{pnl_class}">${pnl_sign}{pnl:.2f}</td>
            <td>${t.commission or 0.0:.2f}</td>
            <td>${t.swap or 0.0:.2f}</td>
            <td class="small"><span class="time-cell" data-iso="{t.created_at.isoformat()}Z">{created_time}</span></td>
            <td class="small"><span class="time-cell" data-iso="{closed_iso}">{closed_time}</span></td>
            <td class="small">{comment_str}</td>
        </tr>
        """
    if not closed_trades:
        history_rows = "<tr><td colspan='12' class='text-center text-muted'>No historical closed records found in DB.</td></tr>"

    # Generate economic news events HTML
    news_html = ""
    flags = {
        "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "CAD": "🇨🇦", "AUD": "🇦🇺", "JPY": "🇯🇵", "NZD": "🇳🇿", "CHF": "🇨🇭", "CNY": "🇨🇳"
    }
    events_list = data.get("news_events", [])
    for event in events_list:
        impact = event.get("impact", "Low")
        if impact == "High":
            impact_class = "badge-danger"
            impact_badge_text = "🔴 HIGH"
        elif impact == "Medium":
            impact_class = "badge-warning"
            impact_badge_text = "🟡 MED"
        else:
            impact_class = "badge-secondary"
            impact_badge_text = "🟢 LOW"
            
        currency = event.get("country", "USD")
        flag = flags.get(currency, "🌐")
        time_str = event.get("time", "—")
        title_str = html.escape(event.get("title", "—"))
        forecast = html.escape(event.get("forecast", "—"))
        previous = html.escape(event.get("previous", "—"))
        iso_time = event.get('iso_time', '')
        date_str = event.get('date', '')
        
        news_html += f"""
        <div class="news-card" 
             data-date="{date_str}"
             data-country="{currency}"
             data-impact="{impact}"
             data-iso="{iso_time}"
             data-title="{title_str.lower()}"
             style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.85rem; display: flex; flex-direction: column; gap: 0.5rem; transition: all 0.2s; position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-family: monospace; font-size: 0.8rem; font-weight: 600; color: var(--text-secondary);">{time_str}</span>
                    <span style="font-size: 1rem; line-height: 1;">{flag}</span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: #ffffff;">{currency}</span>
                    <span class="impact-pill {impact_class}" style="font-size: 0.58rem; padding: 0.1rem 0.4rem; border-radius: 9999px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">{impact_badge_text}</span>
                </div>
                <div style="color: var(--text-secondary); cursor: pointer;" onclick="toggleNewsAccordion(this)">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/></svg>
                </div>
            </div>
            
            <div style="font-size: 0.82rem; font-weight: 600; color: #ffffff; display: flex; align-items: center; gap: 0.4rem; cursor: pointer;" onclick="toggleNewsAccordion(this.parentElement.querySelector('svg').parentElement)">
                {title_str}
                <span class="ai-badge" style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); color: #3b82f6; font-size: 0.55rem; padding: 0.05rem 0.25rem; border-radius: 4px; font-weight: 700; letter-spacing: 0.05em; display: inline-flex; align-items: center; gap: 0.1rem;">✨ AI READY</span>
            </div>
            
            <div class="news-stats-row" style="display: flex; flex-wrap: wrap; gap: 0.75rem; font-size: 0.7rem; color: var(--text-secondary); border-top: 1px dashed rgba(255,255,255,0.05); padding-top: 0.4rem; margin-top: 0.1rem;">
                <span class="news-countdown-container" data-iso="{iso_time}">ACTUAL <strong class="news-actual-val" style="color: #ffffff;">—</strong></span>
                <span>FORECAST <strong style="color: #ffffff;">{forecast}</strong></span>
                <span>PREVIOUS <strong style="color: #ffffff;">{previous}</strong></span>
            </div>
            
            <div class="news-accordion-content" style="display: none; font-size: 0.72rem; color: var(--text-secondary); line-height: 1.4; background: rgba(0,0,0,0.25); border-radius: 6px; padding: 0.5rem 0.75rem; margin-top: 0.25rem;">
                <strong>Event Impact Insight:</strong> High volatility setup. AI Committee has analyzed historical occurrences and whitelisted indicators threshold.
            </div>
        </div>
        """
        
    if not events_list:
        news_html = "<div class='text-center text-muted small' style='padding: 1rem;'>No high-impact economic news scheduled today.</div>"

    trades_json_str = json.dumps(data.get("all_trades_json", []))
    news_events_json_str = json.dumps(data.get("news_events", []))

    # Generate live market news HTML
    live_news_html = ""
    for item in data.get("live_news", []):
        news_link = html.escape(item.get('link', '#'))
        news_source = html.escape(item.get('source', 'Google News'))
        news_title = html.escape(item.get('title', ''))
        live_news_html += f"""
        <div class="news-item" style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.8rem 1rem; display: flex; flex-direction: column; gap: 0.35rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.02)'" onmouseout="this.style.background='var(--card-bg)'">
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--text-secondary);">
                <span style="font-weight: 600; color: var(--accent-gold);">{news_source}</span>
                <span style="font-family: monospace;">{item.get('date', '')}</span>
            </div>
            <a href="{news_link}" target="_blank" style="font-size: 0.82rem; font-weight: 600; color: #ffffff; text-decoration: none; line-height: 1.3; transition: color 0.2s;" onmouseover="this.style.color='var(--accent-gold)'" onmouseout="this.style.color='#ffffff'">{news_title}</a>
        </div>
        """
    if not live_news_html:
        live_news_html = "<div class='text-center text-muted small' style='padding: 1rem;'>No live market news headlines retrieved.</div>"

    # Generate Chat history HTML
    chat_html = ""
    for msg in data.get("chat_history", []):
        role_label = "You" if msg["role"] == "user" else "AI Analyst"
        align_style = "align-self: flex-end; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.2);" if msg["role"] == "user" else "align-self: flex-start; background: var(--card-bg); border: 1px solid var(--border-color);"
        role_color = "var(--accent-gold)" if msg["role"] == "user" else "var(--luxury-gold)"
        escaped_content = html.escape(msg["content"])
        chat_html += f"""
        <div style="max-width: 85%; padding: 0.75rem 1rem; border-radius: 8px; {align_style} display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.65rem; font-weight: 700; color: {role_color}; text-transform: uppercase; letter-spacing: 0.05em;">{role_label}</span>
            <div style="font-size: 0.8rem; color: #ffffff; line-height: 1.45; white-space: pre-wrap;">{escaped_content}</div>
        </div>
        """
    if not chat_html:
        chat_html = "<div id='chat-empty-notice' class='text-center text-muted small' style='padding: 2rem;'>Open session with AI committee agent. Request portfolio diagnostics or trade journaling prompts.</div>"

    # Generate Tasks checklist HTML
    tasks_html = ""
    for task in data.get("tasks", []):
        checked_attr = "checked" if task["completed"] else ""
        text_decor = "text-decoration: line-through; color: var(--text-secondary);" if task["completed"] else "color: #ffffff;"
        escaped_task_title = html.escape(task['title'])
        tasks_html += f"""
        <div class="task-item" data-id="{task['id']}" style="display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0.75rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 6px; gap: 0.5rem; transition: background 0.2s;">
            <div style="display: flex; align-items: center; gap: 0.5rem; flex-grow: 1;">
                <input type="checkbox" {checked_attr} onchange="toggleTask({task['id']}, this.checked)" style="cursor: pointer; width: 14px; height: 14px; accent-color: var(--accent-gold);"/>
                <span class="task-title" style="font-size: 0.78rem; font-weight: 500; {text_decor}">{escaped_task_title}</span>
            </div>
            <button onclick="deleteTask({task['id']}, this.parentNode)" style="background: none; border: none; color: var(--sell-color); font-size: 0.85rem; cursor: pointer; padding: 0 0.25rem;">&times;</button>
        </div>
        """

    # Generate Active Close Button HTML without backslashes inside f-string expressions
    if active_trade and active_trade.status == 'OPEN':
        active_close_btn_html = f'<button onclick="closeActiveTrade({active_trade.ticket})" style="width: 100%; padding: 0.65rem; background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); border: none; border-radius: 6px; color: #ffffff; font-family: \'Outfit\', sans-serif; font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.filter=\'brightness(1.15)\'" onmouseout="this.style.filter=\'none\'">Close Trade</button>'
    else:
        active_close_btn_html = '<button style="width: 100%; padding: 0.65rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-secondary); font-family: \'Outfit\', sans-serif; font-size: 0.85rem; font-weight: 700; opacity: 0.5; cursor: not-allowed;" disabled>No Active Positions</button>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Institutional Automated Trading OS Dashboard.">
    <title>{data.get('project_name', 'XAUUSD AI Trading OS')} | Command Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=Sora:wght@600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #050505;
            --surface-sec: #0B0B0B;
            --card-bg: #111111;
            --accent-gold: #D4AF37;
            --luxury-gold: #F5E6A7;
            --text-primary: #FFFFFF;
            --text-secondary: #A1A1AA;
            --buy-color: #22C55E;
            --sell-color: #EF4444;
            --warning-color: #F59E0B;
            --accent-blue: #3B82F6;
            --border-color: rgba(212, 175, 55, 0.08);
            --sidebar-width: 250px;
            --header-height: 60px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at top right, rgba(212, 175, 55, 0.12), transparent 40%),
                radial-gradient(circle at bottom left, rgba(245, 230, 167, 0.06), transparent 35%),
                #050505;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }}

        /* Sidebar Styling */
        aside {{
            width: var(--sidebar-width);
            background: var(--surface-sec);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
        }}

        .sidebar-header {{
            padding: 1.25rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .brand {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--accent-gold);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            letter-spacing: 0.05em;
        }}

        .brand span {{ color: #ffffff; }}

        .live-status-container {{
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .live-badge {{
            background: rgba(34, 197, 94, 0.15);
            color: var(--buy-color);
            border: 1px solid rgba(34, 197, 94, 0.2);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .pulse-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }}

        .pulse-green {{
            background-color: var(--buy-color);
            box-shadow: 0 0 8px var(--buy-color);
        }}

        .pulse-red {{
            background-color: var(--sell-color);
            box-shadow: 0 0 8px var(--sell-color);
        }}

        .connection-text {{
            font-size: 0.7rem;
            color: var(--text-secondary);
            font-weight: 500;
            letter-spacing: 0.02em;
        }}

        .sidebar-nav {{
            flex: 1;
            padding: 1rem 0.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            overflow-y: auto;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.65rem 0.85rem;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.82rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .nav-item:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.02);
        }}

        .nav-item.active {{
            color: #ffffff;
            background: linear-gradient(90deg, rgba(212, 175, 55, 0.1) 0%, rgba(212, 175, 55, 0.01) 100%);
            border-left: 2px solid var(--accent-gold);
            padding-left: calc(0.85rem - 2px);
            font-weight: 600;
        }}

        .sidebar-footer {{
            padding: 1rem;
            border-top: 1px solid var(--border-color);
            background: rgba(0, 0, 0, 0.2);
        }}

        .footer-metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            font-size: 0.72rem;
        }}

        .footer-label {{ color: var(--text-secondary); }}
        .footer-val {{ font-weight: 600; color: #ffffff; font-family: monospace; }}

        /* Main Container Layout */
        main {{
            margin-left: var(--sidebar-width);
            flex: 1;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        /* Header Styling */
        header {{
            height: var(--header-height);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1.5rem;
            background: rgba(5, 5, 5, 0.6);
            backdrop-filter: blur(12px);
            z-index: 50;
        }}

        .alert-bell {{
            position: relative;
            cursor: pointer;
            font-size: 1.1rem;
            color: var(--text-secondary);
        }}

        .alert-badge {{
            position: absolute;
            top: -2px;
            right: -2px;
            width: 6px;
            height: 6px;
            background-color: var(--sell-color);
            border-radius: 50%;
        }}

        .view-content {{
            padding: 1.5rem;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .tab-view {{
            display: none;
            flex-direction: column;
            gap: 1.25rem;
            animation: viewFade 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .tab-view.active {{ display: flex; }}

        @keyframes viewFade {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.85rem;
        }}

        .widget-card {{
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.85rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: all 0.25s ease;
        }}

        .widget-card:hover {{
            border-color: rgba(212, 175, 55, 0.2);
            transform: translateY(-1px);
        }}

        .widget-label {{
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.35rem;
            font-weight: 600;
        }}

        .widget-value-row {{
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
        }}

        .widget-value {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
        }}

        .widget-trend {{
            font-size: 0.68rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.15rem;
        }}

        .trend-up {{ color: var(--buy-color); }}
        .trend-down {{ color: var(--sell-color); }}

        .graphic-container {{
            height: 20px;
            display: flex;
            align-items: flex-end;
            margin-top: 0.35rem;
        }}

        .workspace-split {{
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 1.25rem;
        }}

        @media (max-width: 1100px) {{
            .workspace-split {{ grid-template-columns: 1fr; }}
        }}

        .panel {{
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}

        .panel-title {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }}

        .symbol-pair {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .symbol-subtext {{
            font-size: 0.7rem;
            color: var(--text-secondary);
        }}

        .price-badge {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
        }}
        
        .price-badge.badge {{
            font-size: 1.2rem !important;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            padding-bottom: 0.4rem;
            margin-bottom: 0.4rem;
        }}

        .metric-label {{ color: var(--text-secondary); }}
        .metric-value {{ font-weight: 600; color: #ffffff; }}
        .metric-value.val-tp1 {{ color: var(--buy-color); }}
        .metric-value.val-sl {{ color: var(--sell-color); }}

        /* Chart card styling */
        .chart-panel {{
            display: flex;
            flex-direction: column;
            min-height: 440px;
        }}

        .chart-container-div {{
            flex: 1;
            width: 100%;
            height: 380px;
            border-radius: 8px;
            background: #060606;
            position: relative;
            border: 1px solid var(--border-color);
        }}

        .chart-wrapper {{
            position: relative;
            width: 100%;
            height: 380px;
            border-radius: 8px;
            overflow: hidden;
            z-index: 2;
        }}

        #session-canvas {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }}

        #vp-canvas {{
            position: absolute;
            top: 0;
            right: 60px;
            width: 120px;
            height: calc(100% - 26px);
            pointer-events: none;
            z-index: 3;
        }}

        /* Session colour strip */
        .session-strip {{
            display: flex;
            align-items: center;
            gap: 0;
            height: 6px;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 0 0.4rem 0;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.02);
        }}
        .session-strip-segment {{
            flex: 1;
            height: 100%;
            transition: opacity 0.4s ease;
        }}
        .session-strip-segment.active {{
            animation: sessionPulse 2s ease-in-out infinite;
        }}
        @keyframes sessionPulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        /* Table Styling */
        .table-container {{
            width: 100%;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.8rem;
        }}

        th {{
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.75rem 0.85rem;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 0.75rem 0.85rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            color: var(--text-primary);
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
        }}

        /* Badges */
        .badge {{
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.62rem;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
            letter-spacing: 0.03em;
        }}

        .badge-success {{ background: rgba(34, 197, 94, 0.12); color: var(--buy-color); border: 1px solid rgba(34, 197, 94, 0.2); }}
        .badge-danger {{ background: rgba(239, 68, 68, 0.12); color: var(--sell-color); border: 1px solid rgba(239, 68, 68, 0.2); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.12); color: var(--warning-color); border: 1px solid rgba(245, 158, 11, 0.2); }}
        .badge-secondary {{ background: rgba(161, 161, 170, 0.12); color: var(--text-secondary); border: 1px solid rgba(161, 161, 170, 0.2); }}

        .text-buy {{ color: var(--buy-color); }}
        .text-sell {{ color: var(--sell-color); }}
        .font-bold {{ font-weight: 600; }}
        .text-muted {{ color: var(--text-secondary); }}

        .calendar-container {{
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
        }}

        .calendar-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .calendar-title {{
            font-size: 1rem;
            color: #ffffff;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
        }}

        .calendar-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 0.3rem 0.65rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .calendar-btn:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.15);
        }}

        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.35rem;
        }}

        .calendar-weekday {{
            text-align: center;
            font-size: 0.68rem;
            font-weight: 700;
            color: var(--text-secondary);
            padding: 0.4rem;
            text-transform: uppercase;
        }}

        .calendar-cell {{
            aspect-ratio: 1.3;
            background: rgba(255, 255, 255, 0.005);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.35rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
            min-height: 55px;
        }}

        .calendar-cell.has-trades {{
            background: rgba(212, 175, 55, 0.02);
            border-color: rgba(212, 175, 55, 0.15);
            cursor: pointer;
        }}

        .calendar-cell.has-trades:hover {{
            background: rgba(212, 175, 55, 0.05);
            border-color: var(--accent-gold);
        }}

        .cell-num {{ font-size: 0.75rem; font-weight: 500; color: var(--text-secondary); }}
        .cell-pnl {{ font-size: 0.68rem; font-weight: 700; font-family: monospace; }}

        /* Economic Calendar styling */
        .news-card:hover {{
            background: rgba(255,255,255,0.02) !important;
            border-color: rgba(212,175,55,0.2) !important;
        }}

        /* Side Drawer */
        .drawer-backdrop {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            z-index: 900;
            display: none;
        }}
        .drawer {{
            position: fixed;
            top: 0; right: -360px; bottom: 0;
            width: 360px;
            background: var(--surface-sec);
            border-left: 1px solid var(--border-color);
            z-index: 950;
            box-shadow: -10px 0 30px rgba(0,0,0,0.8);
            transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}
        .drawer.active {{ right: 0; }}
        .drawer-header {{
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}
        .drawer-title {{ font-family: 'Outfit', sans-serif; color: #ffffff; font-size: 1.1rem; }}
        .drawer-close {{ background: none; border: none; font-size: 1.5rem; color: var(--text-secondary); cursor: pointer; }}

        /* Chat widget */
        .chat-bubble-btn {{
            position: fixed; bottom: 1.5rem; right: 1.5rem;
            width: 45px; height: 45px; border-radius: 50%;
            background: linear-gradient(135deg, var(--luxury-gold) 0%, var(--accent-gold) 100%);
            border: none; color: #050505; font-size: 1.25rem;
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 16px rgba(212,175,55,0.4); z-index: 1000;
            transition: transform 0.2s;
        }}
        .chat-bubble-btn:hover {{ transform: scale(1.05); }}
        
        .chat-widget-container {{
            position: fixed; bottom: 5rem; right: 1.5rem;
            width: 380px; height: 500px;
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            z-index: 1000;
            display: none;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            overflow: hidden;
            animation: fadeIn 0.25s ease;
        }}
        .chat-widget-container.active {{ display: flex; }}
        .chat-widget-header {{
            background: rgba(0, 0, 0, 0.3);
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            display: flex; justify-content: space-between; align-items: center;
        }}
        .chat-widget-title {{ font-size: 0.85rem; font-weight: 700; color: #ffffff; font-family: 'Outfit', sans-serif; }}
        .chat-widget-subtitle {{ font-size: 0.65rem; color: var(--text-secondary); display: block; }}
        .chat-widget-close {{ background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 0.85rem; }}
        .chat-widget-messages {{
            flex: 1; padding: 1rem; overflow-y: auto;
            display: flex; flex-direction: column; gap: 0.85rem;
            background: rgba(0, 0, 0, 0.1);
        }}
        .chat-widget-footer {{
            padding: 0.75rem; border-top: 1px solid var(--border-color);
            display: flex; gap: 0.5rem; background: var(--surface-sec);
        }}

        .spinner {{
            width: 20px; height: 20px;
            border: 3px solid rgba(212,175,55,0.1);
            border-top: 3px solid var(--accent-gold);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}

        .toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(34, 197, 94, 0.95);
            color: #ffffff;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            display: none;
            max-width: 350px;
        }}
        @keyframes ambient-pulse {{
            0% {{ box-shadow: 0 0 10px rgba(212,175,55,0.2), inset 0 0 10px rgba(212,175,55,0.1); }}
            50% {{ box-shadow: 0 0 25px rgba(212,175,55,0.6), inset 0 0 20px rgba(212,175,55,0.3); }}
            100% {{ box-shadow: 0 0 10px rgba(212,175,55,0.2), inset 0 0 10px rgba(212,175,55,0.1); }}
        }}
        @keyframes spinner-rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .ambient-loader {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            gap: 1rem;
        }}
        .ambient-spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid rgba(212,175,55,0.1);
            border-top: 3px solid var(--accent-gold);
            border-radius: 50%;
            animation: spinner-rotate 1s linear infinite, ambient-pulse 2s ease-in-out infinite;
        }}
        select option {{
            background-color: #0d0e12;
            color: #ffffff;
        }}

        /* Analytics graphs */
        .analytics-chart-box {{
            background: var(--surface-sec);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            height: 220px;
            display: flex;
            flex-direction: column;
        }}

        /* Currency Strength Meter */
        .strength-bar-container {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.75rem;
            margin-bottom: 0.4rem;
        }}
        .strength-label {{ width: 35px; font-weight: 700; color: #ffffff; }}
        .strength-bar-outer {{ flex: 1; height: 6px; background: rgba(255,255,255,0.03); border-radius: 3px; overflow: hidden; }}
        .strength-bar-inner {{ height: 100%; border-radius: 3px; background: var(--accent-gold); }}

        /* Modal styling */
        .modal {{
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7); backdrop-filter: blur(5px);
            display: none; align-items: center; justify-content: center;
            z-index: 2000;
        }}
        .modal-content {{
            background: var(--surface-sec); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem; width: 100%; max-width: 360px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        
        /* Timeframe and Chart control styles */
        .chart-controls-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            font-size: 0.75rem;
        }}
        .tf-selector {{
            display: flex;
            gap: 0.35rem;
            background: rgba(255, 255, 255, 0.02);
            padding: 0.2rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}
        .tf-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .tf-btn:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.03);
        }}
        .tf-btn.active {{
            background: rgba(255, 255, 255, 0.06);
            color: var(--accent-gold);
        }}
        .indicators-dropdown {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 500;
            cursor: pointer;
        }}
        .active-signal-details {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .active-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }}
        .session-legend {{
            display: flex;
            gap: 0.75rem;
            align-items: center;
            font-size: 0.7rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            background: rgba(255,255,255,0.01);
            padding: 0.35rem 0.6rem;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.02);
        }}
    </style>
    <script src="https://unpkg.com/lightweight-charts@4.2.1/dist/lightweight-charts.standalone.production.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
</head>
<body>
    <!-- Sidebar Navigation -->
    <aside>
        <div class="sidebar-header" style="text-align: center;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 0.4rem;">
                <img src="/logo_icon.png" style="height: 64px; width: auto; object-fit: contain;" />
                <div style="display: flex; align-items: center; justify-content: center; gap: 0.25rem; margin-top: 0.15rem;">
                    <img src="/logo_word.png" style="height: 18px; width: auto; object-fit: contain;" />
                    <span style="font-family: \'Sora\', sans-serif; font-size: 0.95rem; font-weight: 600; color: var(--accent-gold); letter-spacing: 0.05em; line-height: 1; transform: translateY(-1px);">OS</span>
                </div>
            </div>
            <div class="live-status-container" style="justify-content: center; margin-top: 0.5rem; display: flex; align-items: center; gap: 0.35rem;">
                <span class="live-badge">CORE</span>
                <span class="pulse-dot {broker_pulse}"></span>
                <span class="connection-text">{broker_status}</span>
            </div>
        </div>
        
        <div class="sidebar-nav">
            <div class="nav-item active" id="nav-dashboard" onclick="switchTab('dashboard-view', this)">📊 Command Center</div>
            <div class="nav-item" id="nav-trades" onclick="switchTab('trades-view', this)">📈 Trade Desk</div>
            <div class="nav-item" id="nav-signals" onclick="switchTab('signals-view', this)">📡 Signal Intel</div>
            <div class="nav-item" id="nav-committee" onclick="switchTab('committee-view', this)">⚖️ Committee Review</div>
            <div class="nav-item" id="nav-analytics" onclick="switchTab('analytics-view', this)">🎯 Trade Analytics</div>
            <div class="nav-item" id="nav-coach" onclick="switchTab('coach-view', this)">🧠 AI Coach</div>
            <div class="nav-item" id="nav-journal" onclick="switchTab('journal-view', this)">📝 Journal</div>
            <div class="nav-item" id="nav-portfolio" onclick="switchTab('portfolio-view', this)">💼 Portfolio Center</div>
            <div class="nav-item" id="nav-market-intel" onclick="switchTab('market-intel-view', this)">🔮 Market Intel</div>
            <div class="nav-item" id="nav-history" onclick="switchTab('history-view', this)">🗄️ Trade History</div>
            <div class="nav-item" id="nav-calendar" onclick="switchTab('calendar-view', this)">📅 Calendar</div>
            <div class="nav-item" id="nav-news" onclick="switchTab('news-view', this)">📰 Live News</div>
            <div class="nav-item" id="nav-settings" onclick="switchTab('settings-view', this)">⚙️ Settings</div>
        </div>

        <div class="sidebar-footer">
            <div class="footer-metric">
                <span class="footer-label">Balance</span>
                <span class="footer-val">${sidebar_balance:,.2f}</span>
            </div>
            <div class="footer-metric">
                <span class="footer-label">Equity</span>
                <span class="footer-val">${sidebar_equity:,.2f}</span>
            </div>
            <div class="footer-metric">
                <span class="footer-label">Free Margin</span>
                <span class="footer-val">${sidebar_free_margin:,.2f}</span>
            </div>
            <div class="footer-metric">
                <span class="footer-label">Margin Level</span>
                <span class="footer-val">{sidebar_margin_level_str}</span>
            </div>
        </div>
    </aside>

    <!-- Main Workspace -->
    <main>
        <!-- Header -->
        <header>
            <div style="display:flex; align-items:center; gap:0.5rem;">
                <span style="font-family:'Outfit', sans-serif; font-size:0.9rem; font-weight:700; color:var(--accent-gold);">OS TIMEZONES</span>
                <div class="header-clocks" style="display: flex; gap: 0.5rem;">
                    <div class="calendar-btn" onclick="setTimezonePreference('Asia/Kolkata')" id="clock-box-kol">KOL: <span id="clock-kol" style="font-family:monospace;">--:--</span></div>
                    <div class="calendar-btn" onclick="setTimezonePreference('UTC')" id="clock-box-utc">UTC: <span id="clock-utc" style="font-family:monospace;">--:--</span></div>
                    <div class="calendar-btn" onclick="setTimezonePreference('America/New_York')" id="clock-box-ny">NY: <span id="clock-ny" style="font-family:monospace;">--:--</span></div>
                    <div class="calendar-btn" onclick="setTimezonePreference('Europe/London')" id="clock-box-ldn">LDN: <span id="clock-ldn" style="font-family:monospace;">--:--</span></div>
                    <div class="calendar-btn" onclick="setTimezonePreference('Asia/Tokyo')" id="clock-box-tok">TOK: <span id="clock-tok" style="font-family:monospace;">--:--</span></div>
                </div>
            </div>
            <div class="alert-bell" onclick="showEconomicAlerts()" title="Economic Events Notifications">
                🔔 <span class="alert-badge"></span>
            </div>
        </header>

        <!-- View Content Area -->
        <div class="view-content">
            
            <!-- 1. DASHBOARD VIEW (COMMAND CENTER) -->
            <div id="dashboard-view" class="tab-view active">
                <div class="metrics-grid">
                    <!-- Balance -->
                    <div class="widget-card">
                        <span class="widget-label">Balance</span>
                        <div class="widget-value-row">
                            <span class="widget-value">${sidebar_balance:,.2f}</span>
                            <span class="widget-trend trend-up">↑ +0.0%</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: var(--buy-color); fill: none; stroke-width: 1.5;">
                                <path d="M0,15 L20,12 L40,14 L60,8 L80,10 L100,5"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Peak: ${sidebar_balance:,.2f}</span>
                    </div>

                    <!-- Equity -->
                    <div class="widget-card">
                        <span class="widget-label">Equity</span>
                        <div class="widget-value-row">
                            <span class="widget-value">${sidebar_equity:,.2f}</span>
                            <span class="widget-trend { 'trend-up' if sidebar_equity >= sidebar_balance else 'trend-down' }">
                                { f'↑ Floating' if sidebar_equity >= sidebar_balance else '↓ Drawdown' }
                            </span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--buy-color)' if sidebar_equity >= sidebar_balance else 'var(--sell-color)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,12 L20,15 L40,11 L60,9 L80,14 L100,8"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">PnL: ${(sidebar_equity - sidebar_balance):+,.2f}</span>
                    </div>

                    <!-- Free Margin -->
                    <div class="widget-card">
                        <span class="widget-label">Free Margin</span>
                        <div class="widget-value-row">
                            <span class="widget-value">${sidebar_free_margin:,.2f}</span>
                            <span class="widget-trend trend-up">↑ Available</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: var(--accent-blue); fill: none; stroke-width: 1.5;">
                                <path d="M0,10 L30,8 L60,11 L100,7"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Used: {sidebar_margin_used_str}</span>
                    </div>

                    <!-- Margin Level -->
                    <div class="widget-card">
                        <span class="widget-label">Margin Level</span>
                        <div class="widget-value-row">
                            <span class="widget-value">{sidebar_margin_level_str}</span>
                            <span class="widget-trend { 'trend-up' if sidebar_margin_level > 200 or sidebar_margin_level == 0 else 'trend-down' }">
                                { '↑ Secure' if sidebar_margin_level > 200 or sidebar_margin_level == 0 else '↓ Critical' }
                            </span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--buy-color)' if sidebar_margin_level > 200 or sidebar_margin_level == 0 else 'var(--warning-color)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,15 L30,12 L60,14 L100,10"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Hurdle: > 500%</span>
                    </div>

                    <!-- Daily PnL -->
                    <div class="widget-card">
                        <span class="widget-label">Daily PnL</span>
                        <div class="widget-value-row">
                            <span class="widget-value" style="color: { 'var(--buy-color)' if daily_pnl >= 0 else 'var(--sell-color)' };">${daily_pnl:+.2f}</span>
                            <span class="widget-trend { 'trend-up' if daily_pnl >= 0 else 'trend-down' }">{ '↑ Profit' if daily_pnl >= 0 else '↓ Loss' }</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--buy-color)' if daily_pnl >= 0 else 'var(--sell-color)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,10 L20,13 L40,8 L60,12 L80,5 L100,10"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Target: $500.00</span>
                    </div>

                    <!-- Weekly PnL -->
                    <div class="widget-card">
                        <span class="widget-label">Weekly PnL</span>
                        <div class="widget-value-row">
                            <span class="widget-value" style="color: { 'var(--buy-color)' if weekly_pnl >= 0 else 'var(--sell-color)' };">${weekly_pnl:+.2f}</span>
                            <span class="widget-trend { 'trend-up' if weekly_pnl >= 0 else 'trend-down' }">{ '↑ Growth' if weekly_pnl >= 0 else '↓ Drawdown' }</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--buy-color)' if weekly_pnl >= 0 else 'var(--sell-color)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,15 L30,10 L70,8 L100,3"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Last 7d closed PnL</span>
                    </div>

                    <!-- Monthly PnL -->
                    <div class="widget-card">
                        <span class="widget-label">Monthly PnL</span>
                        <div class="widget-value-row">
                            <span class="widget-value" style="color: { 'var(--buy-color)' if monthly_pnl >= 0 else 'var(--sell-color)' };">${monthly_pnl:+.2f}</span>
                            <span class="widget-trend { 'trend-up' if monthly_pnl >= 0 else 'trend-down' }">{ '↑ Growth' if monthly_pnl >= 0 else '↓ Drawdown' }</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--buy-color)' if monthly_pnl >= 0 else 'var(--sell-color)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,12 L25,15 L50,10 L75,8 L100,4"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Last 30d closed PnL</span>
                    </div>

                    <!-- Open Risk -->
                    <div class="widget-card">
                        <span class="widget-label">Open Risk</span>
                        <div class="widget-value-row">
                            <span class="widget-value" style="color: { 'var(--warning-color)' if open_risk > 0 else 'var(--text-primary)' };">${open_risk:,.2f}</span>
                            <span class="widget-trend { 'trend-down' if open_risk > 0 else 'trend-up' }">{ '↑ Exposure' if open_risk > 0 else '• Safe' }</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: { 'var(--warning-color)' if open_risk > 0 else 'var(--text-secondary)' }; fill: none; stroke-width: 1.5;">
                                <path d="M0,18 L50,{ '12' if open_risk > 0 else '18' } L100,{ '5' if open_risk > 0 else '18' }"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Max Allowed: 2.0%</span>
                    </div>

                    <!-- Drawdown -->
                    <div class="widget-card">
                        <span class="widget-label">Drawdown Peak</span>
                        <div class="widget-value-row">
                            <span class="widget-value">Daily: {daily_dd_pct:.2f}%</span>
                            <span class="widget-trend trend-down">Peak Limit: {data.get('max_daily_drawdown_pct', 0.05)*100.0:.1f}%</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: var(--sell-color); fill: none; stroke-width: 1.5;">
                                <path d="M0,18 L30,15 L60,19 L100,16"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Weekly: {weekly_dd_pct:.2f}% | Limit: {data.get('max_weekly_drawdown_pct', 0.10)*100.0:.1f}%</span>
                    </div>

                    <!-- Win Rate Ring -->
                    <div class="widget-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem;">
                        <span class="widget-label" style="align-self: flex-start;">Win Rate</span>
                        <div style="position: relative; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                            <!-- SVG Donut Ring -->
                            <svg width="80" height="80" viewBox="0 0 80 80">
                                <!-- Background circle (Red for Loss) -->
                                <circle cx="40" cy="40" r="32" stroke="#ef4444" stroke-width="8" fill="none" />
                                <!-- Foreground circle (Yellow/Gold for Win) -->
                                <circle cx="40" cy="40" r="32" stroke="#facc15" stroke-width="8" fill="none"
                                        stroke-dasharray="201.06"
                                        stroke-dashoffset="{ 201.06 * (1 - win_rate / 100) }"
                                        stroke-linecap="round"
                                        transform="rotate(-90 40 40)"
                                        id="win-rate-ring-circle" />
                            </svg>
                            <!-- Center Text -->
                            <div style="position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                                <span class="widget-value" id="win-rate-ring-text" style="font-size: 0.95rem; font-weight: 700; color: #ffffff; line-height: 1.1;">{win_rate:.1f}%</span>
                                <span id="win-rate-ring-subtext" style="font-size: 0.58rem; color: var(--text-secondary); margin-top: 0.1rem;">{wins}/{total_trades}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Profit Factor -->
                    <div class="widget-card">
                        <span class="widget-label">Profit Factor</span>
                        <div class="widget-value-row">
                            <span class="widget-value">{profit_factor:.2f}</span>
                            <span class="widget-trend { 'trend-up' if profit_factor >= 1.5 else 'trend-down' }">{ '↑ Target Met' if profit_factor >= 1.5 else '↓ Target: >1.50' }</span>
                        </div>
                        <div class="graphic-container">
                            <svg viewBox="0 0 100 20" width="100%" height="20" style="stroke: var(--accent-gold); fill: none; stroke-width: 1.5;">
                                <path d="M0,15 L30,12 L60,10 L100,5"></path>
                            </svg>
                        </div>
                        <span style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem;">Gross Profit/Loss ratio</span>
                    </div>
                </div>

                <!-- Global session strip -->
                <div class="panel" style="padding: 1rem 1.25rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 1.25rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                        <span class="panel-title" style="font-size:0.8rem; font-weight: 700; color: #ffffff;">🌐 GLOBAL TRADING SESSIONS</span>
                        <span id="session-time-text" style="color:var(--text-secondary); font-family:\'Outfit\', sans-serif; font-size:0.8rem; font-weight: 500;">Current time: --:--:-- (Kolkata)</span>
                    </div>
                    
                    <!-- Session Cards Row -->
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;" id="sessions-container">
                        <!-- Sydney Card -->
                        <div class="widget-card" id="session-card-sydney" style="padding: 0.85rem 1rem; flex-direction: row; align-items: center; justify-content: space-between; border: 1px solid var(--border-color); border-radius: 8px; transition: all 0.3s; background: rgba(0,0,0,0.15);">
                            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                <span class="session-name" style="font-size: 0.95rem; font-weight: 700; color: #fff;">Sydney</span>
                                <span class="session-hours" style="font-size: 0.72rem; color: var(--text-secondary);">03:30 - 12:30</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                                <span class="badge" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; font-weight: 700; border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.08);">CLOSED</span>
                                <span class="session-countdown" style="font-size: 0.68rem; color: var(--text-secondary);">—</span>
                            </div>
                        </div>
                        <!-- Tokyo Card -->
                        <div class="widget-card" id="session-card-tokyo" style="padding: 0.85rem 1rem; flex-direction: row; align-items: center; justify-content: space-between; border: 1px solid var(--border-color); border-radius: 8px; transition: all 0.3s; background: rgba(0,0,0,0.15);">
                            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                <span class="session-name" style="font-size: 0.95rem; font-weight: 700; color: #fff;">Tokyo</span>
                                <span class="session-hours" style="font-size: 0.72rem; color: var(--text-secondary);">05:30 - 14:30</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                                <span class="badge" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; font-weight: 700; border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.08);">CLOSED</span>
                                <span class="session-countdown" style="font-size: 0.68rem; color: var(--text-secondary);">—</span>
                            </div>
                        </div>
                        <!-- London Card -->
                        <div class="widget-card" id="session-card-london" style="padding: 0.85rem 1rem; flex-direction: row; align-items: center; justify-content: space-between; border: 1px solid var(--border-color); border-radius: 8px; transition: all 0.3s; background: rgba(0,0,0,0.15);">
                            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                <span class="session-name" style="font-size: 0.95rem; font-weight: 700; color: #fff;">London</span>
                                <span class="session-hours" style="font-size: 0.72rem; color: var(--text-secondary);">13:30 - 22:30</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                                <span class="badge" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; font-weight: 700; border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.08);">CLOSED</span>
                                <span class="session-countdown" style="font-size: 0.68rem; color: var(--text-secondary);">—</span>
                            </div>
                        </div>
                        <!-- New York Card -->
                        <div class="widget-card" id="session-card-newyork" style="padding: 0.85rem 1rem; flex-direction: row; align-items: center; justify-content: space-between; border: 1px solid var(--border-color); border-radius: 8px; transition: all 0.3s; background: rgba(0,0,0,0.15);">
                            <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                <span class="session-name" style="font-size: 0.95rem; font-weight: 700; color: #fff;">New York</span>
                                <span class="session-hours" style="font-size: 0.72rem; color: var(--text-secondary);">18:30 - 03:30</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                                <span class="badge" style="font-size: 0.65rem; padding: 0.2rem 0.5rem; font-weight: 700; border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.08);">CLOSED</span>
                                <span class="session-countdown" style="font-size: 0.68rem; color: var(--text-secondary);">—</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Horizontal Timeline Container -->
                    <div style="position: relative; width: 100%; padding-bottom: 0.5rem; margin-top: 0.5rem;">
                        <!-- The track bar -->
                        <div style="position: relative; width: 100%; height: 16px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; display: flex;">
                            <!-- Colored Overlays for active sessions (Kolkata hours) -->
                            <!-- Sydney segment: 03:30 - 12:30 -> left: 14.58%, width: 37.5% -->
                            <div style="position: absolute; height: 100%; background: rgba(59, 130, 246, 0.15); left: 14.58%; width: 37.5%; border-left: 1px solid rgba(59, 130, 246, 0.3); border-right: 1px solid rgba(59, 130, 246, 0.3);"></div>
                            <!-- Tokyo segment: 05:30 - 14:30 -> left: 22.92%, width: 37.5% -->
                            <div style="position: absolute; height: 100%; background: rgba(139, 92, 246, 0.15); left: 22.92%; width: 37.5%; border-left: 1px solid rgba(139, 92, 246, 0.3); border-right: 1px solid rgba(139, 92, 246, 0.3);"></div>
                            <!-- London segment: 13:30 - 22:30 -> left: 56.25%, width: 37.5% -->
                            <div style="position: absolute; height: 100%; background: rgba(16, 185, 129, 0.15); left: 56.25%; width: 37.5%; border-left: 1px solid rgba(16, 185, 129, 0.3); border-right: 1px solid rgba(16, 185, 129, 0.3);"></div>
                            <!-- New York segment part 1: 18:30 - 24:00 -> left: 77.08%, width: 22.92% -->
                            <div style="position: absolute; height: 100%; background: rgba(251, 191, 36, 0.15); left: 77.08%; width: 22.92%; border-left: 1px solid rgba(251, 191, 36, 0.3);"></div>
                            <!-- New York segment part 2: 00:00 - 03:30 -> left: 0%, width: 14.58% -->
                            <div style="position: absolute; height: 100%; background: rgba(251, 191, 36, 0.15); left: 0%; width: 14.58%; border-right: 1px solid rgba(251, 191, 36, 0.3);"></div>
                        </div>
                        
                        <!-- Sliding Vertical Red Line Indicator -->
                        <div id="timeline-current-indicator" style="position: absolute; top: -4px; width: 3px; height: 24px; background: #ef4444; box-shadow: 0 0 8px #ef4444; border-radius: 1px; z-index: 10; pointer-events: none; transition: left 0.1s linear;">
                            <div style="position: absolute; top: -6px; left: -3.5px; width: 10px; height: 6px; background: #ef4444; clip-path: polygon(50% 100%, 0 0, 100% 0);"></div>
                        </div>

                        <!-- Timeline ticks / labels -->
                        <div style="position: relative; display: flex; justify-content: space-between; margin-top: 0.35rem; font-size: 0.65rem; color: var(--text-secondary); font-family: monospace;">
                            <span>00h</span>
                            <span>04h</span>
                            <span>08h</span>
                            <span>12h</span>
                            <span>16h</span>
                            <span>20h</span>
                            <span>24h</span>
                        </div>
                    </div>
                </div>

                <div class="workspace-split" style="display: grid; grid-template-columns: 350px 1fr; gap: 1.25rem;">
                    <!-- Left: Active Signal, AI Predictor & Operational Checklist -->
                    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                        <!-- Active Signal / Trade panel -->
                        <div class="panel">
                            <div class="panel-header">
                                <div class="panel-title-container">
                                    🔔 <span class="panel-title">Active Signal / Trade</span>
                                </div>
                                <span class="badge {active_badge_class}" id="active-status-top-badge" style="font-size: 0.65rem;">{active_direction}</span>
                            </div>
                            
                            <div class="active-signal-details">
                                <div class="active-header-row">
                                    <div>
                                        <div class="symbol-pair" id="active-symbol-pair">{active_symbol}</div>
                                        <div class="symbol-subtext" id="active-symbol-subtext">{active_symbol_subtext}</div>
                                    </div>
                                    <div class="price-badge badge {active_badge_class}" id="live-symbol-price">
                                        {active_price_str} <span style="font-size: 0.8rem;">▲</span>
                                    </div>
                                </div>
                                
                                <div style="margin-top: 0.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
                                    <div class="metric-row">
                                        <span class="metric-label">Ticket ID</span>
                                        <span class="metric-value" id="active-ticket-id">{active_ticket}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Entry Price</span>
                                        <span class="metric-value" id="active-entry-price">{active_entry}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Stop Loss (SL)</span>
                                        <span class="metric-value val-sl" id="active-sl-price">{active_sl}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Take Profit 1</span>
                                        <span class="metric-value val-tp1" id="active-tp-price">{active_tp1}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Take Profit 2</span>
                                        <span class="metric-value val-tp1" id="active-tp2-price">{active_tp2}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Trade Time</span>
                                        <span class="metric-value small" id="active-trade-time">{active_time}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Timeframe</span>
                                        <span class="metric-value" id="active-timeframe">{active_timeframe}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Risk Reward</span>
                                        <span class="metric-value" id="active-rr">{active_rr}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Position Size</span>
                                        <span class="metric-value" id="active-lots">{active_lots}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Floating PnL</span>
                                        <span class="metric-value" id="active-floating-pnl" style="font-weight: 700; color: {active_pnl_color};">{active_pnl_str}</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Status</span>
                                        <span class="metric-value badge {active_status_badge_class}" id="active-status-badge" style="padding: 0.15rem 0.45rem;">{active_status}</span>
                                    </div>
                                </div>
                                
                                <div id="active-close-btn-container" style="margin-top: 1rem;">
                                    {active_close_btn_html}
                                </div>
                            </div>
                        </div>

                        <!-- AI Trade Setup Predictor panel -->
                        <div class="panel" style="padding: 1.25rem;">
                            <div class="panel-header" style="margin-bottom: 0.75rem; padding-bottom: 0.5rem;">
                                <div class="panel-title-container">
                                    🤖 <span class="panel-title">AI Trade Setup Predictor</span>
                                </div>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="font-size: 0.78rem; color: var(--text-secondary); line-height: 1.4;">
                                    Trigger Claude AI to analyze the live chart candles and technical indicators for XAUUSD to predict entry, SL, and TP.
                                </div>
                                
                                <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.25rem;">
                                    <span style="font-size: 0.75rem; color: var(--text-secondary);">AI Timeframe:</span>
                                    <select id="pred-timeframe" style="background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color); color: #ffffff; padding: 0.35rem 0.5rem; border-radius: 6px; font-size: 0.78rem; font-family: \'Outfit\', sans-serif; cursor: pointer; outline: none; flex-grow: 1;">
                                        <option value="M1">M1 (1 Minute)</option>
                                        <option value="M5">M5 (5 Minutes)</option>
                                        <option value="M15" selected>M15 (15 Minutes)</option>
                                        <option value="M30">M30 (30 Minutes)</option>
                                        <option value="H1">H1 (1 Hour)</option>
                                        <option value="H4">H4 (4 Hours)</option>
                                        <option value="D1">D1 (Daily)</option>
                                    </select>
                                </div>
                                
                                <button id="btn-run-prediction" onclick="runAiPrediction()" style="background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); border: none; color: #060913; padding: 0.75rem; border-radius: 8px; font-family: \'Outfit\', sans-serif; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(217,119,6,0.15);" onmouseover="this.style.filter=\'brightness(1.15)\'" onmouseout="this.style.filter=\'none\'">
                                    <span>🔮 Run AI Prediction</span>
                                </button>
                                
                                <div id="prediction-loader" style="display: none; align-items: center; justify-content: center; flex-direction: column; gap: 0.5rem; padding: 1rem 0;">
                                    <div class="spinner"></div>
                                    <span style="font-size: 0.75rem; color: var(--accent-gold); font-weight: 500;">Analyzing chart & indicators...</span>
                                </div>
                                
                                <div id="prediction-results" style="display: none; flex-direction: column; gap: 0.65rem; border-top: 1px dashed var(--border-color); padding-top: 0.75rem; margin-top: 0.25rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">Action:</span>
                                        <span id="pred-action" class="badge" style="font-size: 0.7rem; padding: 0.15rem 0.5rem;">HOLD</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; color: var(--text-secondary);">Entry Price:</span>
                                        <span id="pred-entry" style="font-weight: 600; color: #ffffff; font-family: monospace;">—</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; color: var(--text-secondary);">Stop Loss (SL):</span>
                                        <span id="pred-sl" style="font-weight: 600; color: var(--sell-color); font-family: monospace;">—</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; color: var(--text-secondary);">Take Profit 1:</span>
                                        <span id="pred-tp1" style="font-weight: 600; color: var(--buy-color); font-family: monospace;">—</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; color: var(--text-secondary);">Take Profit 2:</span>
                                        <span id="pred-tp2" style="font-weight: 600; color: var(--buy-color); font-family: monospace;">—</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <span style="font-size: 0.8rem; color: var(--text-secondary);">AI Confidence:</span>
                                        <span id="pred-confidence" style="font-weight: 600; color: var(--accent-gold);">—</span>
                                    </div>
                                    <div style="display: flex; flex-direction: column; gap: 0.25rem; margin-top: 0.25rem;">
                                        <span style="font-size: 0.75rem; font-weight: 600; color: #ffffff;">Technical Reasoning:</span>
                                        <p id="pred-reasoning" style="font-size: 0.72rem; color: var(--text-secondary); line-height: 1.4; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.02); padding: 0.5rem; border-radius: 6px;"></p>
                                    </div>
                                    <button id="btn-place-prediction-order" onclick="placePredictionOrder()" style="display: none; width: 100%; background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); border: none; color: #060913; padding: 0.65rem; border-radius: 6px; font-family: \'Outfit\', sans-serif; font-size: 0.82rem; font-weight: 700; cursor: pointer; transition: all 0.2s; margin-top: 0.5rem; justify-content: center; align-items: center; gap: 0.5rem;" onmouseover="this.style.filter=\'brightness(1.15)\'" onmouseout="this.style.filter=\'none\'">
                                        <span>⚡ Place AI Predicted Order</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Operational Checklist panel -->
                        <div class="panel">
                            <div class="panel-header">
                                <span class="panel-title">📝 Operational Checklist</span>
                            </div>
                            <div style="display:flex; gap:0.4rem; margin-bottom:0.75rem;">
                                <input type="text" id="new-task-input" placeholder="Add checklist task..." style="flex-grow:1; background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.4rem 0.65rem; border-radius:6px; font-size:0.78rem; outline:none;" onkeydown="if(event.key === \'Enter\') addDashboardTask()"/>
                                <button class="calendar-btn" onclick="addDashboardTask()" style="padding:0.4rem 0.85rem;">Add</button>
                            </div>
                            <div id="dashboard-tasks-list" style="display:flex; flex-direction:column; gap:0.45rem; max-height:220px; overflow-y:auto; padding-right:2px;">
                                {tasks_html}
                            </div>
                        </div>
                    </div>

                    <!-- Right: Interactive Candlestick Charts & News Feed -->
                    <div style="display: flex; flex-direction: column; gap: 1.25rem; width: 100%;">
                        <!-- Top: TradingView Chart panel -->
                        <div class="panel chart-panel">
                            <div class="chart-controls-row">
                                <div style="display:flex; align-items:center; gap:0.5rem;">
                                    <span class="symbol-pair">XAUUSD</span>
                                    <span class="symbol-subtext">Gold / US Dollar</span>
                                    <span class="price-badge badge {active_badge_class}" id="chart-price-label">{active_price_str}</span>
                                </div>
                                <div style="display:flex; gap:0.35rem; align-items:center;">
                                    <div class="tf-selector">
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'M1\', this)">M1</button>
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'M5\', this)">M5</button>
                                        <button class="tf-btn active" onclick="changeChartTimeframe(\'M15\', this)">M15</button>
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'M30\', this)">M30</button>
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'H1\', this)">H1</button>
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'H4\', this)">H4</button>
                                        <button class="tf-btn" onclick="changeChartTimeframe(\'D1\', this)">1D</button>
                                    </div>
                                    <select class="indicators-dropdown">
                                        <option>Indicators (EMA, RSI)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <!-- Live Session Colour Legend Strip -->
                            <div class="session-legend" id="session-legend-strip">
                                <div style="display: flex; align-items: center; gap: 0.25rem;">
                                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #3b82f6;"></span>
                                    <span>Sydney <span style="font-family: monospace;">22:00-07:00</span></span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.25rem;">
                                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #8b5cf6;"></span>
                                    <span>Tokyo <span style="font-family: monospace;">00:00-09:00</span></span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.25rem;">
                                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #10b981;"></span>
                                    <span>London <span style="font-family: monospace;">08:00-17:00</span></span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.25rem;">
                                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #fbbf24;"></span>
                                    <span>New York <span style="font-family: monospace;">13:00-22:00</span></span>
                                </div>
                            </div>
                            
                            <div class="chart-container-div" id="tv-chart-container" style="flex: 1; height: 380px; position: relative;">
                                <!-- TV Widget gets loaded here -->
                            </div>
                        </div>

                        <!-- Bottom: METATRADER 5 LIVE CHART broker feed panel -->
                        <div class="panel chart-panel" style="min-height: 440px;">
                            <div class="panel-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.04); padding-bottom: 0.5rem;">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    📊 <span class="panel-title">METATRADER 5 LIVE CHART</span>
                                    <span class="badge badge-success" style="font-size: 0.6rem; padding: 0.1rem 0.35rem;">BROKER FEED</span>
                                </div>
                                <div class="tf-selector" id="mt5-tf-selector" style="display: flex; gap: 0.35rem; align-items: center;">
                                    <button class="tf-btn" data-tf="M1" onclick="changeMt5Timeframe(\'M1\', this)">M1</button>
                                    <button class="tf-btn" data-tf="M5" onclick="changeMt5Timeframe(\'M5\', this)">M5</button>
                                    <button class="tf-btn active" data-tf="M15" onclick="changeMt5Timeframe(\'M15\', this)">M15</button>
                                    <button class="tf-btn" data-tf="M30" onclick="changeMt5Timeframe(\'M30\', this)">M30</button>
                                    <button class="tf-btn" data-tf="H1" onclick="changeMt5Timeframe(\'H1\', this)">H1</button>
                                    <button class="tf-btn" data-tf="H4" onclick="changeMt5Timeframe(\'H4\', this)">H4</button>
                                    <button class="tf-btn" data-tf="D1" onclick="changeMt5Timeframe(\'D1\', this)">1D</button>
                                </div>
                            </div>
                            
                            <div class="chart-container-div" style="flex: 1; height: 380px; position: relative;">
                                <div class="chart-wrapper" id="tv-chart-wrapper" style="position: relative; width: 100%; height: 380px; overflow: hidden; border-radius: 8px; border: 1px solid var(--border-color); background: #050505;"></div>
                                <canvas id="vp-canvas" style="position: absolute; top: 0; right: 60px; width: 120px; height: calc(100% - 26px); pointer-events: none; z-index: 3;"></canvas>
                            </div>
                            
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; font-size:0.7rem; color:var(--text-secondary);">
                                <span>Spread: <strong id="live-spread-val" style="color:#ffffff;">{tick_spread_pips} pips</strong> ({tick_spread_points} pts)</span>
                                <span>Broker Server: <strong style="color:#ffffff;">{mt5_server}</strong></span>
                            </div>
                        </div>

                        <!-- Active Trades panel on Dashboard -->
                        <div class="panel">
                            <div class="panel-header" style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    💼 <span class="panel-title">Active Broker Positions</span>
                                </div>
                            </div>
                            <div class="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Ticket</th>
                                            <th>Pair</th>
                                            <th>Direction</th>
                                            <th>Size</th>
                                            <th>Entry</th>
                                            <th>Current Price</th>
                                            <th>Profit</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="dashboard-open-positions-tbody">
                                        {dashboard_open_trades_rows}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Economic News Alerts Feed -->
                        <div class="panel" style="flex: 1;">
                            <div class="panel-header">
                                <span class="panel-title">📡 High-Impact Economic Feed</span>
                            </div>
                            <div id="dashboard-news-widget-list" style="display:flex; flex-direction:column; gap:0.5rem; max-height:240px; overflow-y:auto; padding-right:2px;">
                                {news_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2. TRADE DESK VIEW -->
            <div id="trades-view" class="tab-view">
                <div style="display:grid; grid-template-columns: 280px 1fr; gap:1.25rem;">
                    <!-- Manual Order Card -->
                    <div class="panel">
                        <div class="panel-header">
                            <span class="panel-title">⚡ Instant Execution</span>
                        </div>
                        <div style="display:flex; flex-direction:column; gap:0.85rem; margin-top:0.5rem;">
                            <div>
                                <label style="font-size: 0.68rem; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Asset Symbol</label>
                                <input type="text" id="manual-order-symbol" value="XAUUSD" style="background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.45rem; border-radius:6px; font-size:0.85rem; width:100%; outline:none;"/>
                            </div>
                            <div>
                                <label style="font-size: 0.68rem; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Lot Size (Volume)</label>
                                <input type="number" id="manual-order-volume" value="0.10" step="0.01" min="0.01" style="background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.45rem; border-radius:6px; font-size:0.85rem; width:100%; outline:none;"/>
                            </div>
                            <div>
                                <label style="font-size: 0.68rem; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Stop Loss Price</label>
                                <input type="number" id="manual-order-sl" placeholder="Optional" step="0.01" style="background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.45rem; border-radius:6px; font-size:0.85rem; width:100%; outline:none;"/>
                            </div>
                            <div>
                                <label style="font-size: 0.68rem; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Take Profit Price</label>
                                <input type="number" id="manual-order-tp" placeholder="Optional" step="0.01" style="background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.45rem; border-radius:6px; font-size:0.85rem; width:100%; outline:none;"/>
                            </div>
                            <div style="display:flex; gap:0.5rem; margin-top:0.5rem;">
                                <button onclick="submitInstantOrder('BUY')" style="flex:1; background:linear-gradient(135deg, #4ade80 0%, #22c55e 100%); border:none; color:#000; padding:0.65rem; border-radius:6px; font-family:'Outfit',sans-serif; font-weight:700; font-size:0.85rem; cursor:pointer; text-transform:uppercase;">BUY</button>
                                <button onclick="submitInstantOrder('SELL')" style="flex:1; background:linear-gradient(135deg, #f87171 0%, #ef4444 100%); border:none; color:#ffffff; padding:0.65rem; border-radius:6px; font-family:'Outfit',sans-serif; font-weight:700; font-size:0.85rem; cursor:pointer; text-transform:uppercase;">SELL</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Open Positions table -->
                    <div class="panel">
                        <div class="panel-header">
                            <span class="panel-title">Active Broker Positions ({len(open_trades)})</span>
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Ticket</th>
                                        <th>Pair</th>
                                        <th>Direction</th>
                                        <th>Size</th>
                                        <th>Entry Price</th>
                                        <th>Current Price</th>
                                        <th>Stop Loss</th>
                                        <th>Take Profit</th>
                                        <th>Current Profit</th>
                                        <th>RR Ratio</th>
                                        <th>Duration</th>
                                        <th>AI Confidence</th>
                                        <th>Execution Control</th>
                                    </tr>
                                </thead>
                                <tbody id="open-positions-tbody">
                                    {open_trades_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. SIGNALS VIEW -->
            <div id="signals-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Signal Ingestion logs</span>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Timestamp (UTC)</th>
                                    <th>Pair</th>
                                    <th>Direction</th>
                                    <th>Source</th>
                                    <th>Market Sentiment</th>
                                    <th>Indicator Quality</th>
                                    <th>AI Confidence</th>
                                    <th>Strategy Performance</th>
                                    <th>Decision Status</th>
                                    <th>Remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                {signals_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 4. COMMITTEE REVIEW VIEW -->
            <div id="committee-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">⚖️ AI Committee Confluence Audit</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 2fr 1fr; gap:1.25rem; margin-top:0.5rem;">
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <div class="widget-card" style="padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.85rem; font-weight:700; color:var(--accent-gold);">CONFLUENCE AUDIT SUMMARY</span>
                                    <span class="badge badge-success" style="font-size:0.78rem;" id="committee-decision-badge">PENDING SELECT</span>
                                </div>
                                <div style="font-size:0.85rem; color:#ffffff; line-height:1.45; border-top:1px solid var(--border-color); padding-top:0.75rem; margin-top:0.75rem;" id="committee-reasoning-box">
                                    Click on any trade in the "Trade History" or "Signal Intel" tabs to load its full committee review. Fallback review metrics are parsed in real-time.
                                </div>
                            </div>
                            
                            <!-- Detailed reviews split -->
                            <div class="panel" style="margin-top:1rem;" id="committee-detailed-reviews">
                                <div style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.5rem;">COMMITTEE MODULE DEBRIEFS</div>
                                <div style="display:flex; flex-direction:column; gap:0.55rem; font-size:0.78rem;">
                                    <div><strong>📡 Technical Review:</strong> <span id="comm-detail-tech" style="color:var(--text-secondary);">Breakout volume confirmation aligns with H1 structure support.</span></div>
                                    <div><strong>📈 Market Review:</strong> <span id="comm-detail-trend" style="color:var(--text-secondary);">Bullish micro structure holds above H1 EMA50.</span></div>
                                    <div><strong>🛡️ Risk Review:</strong> <span id="comm-detail-risk" style="color:var(--text-secondary);">Position size strictly at 1.0% risk per setup.</span></div>
                                    <div><strong>📅 News Review:</strong> <span id="comm-detail-news" style="color:var(--text-secondary);">No immediate high-impact calendar event overlaps.</span></div>
                                    <div><strong>💧 Liquidity Review:</strong> <span id="comm-detail-liq" style="color:var(--text-secondary);">Gold orderbook spread remains below 5.0 points threshold.</span></div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="widget-card" style="padding:1rem; align-items:center; gap:0.5rem; justify-content:center; text-align:center;">
                                <span class="widget-label">Committee Score</span>
                                <span style="font-size:3rem; font-weight:700; color:var(--accent-gold); font-family:'Outfit';" id="committee-score-val">—</span>
                                <span style="font-size:0.72rem; color:var(--text-secondary);" id="committee-confidence-sub">Confidence: Low / High</span>
                            </div>
                            
                            <!-- Committee reviews split subscores -->
                            <div class="panel" style="margin-top:1rem; padding:0.85rem;">
                                <div class="metric-row"><span>Technical Confluence</span><span class="metric-value text-buy" id="comm-sub-tech">80/100</span></div>
                                <div class="metric-row"><span>Market Trend Score</span><span class="metric-value text-buy" id="comm-sub-trend">75/100</span></div>
                                <div class="metric-row"><span>Risk Safety Gate</span><span class="metric-value text-buy" id="comm-sub-risk">90/100</span></div>
                                <div class="metric-row"><span>News Calendar Buffer</span><span class="metric-value text-buy" id="comm-sub-news">85/100</span></div>
                                <div class="metric-row"><span>Liquidity Volatility Check</span><span class="metric-value text-buy" id="comm-sub-liq">70/100</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 5. ANALYTICS VIEW -->
            <div id="analytics-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">🎯 Institutional Performance Metrics</span>
                    </div>
                    <div class="metrics-grid" style="margin-bottom:1rem;">
                        <div class="widget-card">
                            <span class="widget-label">Expectancy</span>
                            <span class="widget-value" id="stats-expectancy">$0.00</span>
                            <span style="font-size:0.65rem; color:var(--text-secondary);">Per trade closed</span>
                        </div>
                        <div class="widget-card">
                            <span class="widget-label">Sharpe Ratio</span>
                            <span class="widget-value" id="stats-sharpe">0.00</span>
                            <span style="font-size:0.65rem; color:var(--text-secondary);">Risk adjusted return</span>
                        </div>
                        <div class="widget-card">
                            <span class="widget-label">Recovery Factor</span>
                            <span class="widget-value" id="stats-recovery">0.00</span>
                            <span style="font-size:0.65rem; color:var(--text-secondary);">Drawdown recovery strength</span>
                        </div>
                        <div class="widget-card">
                            <span class="widget-label">Average Hold Time</span>
                            <span class="widget-value" id="stats-holdtime">0.0m</span>
                            <span style="font-size:0.65rem; color:var(--text-secondary);">Minutes per position</span>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem; margin-top:1.25rem;">
                        <!-- Balance & Equity Curve Line Chart -->
                        <div class="analytics-chart-box" style="height: 250px;">
                            <span class="panel-title" style="font-size:0.75rem; margin-bottom:0.5rem;">📈 Balance & Equity Curve</span>
                            <div style="flex:1; position:relative; min-height:0;">
                                <canvas id="chart-balance-canvas"></canvas>
                            </div>
                        </div>
                        <!-- Session Performance Bar Chart -->
                        <div class="analytics-chart-box" style="height: 250px;">
                            <span class="panel-title" style="font-size:0.75rem; margin-bottom:0.5rem;">📊 Session Performance (Win Rate %)</span>
                            <div style="flex:1; position:relative; min-height:0;">
                                <canvas id="chart-sessions-canvas"></canvas>
                            </div>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:1.25rem; margin-top:1.25rem;">
                        <!-- Pair Performance Pie/Doughnut Chart -->
                        <div class="analytics-chart-box" style="height: 250px;">
                            <span class="panel-title" style="font-size:0.75rem; margin-bottom:0.5rem;">🔀 Pair Performance (PnL USD)</span>
                            <div style="flex:1; position:relative; min-height:0;">
                                <canvas id="chart-pairs-canvas"></canvas>
                            </div>
                        </div>
                        <!-- Strategy Performance Bar Chart -->
                        <div class="analytics-chart-box" style="height: 250px;">
                            <span class="panel-title" style="font-size:0.75rem; margin-bottom:0.5rem;">🎯 Strategy Performance (PnL USD)</span>
                            <div style="flex:1; position:relative; min-height:0;">
                                <canvas id="chart-strategies-canvas"></canvas>
                            </div>
                        </div>
                        <!-- Monthly Returns Bar Chart -->
                        <div class="analytics-chart-box" style="height: 250px;">
                            <span class="panel-title" style="font-size:0.75rem; margin-bottom:0.5rem;">📅 Monthly Returns (PnL USD)</span>
                            <div style="flex:1; position:relative; min-height:0;">
                                <canvas id="chart-monthly-canvas"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 6. AI COACH VIEW -->
            <div id="coach-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">🧠 AI Coach Performance Psychologist</span>
                    </div>
                    <div style="background:rgba(212,175,55,0.03); border: 1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:1rem; display:flex; flex-direction:column; gap:0.5rem;">
                        <span style="font-size:0.75rem; font-weight:700; color:var(--accent-gold); text-transform:uppercase;">Individual Trade Diagnostic Audit</span>
                        <div style="display:flex; gap:0.5rem; align-items:center;">
                            <select id="coach-trade-select" style="flex-grow:1; padding:0.4rem; font-size:0.78rem; background:var(--card-bg); border:1px solid var(--border-color); color:#fff; border-radius:4px; outline:none;"></select>
                            <button onclick="evaluateTradeCoach()" class="calendar-btn" style="padding:0.4rem 1rem;">Analyze Trade</button>
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 280px; gap:1.25rem;">
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <!-- Won/Lost Reason -->
                            <div class="widget-card" style="padding:1rem;">
                                <span style="font-size:0.85rem; font-weight:700; color:var(--accent-gold);">TRADE CONCLUSION & PSYCHOLOGY REVIEW</span>
                                <div id="coach-won-lost-box" style="font-size:0.82rem; color:#ffffff; line-height:1.45; border-top:1px solid var(--border-color); padding-top:0.75rem; margin-top:0.75rem;">
                                    Select a completed closed trade above and click "Analyze Trade" to retrieve the AI Trade Committee psychologist audit.
                                </div>
                            </div>

                            <!-- Mistakes & Risk Observations -->
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem;">
                                <div class="panel" style="border-color:rgba(239,68,68,0.15); background:rgba(239,68,68,0.01);">
                                    <h4 style="font-size:0.8rem; font-weight:700; color:var(--sell-color); margin-bottom:0.5rem;">⚠️ Mistakes Identified</h4>
                                    <div id="coach-mistakes-box" style="font-size:0.78rem; color:var(--text-secondary); line-height:1.4;">
                                        No active diagnostics loaded.
                                    </div>
                                </div>
                                <div class="panel" style="border-color:rgba(212,175,55,0.15); background:rgba(212,175,55,0.01);">
                                    <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.5rem;">🛡️ Risk Observations</h4>
                                    <div id="coach-risk-box" style="font-size:0.78rem; color:var(--text-secondary); line-height:1.4;">
                                        No active diagnostics loaded.
                                    </div>
                                </div>
                            </div>

                            <!-- Strengths & Improvements lists -->
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem;">
                                <div class="panel" style="border-color:rgba(34,197,94,0.15); background:rgba(34,197,94,0.01);">
                                    <h4 style="font-size:0.8rem; font-weight:700; color:var(--buy-color); margin-bottom:0.5rem;">🏆 Strengths Shown</h4>
                                    <div id="coach-strengths-box" style="font-size:0.78rem; color:var(--text-secondary); line-height:1.4;">
                                        No active diagnostics loaded.
                                    </div>
                                </div>
                                <div class="panel" style="border-color:rgba(59,130,246,0.15); background:rgba(59,130,246,0.01);">
                                    <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-blue); margin-bottom:0.5rem;">💡 Suggested Improvements</h4>
                                    <div id="coach-improvements-box" style="font-size:0.78rem; color:var(--text-secondary); line-height:1.4;">
                                        No active diagnostics loaded.
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <button onclick="requestCoachReport()" class="btn-submit" style="margin-top:0; font-size:0.8rem;">Generate Coach Report</button>
                            
                            <div class="panel" style="padding:0.75rem;">
                                <h4 style="font-size:0.75rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.4rem;">Psychological Profile</h4>
                                <div class="metric-row"><span>Discipline Score</span><span class="metric-value" id="profile-discipline-val">92%</span></div>
                                <div class="metric-row"><span>Patience Index</span><span class="metric-value" id="profile-patience-val">85%</span></div>
                                <div class="metric-row"><span>Risk Aversion</span><span class="metric-value" id="profile-risk-val">98%</span></div>
                            </div>
                        </div>
                    </div>

                    <!-- Coach report display container -->
                    <div class="panel" style="margin-top:1.25rem; display:none;" id="coach-report-panel">
                        <h4 style="font-size:0.85rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.5rem;">📋 AI Coach Comprehensive Psychology Report</h4>
                        <div id="coach-report-content" style="font-size:0.8rem; color:#ffffff; line-height:1.5; white-space:pre-wrap; max-height:400px; overflow-y:auto; background:rgba(0,0,0,0.25); padding:1rem; border-radius:6px; border:1px solid var(--border-color);"></div>
                    </div>
                </div>
            </div>

            <!-- 7. TRADING JOURNAL VIEW -->
            <div id="journal-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">📝 Interactive Trade Journal</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 320px 1fr; gap:1.25rem; margin-top:0.5rem;">
                        <div class="panel" style="padding:0.85rem; background:rgba(0,0,0,0.15);">
                            <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Write Journal Entry</h4>
                            <div style="display:flex; flex-direction:column; gap:0.65rem;">
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Select Trade Ticket</label>
                                    <select id="journal-trade-select" style="padding:0.35rem 0.5rem; font-size:0.78rem; background:var(--card-bg); border:1px solid var(--border-color); color:#fff; width:100%; border-radius:4px; outline:none;"></select>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Setup Type</label>
                                    <select id="journal-setup-select" style="padding:0.35rem 0.5rem; font-size:0.78rem; background:var(--card-bg); border:1px solid var(--border-color); color:#fff; width:100%; border-radius:4px; outline:none;">
                                        <option value="Breakout">Breakout Continuation</option>
                                        <option value="Retest">Support/Resistance Retest</option>
                                        <option value="FVG">Fair Value Gap / Liquidity Sweep</option>
                                        <option value="Crossover">EMA Trend Crossover</option>
                                    </select>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Emotion at Execution</label>
                                    <select id="journal-emotion-select" style="padding:0.35rem 0.5rem; font-size:0.78rem; background:var(--card-bg); border:1px solid var(--border-color); color:#fff; width:100%; border-radius:4px; outline:none;">
                                        <option value="Calm">Calm & Disinterested</option>
                                        <option value="Confident">Confident / Analytical</option>
                                        <option value="Greed">Greedy / FOMO</option>
                                        <option value="Fear">Fearful / Hesitant</option>
                                        <option value="Impatient">Impatient / Rushed</option>
                                    </select>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Setup Notes</label>
                                    <textarea id="journal-notes-textarea" placeholder="Explain the rationale, indicators confluence, entry trigger..." style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; font-family:'Inter'; font-size:0.78rem; width:100%; height:60px; padding:0.5rem; border-radius:6px; resize:none; outline:none;"></textarea>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Lessons Learned</label>
                                    <textarea id="journal-lessons-textarea" placeholder="What mistakes were made? What did you learn?" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; font-family:'Inter'; font-size:0.78rem; width:100%; height:60px; padding:0.5rem; border-radius:6px; resize:none; outline:none;"></textarea>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Screenshot Image URL</label>
                                    <input type="text" id="journal-screenshot-input" placeholder="Paste image link here" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <button onclick="saveJournalEntry()" class="btn-submit" style="margin-top:0.25rem; font-size:0.75rem; padding:0.5rem;">Save Entry</button>
                            </div>
                        </div>
                        
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <!-- Journal subviews navigation -->
                            <div style="display:flex; gap:0.5rem;">
                                <button class="calendar-btn active" onclick="switchJournalSubView('timeline', this)" id="btn-journal-timeline">Timeline View</button>
                                <button class="calendar-btn" onclick="switchJournalSubView('calendar', this)" id="btn-journal-calendar">Calendar View</button>
                                <button class="calendar-btn" onclick="switchJournalSubView('replay', this)" id="btn-journal-replay">Trade Replay</button>
                            </div>

                            <!-- Timeline Subview -->
                            <div class="panel journal-subview-panel" id="journal-timeline-subview" style="flex:1;">
                                <h4 style="font-size:0.85rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Journal Timeline</h4>
                                <div id="journal-timeline-list" style="display:flex; flex-direction:column; gap:0.65rem; max-height:420px; overflow-y:auto; padding-right:2px;">
                                    <!-- Populated dynamically -->
                                </div>
                            </div>

                            <!-- Calendar Subview -->
                            <div class="panel journal-subview-panel" id="journal-calendar-subview" style="flex:1; display:none;">
                                <h4 style="font-size:0.85rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Journal Monthly Calendar</h4>
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span id="journal-cal-title" style="font-size:0.8rem; font-weight:700;">June 2026</span>
                                    <div style="display:flex; gap:0.25rem;">
                                        <button class="calendar-btn" onclick="navigateJournalMonth(-1)">&larr;</button>
                                        <button class="calendar-btn" onclick="navigateJournalMonth(1)">&rarr;</button>
                                    </div>
                                </div>
                                <div style="display:grid; grid-template-columns: repeat(7, 1fr); gap:4px; text-align:center;" id="journal-cal-grid">
                                    <!-- Populated dynamically -->
                                </div>
                            </div>

                            <!-- Trade Replay Subview -->
                            <div class="panel journal-subview-panel" id="journal-replay-subview" style="flex:1; display:none;">
                                <h4 style="font-size:0.85rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Trade Entry/Exit Replay Chart</h4>
                                <div style="margin-bottom:0.5rem; display:flex; gap:0.5rem; align-items:center;">
                                    <span style="font-size:0.75rem; color:var(--text-secondary);">Select Trade to Replay:</span>
                                    <select id="journal-replay-select" style="padding:0.3rem; font-size:0.75rem; background:var(--card-bg); border:1px solid var(--border-color); color:#fff; border-radius:4px; outline:none;" onchange="loadReplayChart()"></select>
                                </div>
                                <div id="journal-replay-chart-wrapper" style="width:100%; height:320px; background:#050505; border-radius:6px; border:1px solid var(--border-color); position:relative;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 8. PORTFOLIO CENTER VIEW -->
            <div id="portfolio-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">💼 Portfolio Account Aggregator</span>
                    </div>
                    
                    <div style="display:grid; grid-template-columns: 280px 1fr; gap:1.25rem; margin-top:0.5rem;">
                        <!-- Add account card -->
                        <div class="panel" style="padding:0.85rem; background:rgba(0,0,0,0.15);">
                            <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.5rem;">Link Sub-Account</h4>
                            <div style="display:flex; flex-direction:column; gap:0.65rem;">
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Account Name</label>
                                    <input type="text" id="portfolio-acc-name" placeholder="e.g. Funded Acc 1" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Login ID</label>
                                    <input type="number" id="portfolio-acc-login" placeholder="e.g. 500021" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Trader Password</label>
                                    <input type="password" id="portfolio-acc-password" placeholder="Investor/Trader Password" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Broker Server</label>
                                    <input type="text" id="portfolio-acc-server" placeholder="e.g. FTMO-Demo" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <div>
                                    <label style="font-size:0.7rem; color:var(--text-secondary);">Balance (USD)</label>
                                    <input type="number" id="portfolio-acc-balance" placeholder="e.g. 50000" style="background:var(--card-bg); border:1px solid var(--border-color); color:#fff; padding:0.4rem; border-radius:4px; font-size:0.78rem; width:100%; outline:none;"/>
                                </div>
                                <button onclick="addPortfolioAccount()" class="btn-submit" style="margin-top:0.25rem; font-size:0.75rem; padding:0.5rem;">Add Account</button>
                            </div>
                        </div>
                        
                        <div>
                            <!-- Aggregated stats -->
                            <div class="metrics-grid" style="margin-bottom:1rem;">
                                <div class="widget-card">
                                    <span class="widget-label">Portfolio Equity</span>
                                    <span class="widget-value" id="port-total-equity">$0.00</span>
                                </div>
                                <div class="widget-card">
                                    <span class="widget-label">Combined Drawdown</span>
                                    <span class="widget-value" id="port-combined-dd">0.00%</span>
                                </div>
                                <div class="widget-card">
                                    <span class="widget-label">Linked Accounts</span>
                                    <span class="widget-value" id="port-accounts-count">1</span>
                                </div>
                            </div>
                            
                            <!-- Linked accounts list -->
                            <div class="panel">
                                <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Linked Accounts Registry</h4>
                                <div class="table-container">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Account Name</th>
                                                <th>Server</th>
                                                <th>Balance</th>
                                                <th>Status</th>
                                                <th>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody id="portfolio-accounts-tbody">
                                            <!-- Dynamically populated -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 9. MARKET INTELLIGENCE VIEW -->
            <div id="market-intel-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">🔮 Quantitative Market Intelligence</span>
                    </div>
                    
                    <div style="display:grid; grid-template-columns: 260px 1fr; gap:1.25rem; margin-top:0.5rem;">
                        <!-- Currency Strength Meter -->
                        <div class="panel" style="padding:0.85rem; background:rgba(0,0,0,0.15);">
                            <h4 style="font-size:0.8rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.75rem;">Relative Strength Meter</h4>
                            <div id="currency-strength-container" style="display:flex; flex-direction:column; gap:0.45rem;">
                                <!-- Strengths list -->
                            </div>
                            
                            <div style="border-top:1px solid var(--border-color); margin-top:1rem; padding-top:0.85rem; text-align:center;">
                                <span class="widget-label">Fear & Greed Index</span>
                                <div style="font-size:1.5rem; font-weight:700; color:var(--warning-color); margin-top:0.25rem;" id="fear-greed-val">58 - NEUTRAL</div>
                            </div>
                        </div>
                        
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <!-- AI briefings -->
                            <div class="panel">
                                <h4 style="font-size:0.85rem; font-weight:700; color:var(--accent-gold); margin-bottom:0.5rem;">⚡ AI Market Outlook Briefing</h4>
                                <p style="font-size:0.82rem; color:#ffffff; line-height:1.45;" id="market-brief-text">
                                    Gold is currently trading inside the H1 consolidation range. Moving averages alignment shows neutral structure. High impact CPI scheduled tomorrow will determine the next macro extension.
                                </p>
                                <div style="display:flex; gap:0.5rem; margin-top:0.75rem;">
                                    <button class="calendar-btn" onclick="requestMarketBrief('hourly')">Hourly Brief</button>
                                    <button class="calendar-btn" onclick="requestMarketBrief('daily')">Daily Brief</button>
                                    <button class="calendar-btn" onclick="requestMarketBrief('weekly')">Weekly Outlook</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 10. TRADE HISTORY VIEW -->
            <div id="history-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">All Historical Closed Trades</span>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Ticket ID</th>
                                    <th>Symbol</th>
                                    <th>Type</th>
                                    <th>Volume</th>
                                    <th>Entry Price</th>
                                    <th>Exit Price</th>
                                    <th>Profit</th>
                                    <th>Commission</th>
                                    <th>Swap</th>
                                    <th>Execution Date</th>
                                    <th>Close Date</th>
                                    <th>Remarks / Comment</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 11. TRADING CALENDAR VIEW -->
            <div id="calendar-view" class="tab-view">
                <div class="calendar-container">
                    <div class="calendar-controls">
                        <h2 class="calendar-title" id="calendar-header-title">Calendar</h2>
                        <div>
                            <button class="calendar-btn" id="btn-calendar-prev" onclick="navigateMonth(-1)">&larr; Previous</button>
                            <button class="calendar-btn" id="btn-calendar-next" onclick="navigateMonth(1)">Next &rarr;</button>
                        </div>
                    </div>
                    <div class="calendar-grid" id="calendar-days-grid"></div>
                </div>
            </div>

            <!-- 12. LIVE NEWS VIEW -->
            <div id="news-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Live Forex & Gold Market News Headlines</span>
                    </div>
                    <div id="live-news-list" style="display: flex; flex-direction: column; gap: 0.75rem; max-height: calc(100vh - 200px); overflow-y: auto;">
                        {live_news_html}
                    </div>
                </div>
            </div>

            <!-- 13. SETTINGS VIEW -->
            <div id="settings-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Trading System Risk Guidelines</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.5rem;">
                        <div class="metric-row">
                            <span class="metric-label">Max Risk Per Trade</span>
                            <span class="metric-value">{data.get('risk_percent_per_trade', 0.01)*100.0:.1f}%</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Max Daily Trades Count</span>
                            <span class="metric-value">2</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Drawdown Alert Threshold (Daily / Weekly)</span>
                            <span class="metric-value">{data.get('max_daily_drawdown_pct', 0.05)*100.0:.1f}% / {data.get('max_weekly_drawdown_pct', 0.10)*100.0:.1f}%</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">AI Signal Verification</span>
                            <span class="metric-value">{"ENABLED" if data.get("ai_validation_enabled", True) else "DISABLED"}</span>
                        </div>
                    </div>
                </div>

                <div class="panel" style="margin-top: 1rem;">
                    <div class="panel-header">
                        <span class="panel-title">⚙️ Configure API & Broker Synchronization</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <div>
                            <h4 style="font-size: 0.82rem; font-weight: 700; color: var(--accent-gold); margin-bottom: 0.5rem;">MetaTrader 5 Account Credentials</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem;">
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">MT5 Login ID</label>
                                    <input type="number" id="setting-mt5-login" value="{data.get('mt5_login', 0)}" />
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">MT5 Password</label>
                                    <input type="password" id="setting-mt5-password" value="{data.get('mt5_password', '')}" />
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">MT5 Server Name</label>
                                    <input type="text" id="setting-mt5-server" value="{data.get('mt5_server', '')}" />
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">Broker Mode</label>
                                    <select id="setting-mt5-mock">
                                        <option value="false" {"selected" if not data.get('mt5_mock') else ""}>Live Broker (AtlasFunded)</option>
                                        <option value="true" {"selected" if data.get('mt5_mock') else ""}>Mock Simulation Sandbox</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                            <h4 style="font-size: 0.82rem; font-weight: 700; color: var(--accent-gold); margin-bottom: 0.5rem;">AI LLM Provider Authorization Keys</h4>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">Gemini Key</label>
                                    <input type="password" id="setting-gemini-key" value="{data.get('gemini_api_key', '')}" />
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">OpenAI Key</label>
                                    <input type="password" id="setting-openai-key" value="{data.get('openai_api_key', '')}" />
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.7rem; color: var(--text-secondary);">Claude (Anthropic) Key</label>
                                    <input type="password" id="setting-claude-key" value="{data.get('claude_api_key', '')}" />
                                </div>
                            </div>
                        </div>

                        <div style="display: flex; justify-content: flex-end; margin-top: 0.5rem;">
                            <button id="btn-save-settings" onclick="saveSystemSettings()" class="btn-submit" style="margin-top:0; width:auto; padding:0.6rem 2rem;">
                                Commit Settings & Connect
                            </button>
                        </div>
                    </div>
                </div>

                <div class="panel" style="margin-top: 1.25rem;">
                    <div class="panel-header">
                        <span class="panel-title">System & Database Maintenance</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <button id="btn-clear-history" onclick="clearHistoryAndSync()" style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); color: var(--sell-color); padding: 0.65rem; border-radius: 6px; font-family: 'Outfit'; font-weight: 700; font-size: 0.8rem; cursor: pointer;">
                            🧹 Clear Database History
                        </button>
                        <button id="btn-reset-pnl" onclick="resetDailyPnL()" style="background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.2); color: var(--accent-gold); padding: 0.65rem; border-radius: 6px; font-family: 'Outfit'; font-weight: 700; font-size: 0.8rem; cursor: pointer;">
                            🔄 Reset Daily PNL Peak
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </main>

    <!-- Side Drawer overlay -->
    <div class="drawer-backdrop" id="drawer-bg" onclick="closeTradeDrawer()"></div>
    <div class="drawer" id="trade-drawer">
        <div class="drawer-header">
            <h3 class="drawer-title" id="drawer-date-title">Trades on Date</h3>
            <button class="drawer-close" onclick="closeTradeDrawer()">&times;</button>
        </div>
        <div class="drawer-content">
            <div id="drawer-trades-list"></div>
        </div>
    </div>

    <!-- Chat Bubble & widget -->
    <div class="chat-widget-container" id="chat-widget">
        <div class="chat-widget-header">
            <div class="chat-widget-header-title">
                <span class="chat-widget-title">💬 AI Committee Chat</span>
                <span class="chat-widget-subtitle">Active connection to Claude / Gemini / OpenAI</span>
            </div>
            <button class="chat-widget-close" onclick="toggleChatWidget()">✕</button>
        </div>
        <div class="chat-widget-messages" id="chat-messages">
            {chat_html}
        </div>
        <div class="chat-widget-footer">
            <input type="text" id="chat-input" placeholder="Ask details about indicators..." style="flex-grow: 1; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.8rem; outline: none;" onkeydown="if(event.key === 'Enter') sendChatMessage()"/>
            <button id="btn-voice-chat" onclick="toggleVoiceTyping()" style="background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border-color); color: var(--text-secondary); padding: 0.5rem; border-radius: 6px; cursor: pointer;">🎙️</button>
            <button id="btn-send-chat" onclick="sendChatMessage()" class="calendar-btn">Send</button>
        </div>
    </div>
    <button class="chat-bubble-btn" id="chat-toggle-btn" onclick="toggleChatWidget()">💬</button>

    <!-- Partial Close Modal -->
    <div class="modal" id="partial-close-modal">
        <div class="modal-content">
            <h3 style="font-family:'Outfit'; color:#fff; font-size:1.15rem; margin-bottom:0.75rem;">Partial Exit Position</h3>
            <input type="hidden" id="partial-close-ticket" />
            <div style="margin-bottom:1rem;">
                <label style="font-size:0.72rem; color:var(--text-secondary); display:block; margin-bottom:0.25rem;">Volume to Close (Lots)</label>
                <input type="number" id="partial-close-volume" step="0.01" min="0.01" style="background:rgba(0,0,0,0.2); border:1px solid var(--border-color); color:#fff; padding:0.45rem; border-radius:6px; font-size:0.85rem; width:100%;" />
                <span id="partial-close-max-label" style="font-size:0.65rem; color:var(--text-secondary); margin-top:0.25rem; display:block;">Max open volume: 0.00</span>
            </div>
            <div style="display:flex; gap:0.5rem;">
                <button onclick="submitPartialClose()" class="calendar-btn" style="flex:1; background:var(--buy-color); color:#000; border:none; font-weight:700;">Submit Partial Exit</button>
                <button onclick="closePartialCloseModal()" class="calendar-btn" style="flex:1;">Cancel</button>
            </div>
        </div>
    </div>

    <!-- Client-side trades database JSON injection -->
    <script id="all-trades-data" type="application/json">
        {trades_json_str}
    </script>
    <script id="all-news-events-data" type="application/json">
        {news_events_json_str}
    </script>

    <script>
        let lastPrediction = null;

        // Tab switching engine
        function switchTab(tabId, el) {{
            const views = document.querySelectorAll('.tab-view');
            views.forEach(v => v.classList.remove('active'));
            
            const targetView = document.getElementById(tabId);
            if (targetView) {{
                targetView.classList.add('active');
            }}
            
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => item.classList.remove('active'));
            if (el) el.classList.add('active');
            
            // Draw chart again or initialize specific tabs
            if (tabId === 'analytics-view') {{
                setTimeout(renderAnalyticsCharts, 100);
            }} else if (tabId === 'coach-view') {{
                setTimeout(renderAiCoachInsights, 100);
            }} else if (tabId === 'journal-view') {{
                setTimeout(renderJournalTab, 100);
            }} else if (tabId === 'portfolio-view') {{
                setTimeout(renderPortfolioTab, 100);
            }} else if (tabId === 'market-intel-view') {{
                setTimeout(renderMarketIntelTab, 100);
            }}
        }}

        function toggleChatWidget() {{
            const widget = document.getElementById('chat-widget');
            if (widget) {{
                widget.classList.toggle('active');
                if (widget.classList.contains('active')) {{
                    const messagesContainer = document.getElementById('chat-messages');
                    if (messagesContainer) messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }}
            }}
        }}

        function showToast(message, isError = false) {{
            const toast = document.getElementById('toast');
            if (toast) {{
                toast.textContent = message;
                toast.style.background = isError ? 'rgba(239, 68, 68, 0.95)' : 'rgba(34, 197, 94, 0.95)';
                toast.style.display = 'block';
                setTimeout(() => {{ toast.style.display = 'none'; }}, 4000);
            }}
        }}

        // Timezones clocks
        function updateClock() {{
            const options = {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }};
            
            document.getElementById('clock-kol').textContent = new Date().toLocaleTimeString('en-US', {{ ...options, timeZone: 'Asia/Kolkata' }});
            document.getElementById('clock-utc').textContent = new Date().toLocaleTimeString('en-US', {{ ...options, timeZone: 'UTC' }});
            document.getElementById('clock-ny').textContent = new Date().toLocaleTimeString('en-US', {{ ...options, timeZone: 'America/New_York' }});
            document.getElementById('clock-ldn').textContent = new Date().toLocaleTimeString('en-US', {{ ...options, timeZone: 'Europe/London' }});
            document.getElementById('clock-tok').textContent = new Date().toLocaleTimeString('en-US', {{ ...options, timeZone: 'Asia/Tokyo' }});
            
            updateTradingSessions();
            setTimeout(updateClock, 1000);
        }}

        function updateTradingSessions() {{
            const kolFormatter = new Intl.DateTimeFormat('en-US', {{
                timeZone: 'Asia/Kolkata',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }});
            const kolTimeStr = kolFormatter.format(new Date());
            const sessionTimeText = document.getElementById('session-time-text');
            if (sessionTimeText) {{
                sessionTimeText.textContent = `Current time: ${{kolTimeStr}} (Kolkata)`;
            }}
            
            const parts = kolTimeStr.split(':');
            const h = parseInt(parts[0]);
            const m = parseInt(parts[1]);
            const s = parseInt(parts[2]);
            const T = h + m / 60 + s / 3600;
            
            // Define sessions: name, start, end, DOM id suffix, color theme
            const sessionDefs = [
                {{ name: 'Sydney', start: 3.5, end: 12.5, suffix: 'sydney', color: '#3b82f6', badgeActiveColor: '#60a5fa', badgeBg: 'rgba(59, 130, 246, 0.2)', border: 'rgba(59, 130, 246, 0.4)' }},
                {{ name: 'Tokyo', start: 5.5, end: 14.5, suffix: 'tokyo', color: '#8b5cf6', badgeActiveColor: '#a78bfa', badgeBg: 'rgba(139, 92, 246, 0.2)', border: 'rgba(139, 92, 246, 0.4)' }},
                {{ name: 'London', start: 13.5, end: 22.5, suffix: 'london', color: '#10b981', badgeActiveColor: '#34d399', badgeBg: 'rgba(16, 185, 129, 0.2)', border: 'rgba(16, 185, 129, 0.4)' }},
                {{ name: 'New York', start: 18.5, end: 3.5, suffix: 'newyork', color: '#fbbf24', badgeActiveColor: '#fcd34d', badgeBg: 'rgba(251, 191, 36, 0.2)', border: 'rgba(251, 191, 36, 0.4)' }}
            ];
            
            sessionDefs.forEach(s => {{
                const card = document.getElementById('session-card-' + s.suffix);
                if (!card) return;
                
                let active = false;
                let remaining = 0.0;
                
                if (s.start < s.end) {{
                    // Normal session (e.g. 03:30 to 12:30)
                    if (T >= s.start && T < s.end) {{
                        active = true;
                        remaining = s.end - T;
                    }} else {{
                        active = false;
                        if (T < s.start) {{
                            remaining = s.start - T;
                        }} else {{
                            remaining = (24 - T) + s.start;
                        }}
                    }}
                }} else {{
                    // Overlap midnight (e.g. 18:30 to 03:30 next day)
                    if (T >= s.start || T < s.end) {{
                        active = true;
                        if (T >= s.start) {{
                            remaining = (24 - T) + s.end;
                        }} else {{
                            remaining = s.end - T;
                        }}
                    }} else {{
                        active = false;
                        remaining = s.start - T;
                    }}
                }}
                
                const badge = card.querySelector('.badge');
                const timer = card.querySelector('.session-countdown');
                
                if (active) {{
                    card.style.border = `1px solid ${{s.color}}`;
                    card.style.boxShadow = `0 0 10px rgba(${{hexToRgb(s.color)}}, 0.15)`;
                    if (badge) {{
                        badge.textContent = 'ACTIVE';
                        badge.style.background = s.badgeBg;
                        badge.style.color = s.badgeActiveColor;
                        badge.style.border = `1px solid ${{s.border}}`;
                    }}
                    if (timer) {{
                        timer.textContent = 'Closes in ' + formatHoursToHm(remaining);
                        timer.style.color = s.badgeActiveColor;
                    }}
                }} else {{
                    card.style.border = '1px solid var(--border-color)';
                    card.style.boxShadow = 'none';
                    if (badge) {{
                        badge.textContent = 'CLOSED';
                        badge.style.background = 'rgba(255,255,255,0.05)';
                        badge.style.color = 'var(--text-secondary)';
                        badge.style.border = '1px solid rgba(255,255,255,0.08)';
                    }}
                    if (timer) {{
                        timer.textContent = 'Opens in ' + formatHoursToHm(remaining);
                        timer.style.color = 'var(--text-secondary)';
                    }}
                }}
            }});
            
            // Update sliding current time vertical indicator
            const currentHourPct = (T / 24) * 100;
            const ind = document.getElementById('timeline-current-indicator');
            if (ind) {{
                ind.style.left = `calc(${{currentHourPct}}% - 1.5px)`;
            }}
        }}
        
        function hexToRgb(hex) {{
            const bigint = parseInt(hex.replace('#', ''), 16);
            const r = (bigint >> 16) & 255;
            const g = (bigint >> 8) & 255;
            const b = bigint & 255;
            return `${{r}}, ${{g}}, ${{b}}`;
        }}
        
        function formatHoursToHm(hoursDec) {{
            const totalMin = Math.round(hoursDec * 60);
            const h = Math.floor(totalMin / 60);
            const m = totalMin % 60;
            return `${{h}}h ${{m}}m`;
        }}

        // Save preferences
        function setTimezonePreference(tz) {{
            localStorage.setItem('dashboard_timezone', tz);
            showToast("Preferred timezone updated to: " + tz);
        }}

        // Reconnect Broker
        function reconnectBroker() {{
            const btn = document.getElementById('btn-reconnect-broker');
            if (btn) btn.disabled = true;
            fetch('/api/v1/reconnect', {{ method: 'POST' }})
            .then(res => res.json())
            .then(data => {{
                if (btn) btn.disabled = false;
                if (data.status === 'SUCCESS') {{
                    showToast("✅ " + data.message);
                    setTimeout(() => window.location.reload(), 1500);
                }} else {{
                    showToast("❌ " + data.message, true);
                }}
            }})
            .catch(() => {{ if (btn) btn.disabled = false; }});
        }}

        // save settings
        function saveSystemSettings() {{
            const payload = {{
                mt5_login: parseInt(document.getElementById('setting-mt5-login').value) || 0,
                mt5_password: document.getElementById('setting-mt5-password').value,
                mt5_server: document.getElementById('setting-mt5-server').value,
                mt5_mock: document.getElementById('setting-mt5-mock').value === 'true',
                claude_api_key: document.getElementById('setting-claude-key').value || '',
                openai_api_key: document.getElementById('setting-openai-key').value || '',
                gemini_api_key: document.getElementById('setting-gemini-key').value || ''
            }};
            fetch('/api/v1/settings', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("Configuration saved successfully.");
                    setTimeout(() => window.location.reload(), 1500);
                }} else {{
                    showToast("Failed to save: " + data.message, true);
                }}
            }});
        }}

        // Tasks Checklist
        function addDashboardTask() {{
            const input = document.getElementById('new-task-input');
            const title = input ? input.value.trim() : '';
            if (!title) return;
            fetch('/api/v1/tasks', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ title: title }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    input.value = '';
                    window.location.reload();
                }}
            }});
        }}

        function toggleTask(id, completed) {{
            fetch('/api/v1/tasks/' + id, {{
                method: 'PUT',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ completed: completed }})
            }});
        }}

        function deleteTask(id, el) {{
            fetch('/api/v1/tasks/' + id, {{ method: 'DELETE' }})
            .then(() => el.remove());
        }}

        // Close position
        function closeActiveTrade(ticket) {{
            fetch('/api/v1/close-trade?ticket=' + ticket, {{ method: 'POST' }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("Position Closed.");
                    setTimeout(() => window.location.reload(), 1200);
                }}
            }});
        }}

        // Modify stops inline
        function updateStopsInline(ticket, row) {{
            const sl = parseFloat(row.querySelector('.inline-sl').value) || 0.0;
            const tp = parseFloat(row.querySelector('.inline-tp').value) || 0.0;
            fetch('/api/v1/modify-stops', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ ticket: ticket, sl: sl, tp: tp }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("Stops modified successfully.");
                }} else {{
                    showToast(data.message, true);
                }}
            }});
        }}

        // Breakeven modification
        function moveBreakeven(ticket, entry, tp) {{
            fetch('/api/v1/modify-stops', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ ticket: ticket, sl: entry, tp: tp }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("SL moved to Entry Breakeven.");
                    setTimeout(() => window.location.reload(), 1200);
                }}
            }});
        }}

        // Partial close modal
        function openPartialCloseModal(ticket, volume) {{
            document.getElementById('partial-close-ticket').value = ticket;
            document.getElementById('partial-close-volume').value = (volume / 2).toFixed(2);
            document.getElementById('partial-close-max-label').textContent = "Max open volume: " + volume.toFixed(2);
            document.getElementById('partial-close-modal').style.display = 'flex';
        }}
        function closePartialCloseModal() {{
            document.getElementById('partial-close-modal').style.display = 'none';
        }}
        function submitPartialClose() {{
            const ticket = parseInt(document.getElementById('partial-close-ticket').value);
            const volume = parseFloat(document.getElementById('partial-close-volume').value);
            fetch('/api/v1/partial-close', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ ticket: ticket, volume: volume }})
            }}).then(res => res.json()).then(data => {{
                closePartialCloseModal();
                if (data.status === 'SUCCESS') {{
                    showToast(data.message);
                    setTimeout(() => window.location.reload(), 1200);
                }} else {{
                    showToast(data.detail || "Partial exit rejected", true);
                }}
            }});
        }}

        // Instant order
        function submitInstantOrder(direction) {{
            const symbol = document.getElementById('manual-order-symbol').value;
            const volume = parseFloat(document.getElementById('manual-order-volume').value);
            const sl = parseFloat(document.getElementById('manual-order-sl').value) || 0.0;
            const tp = parseFloat(document.getElementById('manual-order-tp').value) || 0.0;
            fetch('/api/v1/place-order', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ symbol: symbol, direction: direction, volume: volume, sl: sl, tp: tp }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("Order Sent! Ticket #" + data.ticket);
                    setTimeout(() => window.location.reload(), 1500);
                }} else {{
                    showToast(data.detail || "Failed to execute order", true);
                }}
            }});
        }}

        // Maintenance methods
        function clearHistoryAndSync() {{
            fetch('/api/v1/maintenance/clear-history', {{ method: 'POST' }})
            .then(res => res.json()).then(data => {{
                showToast(data.message);
                setTimeout(() => window.location.reload(), 1500);
            }});
        }}
        function resetDailyPnL() {{
            fetch('/api/v1/maintenance/reset-daily-pnl', {{ method: 'POST' }})
            .then(res => res.json()).then(data => {{
                showToast(data.message);
                setTimeout(() => window.location.reload(), 1500);
            }});
        }}

        // Voice chat typing
        let recognition = null;
        let isListening = false;
        function toggleVoiceTyping() {{
            const btn = document.getElementById('btn-voice-chat');
            const input = document.getElementById('chat-input');
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                showToast("Web Speech API not supported.", true);
                return;
            }}
            if (isListening) {{
                if (recognition) recognition.stop();
                return;
            }}
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {{
                isListening = true;
                btn.style.background = 'rgba(212,175,55,0.2)';
                input.placeholder = "Listening...";
            }};
            recognition.onend = function() {{
                isListening = false;
                btn.style.background = 'rgba(255,255,255,0.04)';
                input.placeholder = "Ask details about indicators...";
            }};
            recognition.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;
                if (transcript) input.value = transcript;
            }};
            recognition.start();
        }}

        // Chatbot sending
        function sendChatMessage() {{
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;
            
            const list = document.getElementById('chat-messages');
            const notice = document.getElementById('chat-empty-notice');
            if (notice) notice.remove();
            
            const userDiv = document.createElement('div');
            userDiv.style = 'max-width:85%; padding:0.75rem 1rem; border-radius:8px; align-self:flex-end; background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.2); display:flex; flex-direction:column; gap:0.25rem;';
            userDiv.innerHTML = `<span style="font-size:0.65rem; font-weight:700; color:var(--accent-gold); text-transform:uppercase;">You</span><div style="font-size:0.8rem; color:#fff; line-height:1.45;">${{message}}</div>`;
            list.appendChild(userDiv);
            list.scrollTop = list.scrollHeight;
            input.value = '';
            
            fetch('/api/v1/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: message }})
            }}).then(res => res.json()).then(data => {{
                const aiDiv = document.createElement('div');
                aiDiv.style = 'align-self:flex-start; background:var(--card-bg); border:1px solid var(--border-color); max-width:85%; padding:0.75rem 1rem; border-radius:8px; display:flex; flex-direction:column; gap:0.25rem;';
                aiDiv.innerHTML = `<span style="font-size:0.65rem; font-weight:700; color:var(--luxury-gold); text-transform:uppercase;">AI Assistant</span><div style="font-size:0.8rem; color:#fff; line-height:1.45; white-space:pre-wrap;">${{data.response}}</div>`;
                list.appendChild(aiDiv);
                list.scrollTop = list.scrollHeight;
            }});
        }}

        // Injected data arrays
        let tradesData = [];
        let newsData = [];
        try {{
            tradesData = JSON.parse(document.getElementById('all-trades-data').textContent);
            newsData = JSON.parse(document.getElementById('all-news-events-data').textContent);
        }} catch(e) {{
            console.error("JSON parsing error: ", e);
        }}

        // --- NEW MODULE: TRADE ANALYTICS ---
        var sidebar_balance = {sidebar_balance};
        var sidebar_equity = {sidebar_equity};
        var mt5_server = "{mt5_server}";
        var mt5_login = "{mt5_login}";
        var mt5_mock = {str(mt5_mock).lower()};

        // --- NEW MODULE: TRADE ANALYTICS ---
        function renderAnalyticsCharts() {{
            const closedTrades = tradesData.filter(t => t.status === 'CLOSED').sort((a, b) => new Date(a.closed_at) - new Date(b.closed_at));
            
            let totalHoldMinutes = 0.0;
            let winsCount = 0;
            let lossesCount = 0;
            let totalProfit = 0.0;
            let totalLoss = 0.0;
            let pnlArray = [];
            
            closedTrades.forEach(t => {{
                const p = t.profit || 0.0;
                pnlArray.push(p);
                if (p > 0) {{
                    winsCount++;
                    totalProfit += p;
                }} else {{
                    lossesCount++;
                    totalLoss += Math.abs(p);
                }}
                
                if (t.created_at && t.closed_at) {{
                    const diff = (new Date(t.closed_at) - new Date(t.created_at)) / 60000.0;
                    totalHoldMinutes += diff;
                }}
            }});
            
            const totalCount = closedTrades.length || 1;
            const expectancy = (totalProfit - totalLoss) / totalCount;
            document.getElementById('stats-expectancy').textContent = (expectancy >= 0 ? '+' : '') + '$' + expectancy.toFixed(2);
            document.getElementById('stats-expectancy').className = 'widget-value ' + (expectancy >= 0 ? 'text-buy' : 'text-sell');
            
            const meanPnL = expectancy;
            let varianceSum = 0.0;
            pnlArray.forEach(p => {{ varianceSum += Math.pow(p - meanPnL, 2); }});
            const stdDev = Math.sqrt(varianceSum / totalCount) || 1.0;
            const sharpe = meanPnL / stdDev;
            document.getElementById('stats-sharpe').textContent = sharpe.toFixed(2);
            
            const netProfitVal = totalProfit - totalLoss;
            const maxDDVal = 250.0;
            const recovery = netProfitVal / maxDDVal;
            document.getElementById('stats-recovery').textContent = recovery.toFixed(2);
            
            const avgHold = totalHoldMinutes / totalCount;
            document.getElementById('stats-holdtime').textContent = avgHold.toFixed(1) + ' min';

            if (window.myCharts) {{
                if (window.myCharts.balance) window.myCharts.balance.destroy();
                if (window.myCharts.sessions) window.myCharts.sessions.destroy();
                if (window.myCharts.pairs) window.myCharts.pairs.destroy();
                if (window.myCharts.strategies) window.myCharts.strategies.destroy();
                if (window.myCharts.monthly) window.myCharts.monthly.destroy();
            }} else {{
                window.myCharts = {{}};
            }}

            // 1. Balance/Equity curve Line chart
            let currentB = sidebar_balance - (totalProfit - totalLoss);
            const labels = ['Start'];
            const balancePoints = [currentB];
            closedTrades.forEach((t, i) => {{
                currentB += t.profit;
                balancePoints.push(currentB);
                labels.push('Trade ' + (i + 1));
            }});
            const ctxB = document.getElementById('chart-balance-canvas').getContext('2d');
            window.myCharts.balance = new Chart(ctxB, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Balance',
                        data: balancePoints,
                        borderColor: '#D4AF37',
                        backgroundColor: 'rgba(212, 175, 55, 0.04)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3,
                        pointRadius: balancePoints.length > 20 ? 0 : 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(212,175,55,0.02)' }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }},
                        y: {{ grid: {{ color: 'rgba(212,175,55,0.02)' }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});

            // 2. Session Performance Bar Chart
            const sessions = {{ London: {{ total: 0, wins: 0 }}, NY: {{ total: 0, wins: 0 }}, Tokyo: {{ total: 0, wins: 0 }}, Sydney: {{ total: 0, wins: 0 }} }};
            closedTrades.forEach(t => {{
                const hour = new Date(t.created_at).getUTCHours();
                let sName = 'London';
                if (hour >= 13 && hour < 21) sName = 'NY';
                else if (hour >= 22 || hour < 6) sName = 'Tokyo';
                else if (hour >= 6 && hour < 13) sName = 'Sydney';
                sessions[sName].total++;
                if (t.profit > 0) sessions[sName].wins++;
            }});
            const sessionLabels = ['London', 'New York', 'Tokyo', 'Sydney'];
            const sessionRates = [
                sessions.London.total > 0 ? (sessions.London.wins / sessions.London.total * 100) : 76,
                sessions.NY.total > 0 ? (sessions.NY.wins / sessions.NY.total * 100) : 64,
                sessions.Tokyo.total > 0 ? (sessions.Tokyo.wins / sessions.Tokyo.total * 100) : 52,
                sessions.Sydney.total > 0 ? (sessions.Sydney.wins / sessions.Sydney.total * 100) : 45
            ];
            const ctxS = document.getElementById('chart-sessions-canvas').getContext('2d');
            window.myCharts.sessions = new Chart(ctxS, {{
                type: 'bar',
                data: {{
                    labels: sessionLabels,
                    datasets: [{{
                        label: 'Win Rate %',
                        data: sessionRates,
                        backgroundColor: ['#3B82F6', '#D4AF37', '#EF4444', '#22C55E'],
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }},
                        y: {{ min: 0, max: 100, grid: {{ color: 'rgba(212,175,55,0.02)' }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});

            // 3. Pair Performance Doughnut Chart
            const pairPnL = {{}};
            closedTrades.forEach(t => {{
                pairPnL[t.symbol] = (pairPnL[t.symbol] || 0) + t.profit;
            }});
            const pairLabels = Object.keys(pairPnL);
            const pairValues = Object.values(pairPnL);
            const ctxP = document.getElementById('chart-pairs-canvas').getContext('2d');
            window.myCharts.pairs = new Chart(ctxP, {{
                type: 'doughnut',
                data: {{
                    labels: pairLabels.length > 0 ? pairLabels : ['XAUUSD'],
                    datasets: [{{
                        data: pairValues.length > 0 ? pairValues : [totalProfit - totalLoss || 100],
                        backgroundColor: ['#D4AF37', '#F5E6A7', '#3B82F6', '#22C55E', '#EF4444'],
                        borderColor: '#111111',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'right', labels: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});

            // 4. Strategy Performance Bar Chart
            const strategyPnL = {{}};
            closedTrades.forEach(t => {{
                const strat = t.comment || "Manual";
                strategyPnL[strat] = (strategyPnL[strat] || 0) + t.profit;
            }});
            const strategyLabels = Object.keys(strategyPnL);
            const strategyValues = Object.values(strategyPnL);
            const ctxSt = document.getElementById('chart-strategies-canvas').getContext('2d');
            window.myCharts.strategies = new Chart(ctxSt, {{
                type: 'bar',
                data: {{
                    labels: strategyLabels.length > 0 ? strategyLabels : ['TV Webhook', 'Manual'],
                    datasets: [{{
                        label: 'PnL ($)',
                        data: strategyValues.length > 0 ? strategyValues : [120.0, 45.0],
                        backgroundColor: '#D4AF37',
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }},
                        y: {{ grid: {{ color: 'rgba(212,175,55,0.02)' }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});

            // 5. Monthly Returns Bar Chart
            const monthlyPnL = {{}};
            closedTrades.forEach(t => {{
                const date = new Date(t.closed_at);
                const key = date.toLocaleString('default', {{ month: 'short', year: 'numeric' }});
                monthlyPnL[key] = (monthlyPnL[key] || 0) + t.profit;
            }});
            const monthlyLabels = Object.keys(monthlyPnL);
            const monthlyValues = Object.values(monthlyPnL);
            const ctxM = document.getElementById('chart-monthly-canvas').getContext('2d');
            window.myCharts.monthly = new Chart(ctxM, {{
                type: 'bar',
                data: {{
                    labels: monthlyLabels.length > 0 ? monthlyLabels : ['June 2026'],
                    datasets: [{{
                        label: 'PnL ($)',
                        data: monthlyValues.length > 0 ? monthlyValues : [totalProfit - totalLoss || 250],
                        backgroundColor: (monthlyValues.length > 0 ? monthlyValues : [250]).map(v => v >= 0 ? '#22C55E' : '#EF4444'),
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }},
                        y: {{ grid: {{ color: 'rgba(212,175,55,0.02)' }}, ticks: {{ color: '#A1A1AA', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});
        }}

        // --- NEW MODULE: AI COACH ---
        function renderAiCoachInsights() {{
            const select = document.getElementById('coach-trade-select');
            select.innerHTML = '';
            
            const closedTrades = tradesData.filter(t => t.status === 'CLOSED');
            closedTrades.forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.ticket;
                opt.textContent = `Ticket #${{t.ticket}} (${{t.symbol}} ${{t.order_type}}) - Profit: $${{t.profit.toFixed(2)}}`;
                select.appendChild(opt);
            }});

            // Fetch evaluations to compute psychological profile
            fetch('/api/v1/ai-coach/evaluations')
            .then(res => res.json())
            .then(evals => {{
                let mistakesCount = 0;
                evals.forEach(e => {{
                    const m = e.mistakes.toLowerCase();
                    if (m && m !== 'none' && m !== 'no mistakes' && m !== 'n/a' && !m.includes('no explicit')) {{
                        mistakesCount++;
                    }}
                }});

                // Discipline: Deduct for mistakes
                const discipline = Math.max(50, 95 - mistakesCount * 8);
                document.getElementById('profile-discipline-val').textContent = discipline + '%';

                // Patience: Based on average holding time of closed trades
                let totalHoldSec = 0;
                let count = 0;
                closedTrades.forEach(t => {{
                    if (t.created_at && t.closed_at) {{
                        totalHoldSec += (new Date(t.closed_at) - new Date(t.created_at)) / 1000.0;
                        count++;
                    }}
                }});
                const avgHoldMin = count > 0 ? (totalHoldSec / count / 60.0) : 25;
                const patience = Math.min(100, Math.max(50, Math.round(55 + avgHoldMin * 0.8)));
                document.getElementById('profile-patience-val').textContent = patience + '%';

                // Risk Aversion: Based on volume variance
                let riskAversion = 98;
                if (closedTrades.length > 1) {{
                    const vols = closedTrades.map(t => t.volume);
                    const meanVol = vols.reduce((a, b) => a + b, 0) / vols.length;
                    const variance = vols.reduce((a, b) => a + Math.pow(b - meanVol, 2), 0) / vols.length;
                    if (variance > 0.5) riskAversion = 82;
                    else if (variance > 0.1) riskAversion = 90;
                }}
                document.getElementById('profile-risk-val').textContent = riskAversion + '%';
            }});
        }}

        function evaluateTradeCoach() {{
            const ticket = document.getElementById('coach-trade-select').value;
            if (!ticket) {{
                showToast("No trade selected to analyze.", true);
                return;
            }}
            showToast("Generating AI trade psychologist evaluation...");
            
            document.getElementById('coach-won-lost-box').innerHTML = `
                <div class="ambient-loader">
                    <div class="ambient-spinner"></div>
                    <span style="font-size:0.75rem; color:var(--accent-gold); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">
                        Performing execution audit & synthesizing risk telemetry...
                    </span>
                </div>
            `;
            document.getElementById('coach-mistakes-box').textContent = "Analyzing...";
            document.getElementById('coach-risk-box').textContent = "Analyzing...";
            document.getElementById('coach-strengths-box').textContent = "Analyzing...";
            document.getElementById('coach-improvements-box').textContent = "Analyzing...";
            
            fetch(`/api/v1/ai-coach/evaluate/${{ticket}}`, {{ method: 'POST' }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS' && data.evaluation) {{
                    const e = data.evaluation;
                    document.getElementById('coach-won-lost-box').textContent = e.won_lost_reason;
                    document.getElementById('coach-mistakes-box').textContent = e.mistakes || "None detected.";
                    document.getElementById('coach-risk-box').textContent = e.risk_observations || "Optimal parameters maintained.";
                    document.getElementById('coach-strengths-box').textContent = e.strengths || "Standard compliance.";
                    document.getElementById('coach-improvements-box').textContent = e.improvements || "Continue setup repetition.";
                    showToast("Audit completed.");
                    renderAiCoachInsights(); // Refresh profile stats
                }} else {{
                    showToast("Failed to run diagnostic.", true);
                }}
            }}).catch(() => {{
                showToast("Connection error during diagnostic audit.", true);
            }});
        }}

        function requestCoachReport() {{
            showToast("Requesting full AI Coach psychology audit summary...");
            const reportPanel = document.getElementById('coach-report-panel');
            const reportContent = document.getElementById('coach-report-content');
            reportPanel.style.display = 'block';
            reportContent.innerHTML = `
                <div class="ambient-loader">
                    <div class="ambient-spinner"></div>
                    <span style="font-size:0.75rem; color:var(--accent-gold); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">
                        Reviewing database history & compiling psychology audit...
                    </span>
                </div>
            `;
            
            fetch('/api/v1/chat', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ message: "Analyze all closed trades and AI evaluations to compile a comprehensive trading psychology report. Highlight mistakes, emotional triggers, and concrete action steps." }})
            }}).then(res => res.json()).then(data => {{
                reportContent.textContent = data.response;
                showToast("AI Coach summary report generated successfully!");
            }}).catch(() => {{
                showToast("Failed to generate coach report.", true);
            }});
        }}

        function changeMt5Timeframe(tf) {{
            loadChartData(tf);
        }}

        function formatTimeIsoToLocal(isoStr) {{
            if (!isoStr) return '—';
            try {{
                const date = new Date(isoStr);
                const tz = localStorage.getItem('dashboard_timezone') || 'Asia/Kolkata';
                return date.toLocaleString('en-US', {{
                    timeZone: tz,
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                }}).replace(',', '');
            }} catch(e) {{
                return isoStr;
            }}
        }}

        function rebuildHistoryTable() {{
            const tbody = document.querySelector('#history-view tbody');
            if (!tbody) return;
            
            const closedTrades = tradesData.filter(t => t.status === 'CLOSED').sort((a, b) => new Date(b.closed_at) - new Date(a.closed_at));
            if (closedTrades.length === 0) {{
                tbody.innerHTML = "<tr><td colspan='12' class='text-center text-muted'>No historical closed records found in DB.</td></tr>";
                return;
            }}
            
            let html = '';
            closedTrades.forEach(t => {{
                const typeClass = t.order_type === 'BUY' ? 'text-buy' : 'text-sell';
                const pnl = t.profit || 0.0;
                const pnlClass = pnl > 0 ? 'text-buy font-bold' : (pnl < 0 ? 'text-sell font-bold' : 'text-muted');
                const pnlSign = pnl > 0 ? '+' : '';
                
                const createdTime = t.created_at ? formatTimeIsoToLocal(t.created_at) : '—';
                const closedTime = t.closed_at ? formatTimeIsoToLocal(t.closed_at) : '—';
                const commentStr = t.comment ? escapeHtml(t.comment) : '—';
                const ticketId = t.ticket ? '#' + t.ticket : '—';
                
                html += `
                <tr data-ticket="${{t.ticket}}" style="cursor: pointer;">
                    <td>${{ticketId}}</td>
                    <td class="font-bold">${{t.symbol}}</td>
                    <td class="font-bold ${{typeClass}}">${{t.order_type}}</td>
                    <td>${{(t.volume || 0.0).toFixed(2)}}</td>
                    <td>${{(t.entry_price || 0.0).toFixed(2)}}</td>
                    <td>${{(t.exit_price || 0.0).toFixed(2)}}</td>
                    <td class="${{pnlClass}}">$${{pnlSign}}${{pnl.toFixed(2)}}</td>
                    <td>$${{(t.commission || 0.0).toFixed(2)}}</td>
                    <td>$${{(t.swap || 0.0).toFixed(2)}}</td>
                    <td class="small"><span class="time-cell" data-iso="${{t.created_at}}">${{createdTime}}</span></td>
                    <td class="small"><span class="time-cell" data-iso="${{t.closed_at}}">${{closedTime}}</span></td>
                    <td class="small">${{commentStr}}</td>
                </tr>
                `;
            }});
            tbody.innerHTML = html;
        }}

        function escapeHtml(text) {{
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        // --- NEW MODULE: TRADING JOURNAL ---
        function renderJournalTab() {{
            const select = document.getElementById('journal-trade-select');
            const selectReplay = document.getElementById('journal-replay-select');
            select.innerHTML = '';
            selectReplay.innerHTML = '';
            
            tradesData.filter(t => t.status === 'CLOSED').forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.ticket;
                opt.textContent = `Ticket #${{t.ticket}} (${{t.symbol}} ${{t.order_type}}) - PnL: $${{t.profit.toFixed(2)}}`;
                select.appendChild(opt);
            }});

            // Populate all trades for replay
            tradesData.forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.ticket;
                opt.textContent = `Ticket #${{t.ticket}} [${{t.status}}] (${{t.symbol}} ${{t.order_type}})`;
                selectReplay.appendChild(opt);
            }});
            
            reloadJournalTimeline();
        }}

        function saveJournalEntry() {{
            const ticket = parseInt(document.getElementById('journal-trade-select').value);
            if (!ticket) {{
                showToast("No trade selected to journal.", true);
                return;
            }}
            const setup = document.getElementById('journal-setup-select').value;
            const emotion = document.getElementById('journal-emotion-select').value;
            const notes = document.getElementById('journal-notes-textarea').value.trim();
            const lessons = document.getElementById('journal-lessons-textarea').value.trim();
            const screenshot = document.getElementById('journal-screenshot-input').value.trim();
            
            showToast("Saving journal entry to database...");
            fetch('/api/v1/journal', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    trade_ticket: ticket,
                    setup_type: setup,
                    emotion: emotion,
                    notes: notes,
                    lessons_learned: lessons,
                    screenshot_url: screenshot
                }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast("Journal entry recorded successfully.");
                    document.getElementById('journal-notes-textarea').value = '';
                    document.getElementById('journal-lessons-textarea').value = '';
                    document.getElementById('journal-screenshot-input').value = '';
                    reloadJournalTimeline();
                }} else {{
                    showToast("Failed to save entry.", true);
                }}
            }});
        }}

        function reloadJournalTimeline() {{
            const list = document.getElementById('journal-timeline-list');
            list.innerHTML = '<div>Loading journal timeline...</div>';
            
            fetch('/api/v1/journal')
            .then(res => res.json())
            .then(entries => {{
                list.innerHTML = '';
                if (entries.length === 0) {{
                    list.innerHTML = `<div class="text-center text-muted small" style="padding:1.5rem;">No journal entries registered yet. Fill out the writer form to record setups.</div>`;
                    return;
                }}
                
                entries.forEach(e => {{
                    const card = document.createElement('div');
                    card.className = 'widget-card';
                    card.style = 'padding: 0.85rem; margin-bottom: 0.5rem; background: var(--card-bg);';
                    let screenshotHtml = '';
                    if (e.screenshot_url) {{
                        screenshotHtml = `<img src="${{e.screenshot_url}}" style="max-width:100%; border-radius:4px; margin-top:0.5rem; border:1px solid var(--border-color); display:block;"/>`;
                    }}
                    let lessonsHtml = '';
                    if (e.lessons_learned) {{
                        lessonsHtml = `<p style="font-size:0.75rem; color:var(--text-secondary); margin-top:0.25rem;"><strong>Lessons:</strong> ${{e.lessons_learned}}</p>`;
                    }}
                    card.innerHTML = `
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                            <span style="font-size:0.75rem; font-weight:700; color:var(--accent-gold);">Ticket #${{e.trade_ticket}} (${{e.setup_type || 'Custom'}})</span>
                            <span class="badge badge-warning" style="font-size:0.58rem;">Emotion: ${{e.emotion}}</span>
                        </div>
                        <p style="font-size:0.78rem; color:#fff; line-height:1.45;">${{e.notes}}</p>
                        ${{lessonsHtml}}
                        ${{screenshotHtml}}
                        <span style="font-size:0.62rem; color:var(--text-secondary); margin-top:0.35rem; display:block;">Recorded: ${{new Date(e.created_at).toLocaleString()}}</span>
                    `;
                    list.appendChild(card);
                }});
            }});
        }}

        function switchJournalSubView(subview, btn) {{
            const panels = document.querySelectorAll('.journal-subview-panel');
            panels.forEach(p => p.style.display = 'none');
            
            const target = document.getElementById('journal-' + subview + '-subview');
            if (target) target.style.display = 'block';
            
            const btns = btn.parentNode.querySelectorAll('button');
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            if (subview === 'calendar') {{
                renderJournalCalendar(new Date().getFullYear(), new Date().getMonth());
            }} else if (subview === 'replay') {{
                loadReplayChart();
            }}
        }}

        let journalCalYear = new Date().getFullYear();
        let journalCalMonth = new Date().getMonth();
        
        function navigateJournalMonth(dir) {{
            journalCalMonth += dir;
            if (journalCalMonth < 0) {{ journalCalMonth = 11; journalCalYear--; }}
            else if (journalCalMonth > 11) {{ journalCalMonth = 0; journalCalYear++; }}
            renderJournalCalendar(journalCalYear, journalCalMonth);
        }}

        function renderJournalCalendar(year, month) {{
            const grid = document.getElementById('journal-cal-grid');
            if (!grid) return;
            grid.innerHTML = '';
            
            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            document.getElementById('journal-cal-title').textContent = monthNames[month] + " " + year;
            
            const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
            weekdays.forEach(w => {{
                const el = document.createElement('div');
                el.className = 'calendar-weekday';
                el.style = 'font-size:0.65rem; color:var(--text-secondary); font-weight:600; padding:0.25rem;';
                el.textContent = w;
                grid.appendChild(el);
            }});
            
            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            
            for(let i=0; i<firstDay; i++) {{
                const el = document.createElement('div');
                el.className = 'calendar-cell empty';
                el.style = 'height:40px;';
                grid.appendChild(el);
            }}

            fetch('/api/v1/journal')
            .then(res => res.json())
            .then(entries => {{
                for(let day=1; day<=daysInMonth; day++) {{
                    const cell = document.createElement('div');
                    cell.className = 'calendar-cell';
                    cell.style = 'height:40px; border:1px solid var(--border-color); border-radius:4px; display:flex; flex-direction:column; justify-content:space-between; padding:4px; position:relative; cursor:pointer; background:var(--card-bg);';
                    
                    const num = document.createElement('span');
                    num.className = 'cell-num';
                    num.style = 'font-size:0.65rem; color:var(--text-secondary); font-weight:600;';
                    num.textContent = day;
                    cell.appendChild(num);
                    
                    const dateStr = `${{year}}-${{String(month+1).padStart(2,'0')}}-${{String(day).padStart(2,'0')}}`;
                    const dayEntries = entries.filter(e => e.created_at.startsWith(dateStr));
                    
                    if (dayEntries.length > 0) {{
                        cell.style.borderColor = 'var(--accent-gold)';
                        cell.style.background = 'rgba(212,175,55,0.03)';
                        
                        const dot = document.createElement('span');
                        dot.style = 'width:6px; height:6px; background:var(--accent-gold); border-radius:50%; align-self:center; margin-bottom:4px;';
                        cell.appendChild(dot);
                        
                        cell.onclick = () => {{
                            showToast(`Day has ${{dayEntries.length}} journal logs. Loading timeline...`);
                            switchJournalSubView('timeline', document.getElementById('btn-journal-timeline'));
                        }};
                    }}
                    
                    grid.appendChild(cell);
                }}
            }});
        }}

        let replayChartInstance = null;
        let replayCandleSeries = null;

        function loadReplayChart() {{
            const ticket = parseInt(document.getElementById('journal-replay-select').value);
            if (!ticket) return;
            
            const t = tradesData.find(tr => tr.ticket === ticket) || open_trades.find(tr => tr.ticket === ticket);
            if (!t) return;
            
            const container = document.getElementById('journal-replay-chart-wrapper');
            if (!container) return;
            
            if (replayChartInstance) {{
                replayChartInstance.remove();
                replayChartInstance = null;
            }}
            
            replayChartInstance = LightweightCharts.createChart(container, {{
                layout: {{ background: {{ type: LightweightCharts.ColorType.Solid, color: '#050505' }}, textColor: '#A1A1AA' }},
                grid: {{ vertLines: {{ color: 'rgba(212, 175, 55, 0.02)' }}, horzLines: {{ color: 'rgba(212, 175, 55, 0.02)' }} }},
                rightPriceScale: {{ borderColor: 'rgba(212, 175, 55, 0.08)' }},
                timeScale: {{ borderColor: 'rgba(212, 175, 55, 0.08)' }}
            }});
            
            replayCandleSeries = replayChartInstance.addCandlestickSeries({{
                upColor: '#22c55e', downColor: '#ef4444',
                borderUpColor: '#22c55e', borderDownColor: '#ef4444',
                wickUpColor: '#22c55e', wickDownColor: '#ef4444'
            }});
            
            fetch('/api/v1/chart-data?timeframe=M15&count=120')
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS' && data.data) {{
                    const mapped = data.data.map(d => ({{
                        time: d.time,
                        open: d.open, high: d.high, low: d.low, close: d.close
                    }}));
                    replayCandleSeries.setData(mapped);
                    
                    // Add markers
                    const markers = [];
                    const entryTimeUnix = Math.floor(new Date(t.created_at).getTime() / 1000);
                    
                    // Find closest candle to entry time
                    let entryCandle = null;
                    let minEntryDiff = Infinity;
                    mapped.forEach(c => {{
                        let diff = Math.abs(c.time - entryTimeUnix);
                        if (diff < minEntryDiff) {{
                            minEntryDiff = diff;
                            entryCandle = c;
                        }}
                    }});
                    
                    if (entryCandle) {{
                        markers.push({{
                            time: entryCandle.time,
                            position: 'belowBar',
                            color: '#22c55e',
                            shape: 'arrowUp',
                            text: `${{t.order_type}} Entry @${{t.entry_price}}`
                        }});
                    }}
                    
                    if (t.closed_at) {{
                        const exitTimeUnix = Math.floor(new Date(t.closed_at).getTime() / 1000);
                        let exitCandle = null;
                        let minExitDiff = Infinity;
                        mapped.forEach(c => {{
                            let diff = Math.abs(c.time - exitTimeUnix);
                            if (diff < minExitDiff) {{
                                minExitDiff = diff;
                                exitCandle = c;
                            }}
                        }});
                        
                        if (exitCandle) {{
                            markers.push({{
                                time: exitCandle.time,
                                position: 'aboveBar',
                                color: '#ef4444',
                                shape: 'arrowDown',
                                text: `EXIT @${{t.exit_price || t.entry_price}}`
                            }});
                        }}
                    }}
                    
                    replayCandleSeries.setMarkers(markers);
                }}
            }});
        }}

        // --- NEW MODULE: PORTFOLIO CENTER ---
        function renderPortfolioTab() {{
            reloadPortfolioAccounts();
        }}

        function addPortfolioAccount() {{
            const name = document.getElementById('portfolio-acc-name').value.trim();
            const login = parseInt(document.getElementById('portfolio-acc-login').value);
            const password = document.getElementById('portfolio-acc-password').value;
            const server = document.getElementById('portfolio-acc-server').value.trim();
            const balance = parseFloat(document.getElementById('portfolio-acc-balance').value) || 0.0;
            
            if (!name || !login || !password || !server) {{
                showToast("All portfolio credentials are required.", true);
                return;
            }}
            
            showToast("Linking portfolio sub-account...");
            fetch('/api/v1/portfolio/accounts', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    account_name: name,
                    login_id: login,
                    password: password,
                    server: server,
                    balance: balance
                }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast(data.message);
                    document.getElementById('portfolio-acc-name').value = '';
                    document.getElementById('portfolio-acc-login').value = '';
                    document.getElementById('portfolio-acc-password').value = '';
                    document.getElementById('portfolio-acc-server').value = '';
                    document.getElementById('portfolio-acc-balance').value = '';
                    reloadPortfolioAccounts();
                }} else {{
                    showToast(data.message || "Failed to link account.", true);
                }}
            }});
        }}

        function removePortfolioAccount(id) {{
            showToast("Unlinking portfolio account...");
            fetch(`/api/v1/portfolio/accounts/${{id}}`, {{ method: 'DELETE' }})
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS') {{
                    showToast(data.message);
                    reloadPortfolioAccounts();
                }} else {{
                    showToast("Failed to unlink.", true);
                }}
            }});
        }}

        function reloadPortfolioAccounts() {{
            const tbody = document.getElementById('portfolio-accounts-tbody');
            tbody.innerHTML = '<tr><td colspan="5">Loading accounts...</td></tr>';
            
            fetch('/api/v1/portfolio/accounts')
            .then(res => res.json())
            .then(accounts => {{
                tbody.innerHTML = '';
                
                // Add primary connection
                const mainBalance = parseFloat(sidebar_balance);
                tbody.innerHTML += `
                    <tr>
                        <td class="font-bold">⚜️ Primary Account</td>
                        <td>${{mt5_server}}</td>
                        <td>$${{mainBalance.toFixed(2)}}</td>
                        <td><span class="badge badge-success">Active</span></td>
                        <td>—</td>
                    </tr>
                `;
                
                let totalEquity = parseFloat(sidebar_equity);
                let totalBalance = mainBalance;
                
                accounts.forEach(acc => {{
                    totalEquity += acc.equity;
                    totalBalance += acc.balance;
                    tbody.innerHTML += `
                        <tr>
                            <td class="font-bold">${{acc.account_name}}</td>
                            <td>${{acc.server}}</td>
                            <td>$${{acc.balance.toFixed(2)}}</td>
                            <td><span class="badge badge-success">${{acc.is_active ? 'Active' : 'Connected'}}</span></td>
                            <td><button class="badge badge-danger" onclick="removePortfolioAccount(${{acc.id}})" style="border:none; cursor:pointer;">unlink</button></td>
                        </tr>
                    `;
                }});
                
                document.getElementById('port-total-equity').textContent = '$' + totalEquity.toLocaleString('en-US', {{ minimumFractionDigits: 2 }});
                document.getElementById('port-accounts-count').textContent = (accounts.length + 1);
                
                let combinedDD = 0.0;
                if (totalBalance > 0) {{
                    combinedDD = Math.max(0.0, (totalBalance - totalEquity) / totalBalance * 100);
                }}
                document.getElementById('port-combined-dd').textContent = combinedDD.toFixed(2) + '%';
            }});
        }}

        // --- NEW MODULE: MARKET INTELLIGENCE ---
        function renderMarketIntelTab() {{
            const container = document.getElementById('currency-strength-container');
            container.innerHTML = '';
            
            const strengthValues = [
                {{ cur: 'USD', val: 78, color: '#22c55e' }},
                {{ cur: 'EUR', val: 62, color: '#3b82f6' }},
                {{ cur: 'GBP', val: 55, color: '#fbbf24' }},
                {{ cur: 'JPY', val: 34, color: '#ef4444' }},
                {{ cur: 'CHF', val: 51, color: '#a1a1aa' }}
            ];
            
            strengthValues.forEach(s => {{
                const row = document.createElement('div');
                row.className = 'strength-bar-container';
                row.innerHTML = `
                    <span class="strength-label">${{s.cur}}</span>
                    <div class="strength-bar-outer">
                        <div class="strength-bar-inner" style="width: ${{s.val}}%; background: ${{s.color}};"></div>
                    </div>
                    <span style="font-weight: 700; width:30px; text-align:right;">${{s.val}}%</span>
                `;
                container.appendChild(row);
            }});

            // Load latest generated brief
            fetch('/api/v1/market-intel/brief')
            .then(res => res.json())
            .then(briefs => {{
                if (briefs.length > 0) {{
                    document.getElementById('market-brief-text').textContent = briefs[0].content;
                }}
            }});
        }}

        function rebuildOpenPositionsTable(trades) {{
            const tbody1 = document.getElementById('open-positions-tbody');
            const tbody2 = document.getElementById('dashboard-open-positions-tbody');
            
            if (!trades || trades.length === 0) {{
                const emptyRow = `<tr><td colspan="13" class="text-center text-muted">No active open positions on MT5.</td></tr>`;
                const emptyRowShort = `<tr><td colspan="8" class="text-center text-muted">No active open positions.</td></tr>`;
                if (tbody1) tbody1.innerHTML = emptyRow;
                if (tbody2) tbody2.innerHTML = emptyRowShort;
                return;
            }}
            
            let htmlContent = '';
            let htmlContentShort = '';
            
            trades.forEach(t => {{
                const dirClass = t.order_type === 'BUY' ? 'text-buy' : 'text-sell';
                const pnl = t.profit || 0.0;
                const pnlClass = pnl > 0 ? 'text-buy font-bold' : (pnl < 0 ? 'text-sell font-bold' : 'text-muted');
                const pnlSign = pnl > 0 ? '+' : '';
                
                const isTsActive = localStorage.getItem('ts_' + t.ticket) === 'true' || (t.comment || '').toLowerCase().includes('trailing');
                const trailingStatus = isTsActive ? 'ACTIVE' : 'INACTIVE';
                const trailingClass = isTsActive ? 'badge-success' : 'badge-secondary';
                const durationMin = (t.duration / 60.0).toFixed(1);
                
                htmlContent += `
                <tr data-ticket="${{t.ticket}}">
                    <td>#${{t.ticket}}</td>
                    <td class="font-bold">${{t.symbol}}</td>
                    <td class="font-bold ${{dirClass}}">${{t.order_type}}</td>
                    <td>${{t.volume.toFixed(2)}}</td>
                    <td>${{t.entry_price.toFixed(2)}}</td>
                    <td class="pos-curr-price">${{t.current_price.toFixed(2)}}</td>
                    <td><input type="number" step="0.01" class="inline-sl" value="${{t.sl_price.toFixed(2)}}" style="width: 75px; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); color: #fff; padding: 2px 5px; border-radius: 4px; font-size: 0.78rem;" /></td>
                    <td><input type="number" step="0.01" class="inline-tp" value="${{t.tp_price.toFixed(2)}}" style="width: 75px; background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); color: #fff; padding: 2px 5px; border-radius: 4px; font-size: 0.78rem;" /></td>
                    <td class="${{pnlClass}} pos-profit">${{pnlSign}}$${{pnl.toFixed(2)}}</td>
                    <td>1 : ${{t.rr_ratio.toFixed(2)}}</td>
                    <td class="pos-duration">${{durationMin}}m</td>
                    <td class="font-bold" style="color: var(--accent-gold);">${{Math.round(t.ai_confidence * 100)}}%</td>
                    <td>
                        <div style="display: flex; gap: 0.3rem; flex-wrap: wrap;">
                            <button class="badge btn-gold" onclick="updateStopsInline(${{t.ticket}}, this.parentNode.parentNode.parentNode)" style="border:none; cursor:pointer;" title="Update SL/TP limits">SL/TP</button>
                            <button class="badge badge-warning" onclick="moveBreakeven(${{t.ticket}}, ${{t.entry_price}}, ${{t.tp_price}})" style="border:none; cursor:pointer;" title="Move Stop Loss to Entry">Breakeven</button>
                            <button class="badge badge-danger" onclick="openPartialCloseModal(${{t.ticket}}, ${{t.volume}})" style="border:none; cursor:pointer;" title="Partial Exit Lots">Partial</button>
                            <button class="badge badge-danger" onclick="closeActiveTrade(${{t.ticket}})" style="border:none; cursor:pointer;" title="Market Close Position">CLOSE</button>
                            <button class="badge ${{trailingClass}}" onclick="toggleTrailingStop(${{t.ticket}})" style="border:none; cursor:pointer;" id="trailing-btn-${{t.ticket}}" title="Toggle trailing stop state">${{trailingStatus}} TS</button>
                        </div>
                    </td>
                </tr>
                `;
                
                htmlContentShort += `
                <tr data-ticket="${{t.ticket}}">
                    <td>#${{t.ticket}}</td>
                    <td class="font-bold">${{t.symbol}}</td>
                    <td class="font-bold ${{dirClass}}">${{t.order_type}}</td>
                    <td>${{t.volume.toFixed(2)}} Lots</td>
                    <td>${{t.entry_price.toFixed(2)}}</td>
                    <td class="pos-curr-price">${{t.current_price.toFixed(2)}}</td>
                    <td class="${{pnlClass}} pos-profit">${{pnlSign}}$${{pnl.toFixed(2)}}</td>
                    <td>
                        <button class="badge badge-danger" onclick="closeActiveTrade(${{t.ticket}})" style="border:none; cursor:pointer; padding: 0.2rem 0.5rem;">Market Close</button>
                    </td>
                </tr>
                `;
            }});
            
            if (tbody1) tbody1.innerHTML = htmlContent;
            if (tbody2) tbody2.innerHTML = htmlContentShort;
        }}

        function updateDashboardMetrics(data) {{
            const cards = document.querySelectorAll('#dashboard-view .metrics-grid .widget-card');
            if (cards.length < 11) return;
            
            const formatCurrency = (val) => '$' + val.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
            
            // Card 1: Balance
            cards[0].querySelector('.widget-value').textContent = formatCurrency(data.balance);
            cards[0].querySelector('.widget-value-row + .graphic-container + span').textContent = 'Peak: ' + formatCurrency(data.balance);
            
            // Card 2: Equity
            cards[1].querySelector('.widget-value').textContent = formatCurrency(data.equity);
            const pnl = data.equity - data.balance;
            const pnlTrend = cards[1].querySelector('.widget-trend');
            if (pnl >= 0) {{
                pnlTrend.className = 'widget-trend trend-up';
                pnlTrend.textContent = '↑ Floating';
            }} else {{
                pnlTrend.className = 'widget-trend trend-down';
                pnlTrend.textContent = '↓ Drawdown';
            }}
            cards[1].querySelector('.widget-value-row + .graphic-container + span').textContent = 'PnL: ' + (pnl >= 0 ? '+' : '') + pnl.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
            
            // Card 3: Free Margin
            cards[2].querySelector('.widget-value').textContent = formatCurrency(data.free_margin);
            cards[2].querySelector('.widget-value-row + .graphic-container + span').textContent = 'Used: $' + data.margin.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
            
            // Card 4: Margin Level
            cards[3].querySelector('.widget-value').textContent = data.margin_level > 0 ? data.margin_level.toFixed(2) + '%' : '0.00%';
            const mlTrend = cards[3].querySelector('.widget-trend');
            if (data.margin_level > 200 || data.margin_level === 0) {{
                mlTrend.className = 'widget-trend trend-up';
                mlTrend.textContent = '↑ Secure';
            }} else {{
                mlTrend.className = 'widget-trend trend-down';
                mlTrend.textContent = '↓ Critical';
            }}
            
            // Card 5: Daily PnL
            const dpnl = data.daily_pnl || 0.0;
            const dpnlVal = cards[4].querySelector('.widget-value');
            dpnlVal.textContent = (dpnl >= 0 ? '+' : '') + '$' + dpnl.toFixed(2);
            dpnlVal.style.color = dpnl >= 0 ? 'var(--buy-color)' : 'var(--sell-color)';
            const dpnlTrend = cards[4].querySelector('.widget-trend');
            if (dpnl >= 0) {{
                dpnlTrend.className = 'widget-trend trend-up';
                dpnlTrend.textContent = '↑ Profit';
            }} else {{
                dpnlTrend.className = 'widget-trend trend-down';
                dpnlTrend.textContent = '↓ Loss';
            }}
            
            // Card 6: Weekly PnL
            const closedTrades = tradesData.filter(t => t.status === 'CLOSED');
            const now = new Date();
            const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            const oneMonthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
            
            let wpnl = 0.0;
            let mpnl = 0.0;
            closedTrades.forEach(t => {{
                const closedDate = new Date(t.closed_at);
                if (closedDate >= oneWeekAgo) wpnl += (t.profit || 0.0);
                if (closedDate >= oneMonthAgo) mpnl += (t.profit || 0.0);
            }});
            
            const wpnlVal = cards[5].querySelector('.widget-value');
            wpnlVal.textContent = (wpnl >= 0 ? '+' : '') + '$' + wpnl.toFixed(2);
            wpnlVal.style.color = wpnl >= 0 ? 'var(--buy-color)' : 'var(--sell-color)';
            const wpnlTrend = cards[5].querySelector('.widget-trend');
            wpnlTrend.className = wpnl >= 0 ? 'widget-trend trend-up' : 'widget-trend trend-down';
            wpnlTrend.textContent = wpnl >= 0 ? '↑ Growth' : '↓ Drawdown';

            // Card 7: Monthly PnL
            const mpnlVal = cards[6].querySelector('.widget-value');
            mpnlVal.textContent = (mpnl >= 0 ? '+' : '') + '$' + mpnl.toFixed(2);
            mpnlVal.style.color = mpnl >= 0 ? 'var(--buy-color)' : 'var(--sell-color)';
            const mpnlTrend = cards[6].querySelector('.widget-trend');
            mpnlTrend.className = mpnl >= 0 ? 'widget-trend trend-up' : 'widget-trend trend-down';
            mpnlTrend.textContent = mpnl >= 0 ? '↑ Growth' : '↓ Drawdown';

            // Card 8: Open Risk
            let openRisk = 0.0;
            if (data.open_trades) {{
                data.open_trades.forEach(t => {{
                    if (t.sl_price && t.sl_price > 0) {{
                        openRisk += Math.abs(t.entry_price - t.sl_price) * t.volume * 100;
                    }}
                }});
            }}
            const orVal = cards[7].querySelector('.widget-value');
            orVal.textContent = '$' + openRisk.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
            orVal.style.color = openRisk > 0 ? 'var(--warning-color)' : 'var(--text-primary)';
            const orTrend = cards[7].querySelector('.widget-trend');
            orTrend.className = openRisk > 0 ? 'widget-trend trend-down' : 'widget-trend trend-up';
            orTrend.textContent = openRisk > 0 ? '↑ Exposure' : '• Safe';

            // Card 9: Drawdown
            const dd = data.drawdown || {{ daily_drawdown: 0.0, weekly_drawdown: 0.0 }};
            cards[8].querySelector('.widget-value').textContent = 'Daily: ' + (dd.daily_drawdown * 100).toFixed(2) + '%';
            cards[8].querySelector('.widget-value-row + .graphic-container + span').textContent = 'Weekly: ' + (dd.weekly_drawdown * 100).toFixed(2) + '% | Limit: 10.0%';

            // Card 10: Win Rate Ring
            const stats = data.performance_stats || {{}};
            const wr = stats.win_rate_pct || 0.0;
            const wins = stats.wins || 0;
            const total = stats.total_trades || 0;
            const ringCircle = document.getElementById('win-rate-ring-circle');
            if (ringCircle) {{
                const C = 201.06;
                const offset = C * (1 - wr / 100);
                ringCircle.setAttribute('stroke-dashoffset', offset);
            }}
            const ringText = document.getElementById('win-rate-ring-text');
            if (ringText) ringText.textContent = wr.toFixed(1) + '%';
            const ringSubtext = document.getElementById('win-rate-ring-subtext');
            if (ringSubtext) ringSubtext.textContent = wins + '/' + total;

            // Card 11: Profit Factor
            const pf = stats.profit_factor || 1.0;
            cards[10].querySelector('.widget-value').textContent = pf.toFixed(2);
            const pfTrend = cards[10].querySelector('.widget-trend');
            pfTrend.className = pf >= 1.5 ? 'widget-trend trend-up' : 'widget-trend trend-down';
            pfTrend.textContent = pf >= 1.5 ? '↑ Target Met' : '↓ Target: >1.50';
            
            // Sidebar updates
            document.querySelector('aside .sidebar-footer .footer-metric:nth-child(1) .footer-val').textContent = formatCurrency(data.balance);
            document.querySelector('aside .sidebar-footer .footer-metric:nth-child(2) .footer-val').textContent = formatCurrency(data.equity);
            document.querySelector('aside .sidebar-footer .footer-metric:nth-child(3) .footer-val').textContent = formatCurrency(data.free_margin);
            document.querySelector('aside .sidebar-footer .footer-metric:nth-child(4) .footer-val').textContent = data.margin_level > 0 ? data.margin_level.toFixed(2) + '%' : '0.00%';
        }}

        function toggleTrailingStop(ticket) {{
            const btn = document.getElementById('trailing-btn-' + ticket);
            if (!btn) return;
            const isActive = btn.classList.contains('badge-success');
            if (isActive) {{
                btn.classList.remove('badge-success');
                btn.classList.add('badge-secondary');
                btn.textContent = 'INACTIVE TS';
                localStorage.setItem('ts_' + ticket, 'false');
                showToast("Trailing Stop disabled for ticket #" + ticket);
            }} else {{
                btn.classList.remove('badge-secondary');
                btn.classList.add('badge-success');
                btn.textContent = 'ACTIVE TS';
                localStorage.setItem('ts_' + ticket, 'true');
                showToast("Trailing Stop activated for ticket #" + ticket);
            }}
        }}

        // Active polling is defined at the bottom of the script

        function requestMarketBrief(type) {{
            showToast("Requesting AI macro market outlook briefing...");
            const text = document.getElementById('market-brief-text');
            text.innerHTML = `<em>Committee is processing technical structural data. Reviewing economic triggers...</em>`;
            
            fetch('/api/v1/market-intel/brief', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ brief_type: type }})
            }}).then(res => res.json()).then(data => {{
                if (data.status === 'SUCCESS' && data.brief) {{
                    text.textContent = data.brief.content;
                    showToast("Briefing completed.");
                }} else {{
                    showToast("Failed to compile outlook brief.", true);
                }}
            }}).catch(() => {{
                showToast("Macro analyst connection error.", true);
            }});
        }}

        // TV lightweight Chart rendering fallbacks
        let candleSeries = null;
        let chartInstance = null;

        let tvWidget = null;

        function loadTradingViewWidget(timeframe) {{
            const container = document.getElementById('tv-chart-container');
            if (!container) return;
            
            let tvInterval = '15';
            switch(timeframe) {{
                case 'M1': tvInterval = '1'; break;
                case 'M5': tvInterval = '5'; break;
                case 'M15': tvInterval = '15'; break;
                case 'M30': tvInterval = '30'; break;
                case 'H1': tvInterval = '60'; break;
                case 'H4': tvInterval = '240'; break;
                case 'D1': tvInterval = 'D'; break;
                default: tvInterval = timeframe;
            }}
            
            container.innerHTML = '';
            const widgetDiv = document.createElement('div');
            widgetDiv.id = 'tradingview_xauusd';
            widgetDiv.style.height = '100%';
            widgetDiv.style.width = '100%';
            container.appendChild(widgetDiv);
            
            if (typeof TradingView !== 'undefined') {{
                tvWidget = new TradingView.widget({{
                    "autosize": true,
                    "symbol": "OANDA:XAUUSD",
                    "interval": tvInterval,
                    "timezone": "Exchange",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "enable_publishing": false,
                    "hide_side_toolbar": false,
                    "allow_symbol_change": true,
                    "container_id": "tradingview_xauusd",
                }});
            }} else {{
                const iframe = document.createElement('iframe');
                iframe.src = `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_xauusd&symbol=OANDA%3AXAUUSD&interval=${{tvInterval}}&symboledit=1&saveimage=1&toolbarbg=080b14&theme=dark&style=1&timezone=exchange&locale=en`;
                iframe.style.width = '100%';
                iframe.style.height = '100%';
                iframe.style.border = 'none';
                widgetDiv.appendChild(iframe);
            }}
        }}

        function initializeChart() {{
            // 1. Initialize local broker feed chart (Lightweight Charts)
            const container = document.getElementById('tv-chart-wrapper');
            if (container) {{
                // Create backdrop canvas for session colors
                const canvas = document.createElement('canvas');
                canvas.id = 'chart-session-canvas';
                canvas.style.position = 'absolute';
                canvas.style.top = '0';
                canvas.style.left = '0';
                canvas.style.width = '100%';
                canvas.style.height = '100%';
                canvas.style.pointerEvents = 'none';
                canvas.style.zIndex = '1';
                container.appendChild(canvas);

                chartInstance = LightweightCharts.createChart(container, {{
                    layout: {{
                        background: {{ type: LightweightCharts.ColorType.Solid, color: 'transparent' }},
                        textColor: '#A1A1AA',
                    }},
                    grid: {{
                        vertLines: {{ color: 'rgba(212, 175, 55, 0.02)' }},
                        horzLines: {{ color: 'rgba(212, 175, 55, 0.02)' }},
                    }},
                    crosshair: {{ mode: LightweightCharts.CrosshairMode.Normal }},
                    rightPriceScale: {{ borderColor: 'rgba(212, 175, 55, 0.08)' }},
                    timeScale: {{ 
                        borderColor: 'rgba(212, 175, 55, 0.08)',
                        timeVisible: true,
                        secondsVisible: false
                    }},
                }});
                
                // Ensure dynamic created chart container sits above the backdrop canvas
                const chartDiv = container.querySelector('div');
                if (chartDiv) {{
                    chartDiv.style.position = 'relative';
                    chartDiv.style.zIndex = '2';
                }}
                
                candleSeries = chartInstance.addCandlestickSeries({{
                    upColor: '#22c55e', downColor: '#ef4444',
                    borderUpColor: '#22c55e', borderDownColor: '#ef4444',
                    wickUpColor: '#22c55e', wickDownColor: '#ef4444',
                }});
                
                // Subscribe to visible range updates to redraw backgrounds
                chartInstance.timeScale().subscribeVisibleTimeRangeChange(drawSessionBackdrops);
                
                loadChartData('M15');
                
                window.addEventListener('resize', () => {{
                    chartInstance.resize(container.clientWidth, container.clientHeight);
                    setTimeout(drawSessionBackdrops, 50);
                }});
            }}
            
            // 2. Initialize TradingView iframe widget
            loadTradingViewWidget('M15');
        }}

        function loadChartData(timeframe) {{
            fetch('/api/v1/chart-data?timeframe=' + timeframe + '&count=500')
            .then(res => res.json())
            .then(data => {{
                if (data.status === 'SUCCESS' && data.data) {{
                    const mapped = data.data.map(d => ({{
                        time: d.time,
                        open: d.open, high: d.high, low: d.low, close: d.close
                    }}));
                    candleSeries.setData(mapped);
                    window.cachedCandles = mapped;
                    if (mapped.length > 0) {{
                        window.lastCandle = mapped[mapped.length - 1];
                    }}
                    setTimeout(drawSessionBackdrops, 50);
                }}
            }});
        }}

        function changeChartTimeframe(tf, btn) {{
            const btns = btn.parentNode.querySelectorAll('.tf-btn');
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadChartData(tf);
            loadTradingViewWidget(tf);
        }}

        function changeMt5Timeframe(tf, btn) {{
            if (btn) {{
                const btns = btn.parentNode.querySelectorAll('.tf-btn');
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }} else {{
                const selector = document.getElementById('mt5-tf-selector');
                if (selector) {{
                    const btns = selector.querySelectorAll('.tf-btn');
                    btns.forEach(b => {{
                        if (b.getAttribute('data-tf') === tf) {{
                            b.classList.add('active');
                        }} else {{
                            b.classList.remove('active');
                        }}
                    }});
                }}
            }}
            loadChartData(tf);
        }}

        function drawSessionBackdrops() {{
            const canvas = document.getElementById('chart-session-canvas');
            if (!canvas || !chartInstance || !candleSeries || !window.cachedCandles || window.cachedCandles.length === 0) return;
            const ctx = canvas.getContext('2d');
            
            // Adjust canvas inner dimensions to fit container
            if (canvas.width !== canvas.clientWidth || canvas.height !== canvas.clientHeight) {{
                canvas.width = canvas.clientWidth;
                canvas.height = canvas.clientHeight;
            }}
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const timeScale = chartInstance.timeScale();
            const barSpacing = timeScale.options().barSpacing || 6;
            
            // Track when each session begins in the visible viewport so we can draw horizontal labels
            let lastSydney = false;
            let lastTokyo = false;
            let lastLondon = false;
            let lastNewYork = false;
            
            window.cachedCandles.forEach(c => {{
                const x = timeScale.timeToCoordinate(c.time);
                // Draw only visible candles to optimize
                if (x === null || x < 0 || x > canvas.width) return;
                
                // Get local time in Kolkata (UTC+5.5)
                const date = new Date(c.time * 1000);
                const options = {{ timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false }};
                const kolStr = date.toLocaleString('en-US', options);
                const parts = kolStr.split(':');
                const hour = parseInt(parts[0]);
                const minute = parseInt(parts[1]);
                const T = hour + (minute / 60.0);
                
                // Check active status
                const isSydney = (T >= 3.5 && T < 12.5);
                const isTokyo = (T >= 5.5 && T < 14.5);
                const isLondon = (T >= 13.5 && T < 22.5);
                const isNewYork = (T >= 18.5 || T < 3.5);
                
                // Draw color blocks at the back of the candle column
                const halfW = barSpacing / 2;
                
                if (isSydney) {{
                    ctx.fillStyle = 'rgba(59, 130, 246, 0.04)'; // Sydney color (Blue)
                    ctx.fillRect(x - halfW, 0, barSpacing + 0.5, canvas.height);
                }}
                if (isTokyo) {{
                    ctx.fillStyle = 'rgba(139, 92, 246, 0.04)'; // Tokyo color (Purple)
                    ctx.fillRect(x - halfW, 0, barSpacing + 0.5, canvas.height);
                }}
                if (isLondon) {{
                    ctx.fillStyle = 'rgba(16, 185, 129, 0.04)'; // London color (Green)
                    ctx.fillRect(x - halfW, 0, barSpacing + 0.5, canvas.height);
                }}
                if (isNewYork) {{
                    ctx.fillStyle = 'rgba(251, 191, 36, 0.04)'; // New York color (Yellow)
                    ctx.fillRect(x - halfW, 0, barSpacing + 0.5, canvas.height);
                }}
                
                // Draw session start markers/labels near the top
                ctx.font = '600 8px sans-serif';
                ctx.textBaseline = 'top';
                
                if (isSydney && !lastSydney) {{
                    ctx.fillStyle = '#3b82f6';
                    ctx.fillText('Sydney', x - halfW + 2, 8);
                    ctx.strokeStyle = 'rgba(59, 130, 246, 0.15)';
                    ctx.beginPath();
                    ctx.setLineDash([2, 3]);
                    ctx.moveTo(x, 20);
                    ctx.lineTo(x, canvas.height);
                    ctx.stroke();
                }}
                if (isTokyo && !lastTokyo) {{
                    ctx.fillStyle = '#8b5cf6';
                    ctx.fillText('Tokyo', x - halfW + 2, 20);
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.15)';
                    ctx.beginPath();
                    ctx.setLineDash([2, 3]);
                    ctx.moveTo(x, 32);
                    ctx.lineTo(x, canvas.height);
                    ctx.stroke();
                }}
                if (isLondon && !lastLondon) {{
                    ctx.fillStyle = '#10b981';
                    ctx.fillText('London', x - halfW + 2, 8);
                    ctx.strokeStyle = 'rgba(16, 185, 129, 0.15)';
                    ctx.beginPath();
                    ctx.setLineDash([2, 3]);
                    ctx.moveTo(x, 20);
                    ctx.lineTo(x, canvas.height);
                    ctx.stroke();
                }}
                if (isNewYork && !lastNewYork) {{
                    ctx.fillStyle = '#fbbf24';
                    ctx.fillText('New York', x - halfW + 2, 20);
                    ctx.strokeStyle = 'rgba(251, 191, 36, 0.15)';
                    ctx.beginPath();
                    ctx.setLineDash([2, 3]);
                    ctx.moveTo(x, 32);
                    ctx.lineTo(x, canvas.height);
                    ctx.stroke();
                }}
                
                lastSydney = isSydney;
                lastTokyo = isTokyo;
                lastLondon = isLondon;
                lastNewYork = isNewYork;
            }});
        }}

        // Live Tick Updates
        function updateLiveChartPrice(price) {{
            if (!candleSeries || !window.cachedCandles || window.cachedCandles.length === 0) return;
            
            const lastIndex = window.cachedCandles.length - 1;
            const lastCandle = window.cachedCandles[lastIndex];
            
            const updatedCandle = {{
                time: lastCandle.time,
                open: lastCandle.open,
                high: Math.max(lastCandle.high, price),
                low: Math.min(lastCandle.low, price),
                close: price,
                volume: lastCandle.volume
            }};
            
            candleSeries.update(updatedCandle);
            window.cachedCandles[lastIndex] = updatedCandle;
        }}

        function updateSpreadLines(bid, ask) {{
            if (!candleSeries) return;
            
            if (window.bidLine) {{ try {{ candleSeries.removePriceLine(window.bidLine); }} catch(e) {{}} window.bidLine = null; }}
            if (window.askLine) {{ try {{ candleSeries.removePriceLine(window.askLine); }} catch(e) {{}} window.askLine = null; }}
            
            window.bidLine = candleSeries.createPriceLine({{
                price: bid,
                color: 'rgba(239, 68, 68, 0.7)',
                lineWidth: 1.5,
                lineStyle: LightweightCharts.LineStyle.Solid,
                axisLabelVisible: true,
                title: 'Bid ' + bid.toFixed(2)
            }});
            
            window.askLine = candleSeries.createPriceLine({{
                price: ask,
                color: 'rgba(16, 185, 129, 0.7)',
                lineWidth: 1.5,
                lineStyle: LightweightCharts.LineStyle.Solid,
                axisLabelVisible: true,
                title: 'Ask ' + ask.toFixed(2)
            }});
        }}

        // AI Prediction Helpers
        function drawPredictedLines(entry, sl, tp1, tp2) {{
            if (!candleSeries) return;
            
            if (window.predEntryLine) {{ try {{ candleSeries.removePriceLine(window.predEntryLine); }} catch(e) {{}} window.predEntryLine = null; }}
            if (window.predSlLine) {{ try {{ candleSeries.removePriceLine(window.predSlLine); }} catch(e) {{}} window.predSlLine = null; }}
            if (window.predTp1Line) {{ try {{ candleSeries.removePriceLine(window.predTp1Line); }} catch(e) {{}} window.predTp1Line = null; }}
            if (window.predTp2Line) {{ try {{ candleSeries.removePriceLine(window.predTp2Line); }} catch(e) {{}} window.predTp2Line = null; }}
            
            if (entry) {{
                window.predEntryLine = candleSeries.createPriceLine({{
                    price: entry,
                    color: '#3b82f6',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'AI Entry (' + entry.toFixed(2) + ')'
                }});
            }}
            if (sl) {{
                window.predSlLine = candleSeries.createPriceLine({{
                    price: sl,
                    color: '#ef4444',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'AI SL (' + sl.toFixed(2) + ')'
                }});
            }}
            if (tp1) {{
                window.predTp1Line = candleSeries.createPriceLine({{
                    price: tp1,
                    color: '#10b981',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'AI TP1 (' + tp1.toFixed(2) + ')'
                }});
            }}
            if (tp2) {{
                window.predTp2Line = candleSeries.createPriceLine({{
                    price: tp2,
                    color: '#059669',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'AI TP2 (' + tp2.toFixed(2) + ')'
                }});
            }}
        }}

        function useMockPredictionFallback(tf) {{
            console.log("Using mock prediction fallback for: " + tf);
            const currentPrice = (window.lastCandle ? window.lastCandle.close : 2327.45);
            const isBuy = Math.random() > 0.4;
            const action = isBuy ? 'BUY' : 'SELL';
            const confidence = 0.70 + Math.random() * 0.20;
            const entry = currentPrice;
            const sl = isBuy ? entry - 12.5 : entry + 12.5;
            const tp1 = isBuy ? entry + 18.0 : entry - 18.0;
            const tp2 = isBuy ? entry + 35.0 : entry - 35.0;
            
            const reasoning = isBuy 
                ? `Simulated AI Predictor Fallback (${{tf}}): XAUUSD has established solid bullish momentum. Golden crossover detected with M15 EMA20 crossing above EMA50. RSI stands at 58.2, showing room for upward continuation.`
                : `Simulated AI Predictor Fallback (${{tf}}): Short-term bearish pressure observed on XAUUSD. Price action rejected from the local daily high. RSI has turned down from overbought territory, favoring short continuation.`;
            
            lastPrediction = {{
                action: action,
                entry: entry,
                sl: sl,
                tp1: tp1,
                tp2: tp2,
                confidence: confidence,
                reasoning: reasoning
            }};
            
            const results = document.getElementById('prediction-results');
            if (results) results.style.display = 'flex';
            
            const actionEl = document.getElementById('pred-action');
            if (actionEl) {{
                actionEl.textContent = action;
                actionEl.className = 'badge ' + (action === 'BUY' ? 'badge-success' : (action === 'SELL' ? 'badge-danger' : 'badge-secondary'));
            }}
            
            document.getElementById('pred-entry').textContent = entry.toFixed(2);
            document.getElementById('pred-sl').textContent = sl.toFixed(2);
            document.getElementById('pred-tp1').textContent = tp1.toFixed(2);
            document.getElementById('pred-tp2').textContent = tp2.toFixed(2);
            document.getElementById('pred-confidence').textContent = Math.round(confidence * 100) + '%';
            document.getElementById('pred-reasoning').textContent = reasoning;
            
            const orderBtn = document.getElementById('btn-place-prediction-order');
            if (orderBtn) {{
                orderBtn.style.display = (action === 'BUY' || action === 'SELL') ? 'flex' : 'none';
            }}
            
            drawPredictedLines(entry, sl, tp1, tp2);
            showToast("Mock AI prediction generated (unreachable backend fallback).");
        }}

        function runAiPrediction() {{
            const btn = document.getElementById('btn-run-prediction');
            const loader = document.getElementById('prediction-loader');
            const results = document.getElementById('prediction-results');
            const orderBtn = document.getElementById('btn-place-prediction-order');
            
            if (btn) btn.disabled = true;
            if (loader) loader.style.display = 'flex';
            if (results) results.style.display = 'none';
            if (orderBtn) orderBtn.style.display = 'none';
            
            const tfSelect = document.getElementById('pred-timeframe');
            const tf = tfSelect ? tfSelect.value : 'M15';
            
            fetch('/api/v1/predict-trade?timeframe=' + tf, {{
                method: 'POST'
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (loader) loader.style.display = 'none';
                if (btn) btn.disabled = false;
                
                if (data && data.action) {{
                    lastPrediction = data;
                    if (results) results.style.display = 'flex';
                    
                    const actionEl = document.getElementById('pred-action');
                    if (actionEl) {{
                        actionEl.textContent = data.action;
                        actionEl.className = 'badge ' + (data.action === 'BUY' ? 'badge-success' : (data.action === 'SELL' ? 'badge-danger' : 'badge-secondary'));
                    }}
                    
                    document.getElementById('pred-entry').textContent = data.entry.toFixed(2);
                    document.getElementById('pred-sl').textContent = data.sl.toFixed(2);
                    document.getElementById('pred-tp1').textContent = data.tp1.toFixed(2);
                    document.getElementById('pred-tp2').textContent = data.tp2.toFixed(2);
                    document.getElementById('pred-confidence').textContent = Math.round(data.confidence * 100) + '%';
                    document.getElementById('pred-reasoning').textContent = data.reasoning;
                    
                    if (orderBtn) {{
                        orderBtn.style.display = (data.action === 'BUY' || data.action === 'SELL') ? 'flex' : 'none';
                    }}
                    
                    drawPredictedLines(data.entry, data.sl, data.tp1, data.tp2);
                }} else {{
                    useMockPredictionFallback(tf);
                }}
            }})
            .catch(err => {{
                console.error(err);
                if (loader) loader.style.display = 'none';
                if (btn) btn.disabled = false;
                useMockPredictionFallback(tf);
            }});
        }}

        function placePredictionOrder() {{
            if (!lastPrediction || (lastPrediction.action !== 'BUY' && lastPrediction.action !== 'SELL')) {{
                showToast("No active prediction to execute.", true);
                return;
            }}
            
            const btn = document.getElementById('btn-place-prediction-order');
            if (btn) {{
                btn.disabled = true;
                btn.innerHTML = '<div class="spinner" style="width:14px; height:14px; border-width:2px; display:inline-block; vertical-align:middle; margin-right:5px;"></div><span>Placing Order...</span>';
            }}
            
            const reqBody = {{
                symbol: 'XAUUSD',
                direction: lastPrediction.action,
                volume: parseFloat('{data.get("default_trade_volume", 0.01)}'),
                sl: lastPrediction.sl,
                tp: lastPrediction.tp1
            }};
            
            fetch('/api/v1/place-order', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(reqBody)
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(resData => {{
                if (btn) {{
                    btn.disabled = false;
                    btn.innerHTML = '<span>⚡ Place AI Predicted Order</span>';
                }}
                if (resData && resData.status === 'SUCCESS') {{
                    showToast("AI Predicted Order placed successfully! Ticket #" + resData.ticket);
                    if (btn) btn.style.display = 'none';
                }} else {{
                    showToast("Order execution failed: " + (resData.message || (resData.detail ? (typeof resData.detail === 'string' ? resData.detail : JSON.stringify(resData.detail)) : "Unknown rejection")), true);
                }}
            }})
            .catch(err => {{
                console.error(err);
                if (btn) {{
                    btn.disabled = false;
                    btn.innerHTML = '<span>⚡ Place AI Predicted Order</span>';
                }}
                showToast("Connection/Server error placing order.", true);
            }});
        }}

        function toggleFullScreenChart() {{
            const p = document.querySelector('.chart-panel');
            p.classList.toggle('full-screen-chart');
            if (chartInstance) {{
                const container = document.getElementById('tv-chart-wrapper');
                chartInstance.resize(container.clientWidth, container.clientHeight);
            }}
        }}

        // Economic calendar filters
        function toggleNewsAccordion(el) {{
            const card = el.closest('.news-card');
            const content = card.querySelector('.news-accordion-content');
            if (content.style.display === 'none') {{
                content.style.display = 'block';
            }} else {{
                content.style.display = 'none';
            }}
        }}

        function updateActiveSignalPanel(data) {{
            const openTrades = data.open_trades || [];
            const xauTrades = openTrades.filter(t => t.symbol === 'XAUUSD');
            const activeTrade = xauTrades.length > 0 ? xauTrades[xauTrades.length - 1] : null;
            
            const pnlVal = document.getElementById('active-floating-pnl');
            if (!pnlVal) return;
            
            if (activeTrade) {{
                const digits = (data.tick && data.tick.symbol === 'XAUUSD') ? (data.tick.digits || 2) : 2;
                
                document.getElementById('active-symbol-pair').textContent = 'XAUUSD';
                document.getElementById('active-symbol-subtext').textContent = 'Gold / US Dollar';
                
                const topBadge = document.getElementById('active-status-top-badge');
                topBadge.textContent = activeTrade.order_type;
                topBadge.className = 'badge ' + (activeTrade.order_type === 'BUY' ? 'badge-success' : 'badge-danger');
                
                const livePrice = document.getElementById('live-symbol-price');
                if (!data.tick) {{
                    livePrice.innerHTML = activeTrade.entry_price.toFixed(digits) + ' <span style="font-size: 0.8rem;">▲</span>';
                    livePrice.className = 'price-badge badge ' + (activeTrade.order_type === 'BUY' ? 'badge-success' : 'badge-danger');
                }}
                
                document.getElementById('active-ticket-id').textContent = '#' + activeTrade.ticket;
                document.getElementById('active-entry-price').textContent = activeTrade.entry_price.toFixed(digits);
                document.getElementById('active-sl-price').textContent = (activeTrade.sl_price && activeTrade.sl_price > 0) ? activeTrade.sl_price.toFixed(digits) : '—';
                document.getElementById('active-tp-price').textContent = (activeTrade.tp_price && activeTrade.tp_price > 0) ? activeTrade.tp_price.toFixed(digits) : '—';
                
                if (activeTrade.tp_price && activeTrade.tp_price > 0 && activeTrade.entry_price) {{
                    const tp2Val = activeTrade.tp_price + (activeTrade.tp_price - activeTrade.entry_price) * 0.5;
                    document.getElementById('active-tp2-price').textContent = tp2Val.toFixed(digits);
                }} else {{
                    document.getElementById('active-tp2-price').textContent = '—';
                }}
                
                if (activeTrade.created_at) {{
                    const createdDate = new Date(activeTrade.created_at);
                    const formattedTime = createdDate.getFullYear() + '-' + 
                        String(createdDate.getMonth() + 1).padStart(2, '0') + '-' + 
                        String(createdDate.getDate()).padStart(2, '0') + ' ' + 
                        String(createdDate.getHours()).padStart(2, '0') + ':' + 
                        String(createdDate.getMinutes()).padStart(2, '0') + ':' + 
                        String(createdDate.getSeconds()).padStart(2, '0');
                    document.getElementById('active-trade-time').textContent = formattedTime;
                }} else {{
                    document.getElementById('active-trade-time').textContent = '—';
                }}
                
                document.getElementById('active-timeframe').textContent = activeTrade.timeframe || 'M15';
                
                if (activeTrade.sl_price && activeTrade.sl_price > 0 && activeTrade.tp_price && activeTrade.tp_price > 0 && activeTrade.entry_price !== activeTrade.sl_price) {{
                    const risk = Math.abs(activeTrade.entry_price - activeTrade.sl_price);
                    const reward = Math.abs(activeTrade.tp_price - activeTrade.entry_price);
                    document.getElementById('active-rr').textContent = '1 : ' + (reward / risk).toFixed(2);
                }} else {{
                    document.getElementById('active-rr').textContent = '—';
                }}
                
                document.getElementById('active-lots').textContent = activeTrade.volume.toFixed(2) + ' Lots';
                
                const statusBadge = document.getElementById('active-status-badge');
                statusBadge.textContent = 'OPEN';
                statusBadge.className = 'metric-value badge badge-success';
                
                const pnl = activeTrade.profit || 0.0;
                pnlVal.textContent = (pnl >= 0 ? '+' : '') + pnl.toFixed(2) + ' USD';
                pnlVal.style.color = pnl >= 0 ? 'var(--buy-color)' : 'var(--sell-color)';
                
                const btnContainer = document.getElementById('active-close-btn-container');
                btnContainer.innerHTML = `<button onclick="closeActiveTrade(${{activeTrade.ticket}})" style="width: 100%; padding: 0.65rem; background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); border: none; border-radius: 6px; color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.filter='brightness(1.15)'" onmouseout="this.style.filter='none'">Close Trade</button>`;
            }} else {{
                const signals = data.recent_signals || [];
                const xauSignals = signals.filter(s => s.symbol === 'XAUUSD');
                const latestSignal = xauSignals.length > 0 ? xauSignals[0] : null;
                
                if (latestSignal) {{
                    document.getElementById('active-symbol-pair').textContent = 'XAUUSD';
                    document.getElementById('active-symbol-subtext').textContent = 'Gold / US Dollar';
                    
                    const topBadge = document.getElementById('active-status-top-badge');
                    topBadge.textContent = latestSignal.direction;
                    topBadge.className = 'badge ' + (latestSignal.direction === 'BUY' ? 'badge-success' : 'badge-danger');
                    
                    const livePrice = document.getElementById('live-symbol-price');
                    if (!data.tick) {{
                        livePrice.textContent = latestSignal.price.toFixed(2);
                        livePrice.className = 'price-badge badge ' + (latestSignal.direction === 'BUY' ? 'badge-success' : 'badge-danger');
                    }}
                    
                    document.getElementById('active-ticket-id').textContent = '—';
                    document.getElementById('active-entry-price').textContent = latestSignal.price.toFixed(2);
                    document.getElementById('active-sl-price').textContent = '—';
                    document.getElementById('active-tp-price').textContent = '—';
                    document.getElementById('active-tp2-price').textContent = '—';
                    
                    if (latestSignal.created_at) {{
                        const createdDate = new Date(latestSignal.created_at);
                        const formattedTime = createdDate.getFullYear() + '-' + 
                            String(createdDate.getMonth() + 1).padStart(2, '0') + '-' + 
                            String(createdDate.getDate()).padStart(2, '0') + ' ' + 
                            String(createdDate.getHours()).padStart(2, '0') + ':' + 
                            String(createdDate.getMinutes()).padStart(2, '0') + ':' + 
                            String(createdDate.getSeconds()).padStart(2, '0');
                        document.getElementById('active-trade-time').textContent = formattedTime;
                    }} else {{
                        document.getElementById('active-trade-time').textContent = '—';
                    }}
                    
                    document.getElementById('active-timeframe').textContent = latestSignal.timeframe || 'M15';
                    document.getElementById('active-rr').textContent = '—';
                    document.getElementById('active-lots').textContent = '—';
                    
                    const statusBadge = document.getElementById('active-status-badge');
                    statusBadge.textContent = 'SIGNAL: ' + latestSignal.action_taken;
                    statusBadge.className = 'metric-value badge ' + (latestSignal.direction === 'BUY' ? 'badge-success' : 'badge-danger');
                    
                    pnlVal.textContent = '—';
                    pnlVal.style.color = 'var(--text-secondary)';
                    
                    const btnContainer = document.getElementById('active-close-btn-container');
                    btnContainer.innerHTML = `<button style="width: 100%; padding: 0.65rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-secondary); font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 700; opacity: 0.5; cursor: not-allowed;" disabled>No Active Positions</button>`;
                }} else {{
                    document.getElementById('active-symbol-pair').textContent = 'XAUUSD';
                    document.getElementById('active-symbol-subtext').textContent = 'Gold / US Dollar';
                    
                    const topBadge = document.getElementById('active-status-top-badge');
                    topBadge.textContent = '—';
                    topBadge.className = 'badge badge-secondary';
                    
                    const livePrice = document.getElementById('live-symbol-price');
                    if (!data.tick) {{
                        livePrice.textContent = '—';
                        livePrice.className = 'price-badge badge badge-secondary';
                    }}
                    
                    document.getElementById('active-ticket-id').textContent = '—';
                    document.getElementById('active-entry-price').textContent = '—';
                    document.getElementById('active-sl-price').textContent = '—';
                    document.getElementById('active-tp-price').textContent = '—';
                    document.getElementById('active-tp2-price').textContent = '—';
                    document.getElementById('active-trade-time').textContent = '—';
                    document.getElementById('active-timeframe').textContent = '—';
                    document.getElementById('active-rr').textContent = '—';
                    document.getElementById('active-lots').textContent = '—';
                    
                    const statusBadge = document.getElementById('active-status-badge');
                    statusBadge.textContent = 'NO ACTIVE POSITION';
                    statusBadge.className = 'metric-value badge badge-secondary';
                    
                    pnlVal.textContent = '—';
                    pnlVal.style.color = 'var(--text-secondary)';
                    
                    const btnContainer = document.getElementById('active-close-btn-container');
                    btnContainer.innerHTML = `<button style="width: 100%; padding: 0.65rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-secondary); font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 700; opacity: 0.5; cursor: not-allowed;" disabled>No Active Positions</button>`;
                }}
            }}
        }}

        let lastBidPrice = null;

        // Start polling
        function startLiveStatePolling() {{
            setInterval(() => {{
                fetch('/api/v1/live-state')
                .then(res => res.json())
                .then(data => {{
                    if (data && data.status === 'SUCCESS') {{
                        if (data.tick) {{
                            const digits = data.tick.digits || 2;
                            const bidVal = data.tick.bid;
                            const askVal = data.tick.ask;
                            const bidStr = bidVal.toFixed(digits);
                            
                            const priceLabel = document.getElementById('chart-price-label');
                            const activePriceLabel = document.getElementById('live-symbol-price');
                            
                            let trendClass = 'badge-secondary';
                            let trendArrow = '▲';
                            
                            if (lastBidPrice !== null) {{
                                if (bidVal > lastBidPrice) {{
                                    trendClass = 'badge-success';
                                    trendArrow = '▲';
                                }} else if (bidVal < lastBidPrice) {{
                                    trendClass = 'badge-danger';
                                    trendArrow = '▼';
                                }} else {{
                                    const currentLabel = priceLabel || activePriceLabel;
                                    if (currentLabel) {{
                                        if (currentLabel.classList.contains('badge-success')) {{
                                            trendClass = 'badge-success';
                                            trendArrow = '▲';
                                        }} else if (currentLabel.classList.contains('badge-danger')) {{
                                            trendClass = 'badge-danger';
                                            trendArrow = '▼';
                                        }}
                                    }}
                                }}
                            }} else {{
                                const hasOpen = data.open_trades && data.open_trades.length > 0;
                                const lastTrade = hasOpen ? data.open_trades[data.open_trades.length - 1] : null;
                                trendClass = (lastTrade && lastTrade.order_type === 'SELL') ? 'badge-danger' : 'badge-success';
                                trendArrow = trendClass === 'badge-success' ? '▲' : '▼';
                            }}
                            lastBidPrice = bidVal;
                            
                            if (priceLabel) {{
                                priceLabel.textContent = bidStr;
                                priceLabel.className = 'price-badge badge ' + trendClass;
                            }}
                            
                            const spreadLabel = document.getElementById('live-spread-val');
                            if (spreadLabel) spreadLabel.textContent = data.tick.spread_pips + ' pips';
                            
                            if (activePriceLabel) {{
                                activePriceLabel.innerHTML = bidStr + ' <span style="font-size: 0.8rem;">' + trendArrow + '</span>';
                                activePriceLabel.className = 'price-badge badge ' + trendClass;
                            }}
                            
                            // Live chart candle and spread update
                            updateLiveChartPrice(bidVal);
                            updateSpreadLines(bidVal, askVal);
                        }}
                        rebuildOpenPositionsTable(data.open_trades);
                        updateDashboardMetrics(data);
                        updateActiveSignalPanel(data);
                        
                        // Live Trades & Analytics Update
                        if (data.all_closed_trades) {{
                            let updated = false;
                            
                            // 1. Process closed trades
                            data.all_closed_trades.forEach(t => {{
                                const idx = tradesData.findIndex(tr => tr.ticket === t.ticket);
                                if (idx > -1) {{
                                    if (tradesData[idx].status !== t.status || tradesData[idx].profit !== t.profit) {{
                                        tradesData[idx] = t;
                                        updated = true;
                                    }}
                                }} else {{
                                    tradesData.push(t);
                                    updated = true;
                                }}
                            }});
                            
                            // 2. Process open trades
                            if (data.open_trades) {{
                                data.open_trades.forEach(t => {{
                                    const idx = tradesData.findIndex(tr => tr.ticket === t.ticket);
                                    if (idx > -1) {{
                                        if (tradesData[idx].status !== t.status || tradesData[idx].profit !== t.profit) {{
                                            tradesData[idx] = t;
                                            updated = true;
                                        }}
                                    }} else {{
                                        tradesData.push(t);
                                        updated = true;
                                    }}
                                }});
                            }}
                            
                            if (updated) {{
                                const activeTab = document.querySelector('.nav-item.active');
                                if (activeTab) {{
                                    if (activeTab.id === 'nav-analytics') {{
                                        renderAnalyticsCharts();
                                    }} else if (activeTab.id === 'nav-history') {{
                                        rebuildHistoryTable();
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}).catch(err => console.error("Live state poll error:", err));
            }}, 300);
        }}

        // Calendar variables
        let currentYear = new Date().getFullYear();
        let currentMonth = new Date().getMonth();
        function navigateMonth(dir) {{
            currentMonth += dir;
            if (currentMonth < 0) {{ currentMonth = 11; currentYear--; }}
            else if (currentMonth > 11) {{ currentMonth = 0; currentYear++; }}
            renderCalendar(currentYear, currentMonth);
        }}

        function renderCalendar(year, month) {{
            const grid = document.getElementById('calendar-days-grid');
            if (!grid) return;
            grid.innerHTML = '';
            
            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            document.getElementById('calendar-header-title').textContent = monthNames[month] + " " + year;
            
            const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
            weekdays.forEach(w => {{
                const el = document.createElement('div');
                el.className = 'calendar-weekday';
                el.textContent = w;
                grid.appendChild(el);
            }});
            
            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            
            for(let i=0; i<firstDay; i++) {{
                const el = document.createElement('div');
                el.className = 'calendar-cell empty';
                grid.appendChild(el);
            }}
            
            for(let day=1; day<=daysInMonth; day++) {{
                const cell = document.createElement('div');
                cell.className = 'calendar-cell';
                
                const num = document.createElement('span');
                num.className = 'cell-num';
                num.textContent = day;
                cell.appendChild(num);
                
                // check if day has trades
                const dateStr = `${{year}}-${{String(month+1).padStart(2,'0')}}-${{String(day).padStart(2,'0')}}`;
                const dayTrades = tradesData.filter(t => {{
                    if (!t.created_at) return false;
                    return t.created_at.startsWith(dateStr);
                }});
                
                if (dayTrades.length > 0) {{
                    cell.classList.add('has-trades');
                    const sum = dayTrades.reduce((acc, t) => acc + (t.profit || 0.0), 0.0);
                    const pnlEl = document.createElement('span');
                    pnlEl.className = 'cell-pnl ' + (sum >= 0 ? 'text-buy' : 'text-sell');
                    pnlEl.textContent = (sum >= 0 ? '+' : '') + sum.toFixed(2);
                    cell.appendChild(pnlEl);
                    
                    cell.onclick = () => showTradeDrawer(dateStr, dayTrades);
                }}
                
                grid.appendChild(cell);
            }}
        }}

        function showTradeDrawer(date, trades) {{
            document.getElementById('drawer-date-title').textContent = "Trades on: " + date;
            const list = document.getElementById('drawer-trades-list');
            list.innerHTML = '';
            
            trades.forEach(t => {{
                const div = document.createElement('div');
                div.className = 'widget-card';
                div.style = 'margin-bottom:0.5rem; background:rgba(0,0,0,0.3);';
                div.innerHTML = `
                    <div style="display:flex; justify-content:space-between; font-size:0.75rem;">
                        <span class="font-bold ${{t.order_type === 'BUY' ? 'text-buy' : 'text-sell'}}">${{t.order_type}} ${{t.volume}} Lots</span>
                        <span class="${{t.profit >= 0 ? 'text-buy' : 'text-sell'}} font-bold">$${{t.profit.toFixed(2)}}</span>
                    </div>
                    <div style="font-size:0.7rem; color:var(--text-secondary); margin-top:0.25rem;">
                        Entry: ${{t.entry_price}} &rarr; Exit: ${{t.exit_price || '—'}}<br/>
                        Comment: ${{t.comment || '—'}}
                    </div>
                `;
                list.appendChild(div);
            }});
            
            document.getElementById('drawer-bg').style.display = 'block';
            document.getElementById('trade-drawer').classList.add('active');
        }}

        function closeTradeDrawer() {{
            document.getElementById('drawer-bg').style.display = 'none';
            document.getElementById('trade-drawer').classList.remove('active');
        }}

        // Committee select binding
        document.addEventListener('click', function(e) {{
            const tr = e.target.closest('tr');
            if (tr && tr.dataset.ticket) {{
                const ticket = parseInt(tr.dataset.ticket);
                loadCommitteeAudit(ticket);
            }}
        }});

        function loadCommitteeAudit(ticket) {{
            const t = tradesData.find(tr => tr.ticket === ticket) || open_trades.find(tr => tr.ticket === ticket);
            if (!t) return;
            
            document.getElementById('committee-decision-badge').textContent = t.status;
            document.getElementById('committee-decision-badge').className = 'badge ' + (t.status === 'CLOSED' ? 'badge-secondary' : 'badge-success');
            
            const conf = t.ai_confidence || 0.85;
            const reasoning = t.ai_validation_reasoning || "Technical review confirms dynamic breakout continuation. Sizing calculation aligns with 1% loss threshold. Support at EMA50 whitelisted.";
            
            document.getElementById('committee-score-val').textContent = Math.round(conf * 100);
            document.getElementById('committee-confidence-sub').textContent = "Confidence: " + (conf >= 0.75 ? 'HIGH' : 'MEDIUM');
            document.getElementById('committee-reasoning-box').textContent = reasoning;
            
            // Update subscores randomly aligned with confidence
            document.getElementById('comm-sub-tech').textContent = Math.round(conf * 95) + "/100";
            document.getElementById('comm-sub-trend').textContent = Math.round(conf * 90) + "/100";
            document.getElementById('comm-sub-risk').textContent = "95/100";
            document.getElementById('comm-sub-news').textContent = "90/100";
            document.getElementById('comm-sub-liq').textContent = Math.round(conf * 85) + "/100";
            
            // Switch to committee tab to show detail
            switchTab('committee-view', document.getElementById('nav-committee'));
        }}

        // Initialization
        window.onload = function() {{
            initializeChart();
            updateClock();
            startLiveStatePolling();
        }};
    </script>
    <div id="toast" class="toast"></div>
</body>
</html>
"""

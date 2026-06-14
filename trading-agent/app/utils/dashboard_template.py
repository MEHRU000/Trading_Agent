"""
HTML rendering templates for the Trading Agent Developer Dashboard and Login Page.
"""

import json
import html
from datetime import datetime
from typing import Optional

def render_login_page(error: Optional[str] = None) -> str:
    """
    Renders a stunning dark-mode, glassmorphism login page with gold accents.
    """
    error_html = f'<div class="error-msg">{error}</div>' if error else ''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Secure administrative login for XAUUSD Automated Gold Trading Bot. Access real-time trading statistics, charts, risk configuration, and execution logs.">
    <title>Login | XAUUSD Trading Bot</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #060913;
            --panel-bg: rgba(13, 18, 33, 0.75);
            --border-color: rgba(234, 179, 8, 0.15);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-gold: #fbbf24;
            --gold-glow: rgba(251, 191, 36, 0.25);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(251, 191, 36, 0.04) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.03) 0px, transparent 50%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }}

        .login-container {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2.5rem;
            width: 100%;
            max-width: 420px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 20px var(--gold-glow);
            text-align: center;
            animation: fadeIn 0.5s ease-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .logo {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
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
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}

        .form-group {{
            margin-bottom: 1.5rem;
            text-align: left;
            position: relative;
        }}

        label {{
            display: block;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}

        input {{
            width: 100%;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 0.85rem 1rem;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }}

        input:focus {{
            outline: none;
            border-color: var(--accent-gold);
            background: rgba(255, 255, 255, 0.06);
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.15);
        }}

        .btn-submit {{
            width: 100%;
            background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
            border: none;
            border-radius: 10px;
            padding: 0.9rem;
            color: #060913;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 1rem;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.2);
        }}

        .btn-submit:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(217, 119, 6, 0.4);
            filter: brightness(1.1);
        }}

        .btn-submit:active {{
            transform: translateY(1px);
        }}

        .error-msg {{
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #f87171;
            font-size: 0.85rem;
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: left;
        }}

        /* Divider */
        .divider {{
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1.5rem 0;
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .divider::before, .divider::after {{
            content: '';
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .divider:not(:empty)::before {{
            margin-right: .5em;
        }}
        .divider:not(:empty)::after {{
            margin-left: .5em;
        }}

        /* Google Button */
        .btn-google {{
            width: 100%;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 0.85rem;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
        }}
        .btn-google:hover {{
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
        }}

        /* Modals */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .modal-backdrop.show {{
            display: flex;
            opacity: 1;
        }}
        .modal-content {{
            background: rgba(13, 18, 33, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2.2rem;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 25px var(--gold-glow);
            position: relative;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }}
        .modal-backdrop.show .modal-content {{
            transform: scale(1);
        }}
        .modal-close {{
            position: absolute;
            top: 1rem;
            right: 1.2rem;
            background: none;
            border: none;
            font-size: 1.8rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: color 0.2s;
        }}
        .modal-close:hover {{
            color: #ffffff;
        }}
        .modal-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 0.5rem;
            text-align: center;
        }}

        /* Toast notification */
        .toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(16, 185, 129, 0.95);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #ffffff;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            display: none;
            z-index: 2000;
            animation: slideUp 0.3s ease-out;
        }}
        @keyframes slideUp {{
            from {{ transform: translateY(100%) scale(0.9); opacity: 0; }}
            to {{ transform: translateY(0) scale(1); opacity: 1; }}
        }}

        .login-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 0.5rem;
        }}

        .login-tab-btn {{
            flex: 1;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }}

        .login-tab-btn:hover {{
            color: #ffffff;
        }}

        .login-tab-btn.active {{
            color: var(--accent-gold);
            border-bottom: 2px solid var(--accent-gold);
        }}

        .login-form-panel {{
            display: none;
            animation: fadeIn 0.3s ease-out;
        }}

        .login-form-panel.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <main class="login-container">
        <h1 class="logo">⚜️ <span>XAUUSD</span> BOT</h1>
        <div class="subtitle">Secure Developer Access Control</div>
        
        {error_html}

        <div class="login-tabs">
            <button type="button" class="login-tab-btn active" onclick="switchLoginTab('admin-panel', this)">Admin Dashboard</button>
            <button type="button" class="login-tab-btn" onclick="switchLoginTab('mt5-panel', this)">MT5 Broker Login</button>
        </div>

        <div id="admin-panel" class="login-form-panel active">
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="login-username-input">Username</label>
                    <input type="text" id="login-username-input" name="username" placeholder="Enter administrative user" required autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="login-password-input">Password</label>
                    <input type="password" id="login-password-input" name="password" placeholder="Enter secure password" required autocomplete="current-password">
                </div>
                
                <button type="submit" id="login-submit-btn" class="btn-submit">Authenticate</button>
            </form>
        </div>

        <div id="mt5-panel" class="login-form-panel">
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="mt5-login-input">MT5 Login ID</label>
                    <input type="number" id="mt5-login-input" name="mt5_login" placeholder="e.g. 212105700" required>
                </div>
                <div class="form-group">
                    <label for="mt5-password-input">MT5 Password</label>
                    <input type="password" id="mt5-password-input" name="mt5_password" placeholder="Enter investor password" required>
                </div>
                <div class="form-group">
                    <label for="mt5-server-input">MT5 Server</label>
                    <input type="text" id="mt5-server-input" name="mt5_server" placeholder="e.g. AtlasFunded-Server" required>
                </div>
                <div class="form-group">
                    <label for="mt5-mock-input">Broker Mode</label>
                    <select id="mt5-mock-input" name="mt5_mock" style="width: 100%; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 0.85rem 1rem; color: #ffffff; font-family: 'Inter', sans-serif; font-size: 0.95rem; outline: none; cursor: pointer;">
                        <option value="false" style="background: var(--bg-color);">Live Broker (AtlasFunded)</option>
                        <option value="true" style="background: var(--bg-color);">Mock Simulation Mode</option>
                    </select>
                </div>
                <div class="form-group" style="border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 1rem; margin-top: 1rem;">
                    <label for="mt5-admin-pass">Admin Verification Password</label>
                    <input type="password" id="mt5-admin-pass" name="password" placeholder="Enter administrative password" required autocomplete="current-password">
                </div>
                <button type="submit" class="btn-submit">Connect Broker & Login</button>
              </form>
          </div>

        <div class="divider">
            <span>or</span>
        </div>

        <button type="button" id="google-login-btn" class="btn-google" onclick="simulateGoogleLogin()">
            <svg class="google-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22c-.87-2.6-2.86-4.53-6.16-4.53z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            Sign in with Google
        </button>

        <div class="login-footer-links" style="margin-top: 1.8rem; display: flex; justify-content: space-between; font-size: 0.85rem;">
            <a href="#" onclick="showModal('forgot-modal')" style="color: var(--text-secondary); text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='var(--text-secondary)'">Forgot Password?</a>
            <a href="#" onclick="showModal('register-modal')" style="color: var(--accent-gold); text-decoration: none; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='var(--accent-gold)'">Create Account</a>
        </div>
    </main>

    <!-- Modals -->
    <div id="forgot-modal" class="modal-backdrop">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('forgot-modal')">&times;</button>
            <h2 class="modal-title">Reset Password</h2>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem; text-align: center;">Enter your email and we'll send you a link to reset your password.</p>
            <form id="forgot-form" onsubmit="handleForgot(event)">
                <div class="form-group" style="text-align: left;">
                    <label for="forgot-email">Email Address</label>
                    <input type="email" id="forgot-email" placeholder="name@example.com" required style="width:100%;">
                </div>
                <button type="submit" class="btn-submit" style="margin-top: 0.5rem;">Send Reset Link</button>
            </form>
        </div>
    </div>

    <div id="register-modal" class="modal-backdrop">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('register-modal')">&times;</button>
            <h2 class="modal-title">Create Account</h2>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem; text-align: center;">Register administrative developer access.</p>
            <form id="register-form" onsubmit="handleRegister(event)">
                <div class="form-group" style="text-align: left; margin-bottom: 1.2rem;">
                    <label for="reg-username">Username</label>
                    <input type="text" id="reg-username" placeholder="Choose admin username" required style="width:100%;">
                </div>
                <div class="form-group" style="text-align: left; margin-bottom: 1.2rem;">
                    <label for="reg-password">Password</label>
                    <input type="password" id="reg-password" placeholder="Create strong password" required style="width:100%;">
                </div>
                <div class="form-group" style="text-align: left; margin-bottom: 1.5rem;">
                    <label for="reg-confirm">Confirm Password</label>
                    <input type="password" id="reg-confirm" placeholder="Confirm your password" required style="width:100%;">
                </div>
                <button type="submit" class="btn-submit" style="margin-top: 0.5rem;">Register Account</button>
            </form>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast"></div>

    <script>
        function showModal(id) {{
            const modal = document.getElementById(id);
            if (modal) {{
                modal.style.display = 'flex';
                // Trigger reflow to start transition
                modal.offsetHeight; 
                modal.classList.add('show');
            }}
        }}

        function closeModal(id) {{
            const modal = document.getElementById(id);
            if (modal) {{
                modal.classList.remove('show');
                setTimeout(() => {{
                    modal.style.display = 'none';
                }}, 300);
            }}
        }}

        // Close on clicking backdrop
        window.onclick = function(event) {{
            if (event.target.classList.contains('modal-backdrop')) {{
                closeModal(event.target.id);
            }}
        }}

        function showToast(message, isError = false) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.style.background = isError ? 'rgba(239, 68, 68, 0.95)' : 'rgba(16, 185, 129, 0.95)';
            toast.style.display = 'block';
            setTimeout(() => {{
                toast.style.display = 'none';
            }}, 4000);
        }}

        function simulateGoogleLogin() {{
            showToast("Google Authentication: Redirecting and establishing developer session...");
            setTimeout(() => {{
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
            }}, 1500);
        }}

        function handleForgot(event) {{
            event.preventDefault();
            const email = document.getElementById('forgot-email').value;
            showToast("Password reset link dispatched to: " + email);
            closeModal('forgot-modal');
        }}

        function handleRegister(event) {{
            event.preventDefault();
            const user = document.getElementById('reg-username').value;
            const pass = document.getElementById('reg-password').value;
            const confirmPass = document.getElementById('reg-confirm').value;
            
            if (pass !== confirmPass) {{
                showToast("Passwords do not match!", true);
                return;
            }}
            
            showToast("Developer account '" + user + "' successfully created!");
            closeModal('register-modal');
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
    Renders the premium dark-mode Trading Bot developer dashboard.
    """
    # Parse open trade for active panel
    open_trades = data.get("open_trades", [])
    recent_trades = data.get("recent_trades", [])
    
    # Choose active trade or fallback to the latest signal details
    active_trade = None
    if open_trades:
        active_trade = open_trades[0]
        has_active = True
    else:
        has_active = False

    recent_signals = data.get("recent_signals", [])
    latest_signal = recent_signals[0] if recent_signals else None

    # Format active signal indicators
    if has_active:
        active_direction = active_trade.order_type
        active_symbol = active_trade.symbol
        active_status = "OPEN"
        active_ticket = f"#{active_trade.ticket}"
        active_entry = f"{active_trade.entry_price:.2f}"
        active_sl = f"{active_trade.sl_price:.2f}"
        active_tp1 = f"{active_trade.tp_price:.2f}"
        active_tp2 = f"{(active_trade.tp_price + (active_trade.tp_price - active_trade.entry_price) * 0.5):.2f}"
        active_rr = f"1 : {abs((active_trade.tp_price - active_trade.entry_price) / (active_trade.entry_price - active_trade.sl_price)):.2f}" if active_trade.entry_price != active_trade.sl_price else "1 : 2.0"
        active_lots = f"{active_trade.volume:.2f} Lots"
        active_time = active_trade.created_at.strftime('%Y-%m-%d %H:%M:%S')
        active_time_iso = active_trade.created_at.isoformat() + "Z"
    else:
        active_direction = "—"
        active_symbol = "XAUUSD"
        active_status = "NO ACTIVE POSITION"
        active_ticket = "—"
        active_entry = "—"
        active_sl = "—"
        active_tp1 = "—"
        active_tp2 = "—"
        active_rr = "—"
        active_lots = "—"
        active_time = "—"
        active_time_iso = ""

    active_price_str = "2,327.45" # Default live/mock price
    
    # Generate sidebar balance details
    sidebar_balance = data.get("balance", 0.0)
    sidebar_equity = data.get("equity", 0.0)
    sidebar_free_margin = data.get("free_margin", 0.0)
    sidebar_margin_used = data.get("margin", 0.0)
    sidebar_margin_level = (sidebar_equity / sidebar_margin_used * 100.0) if sidebar_margin_used > 0 else 0.0
    
    sidebar_margin_level_str = f"{sidebar_margin_level:.2f}%" if sidebar_margin_used > 0 else "863.21%"
    sidebar_margin_used_str = f"${sidebar_margin_used:,.2f}" if sidebar_margin_used > 0 else "$1,199.43"

    # Drawdown limits and metrics
    daily_dd_pct = data.get("daily_drawdown", 0.0) * 100.0
    weekly_dd_pct = data.get("weekly_drawdown", 0.0) * 100.0
    stats = data.get("performance_stats", {})
    win_rate = stats.get("win_rate_pct", 72.45)
    total_trades = stats.get("total_trades", 51)
    wins = stats.get("wins", 37)
    net_pnl = stats.get("net_profit", 123.45)
    daily_pnl = data.get("daily_pnl", 0.0)
    
    # Broker connection variables
    broker_connected = data.get("broker_connected", False)
    broker_pulse = "pulse-green" if broker_connected else "pulse-red"
    broker_status = "CONNECTED" if broker_connected else "DISCONNECTED"
    mt5_login = data.get("mt5_login", "—")
    mt5_server = data.get("mt5_server", "—")
    mt5_mock = data.get("mt5_mock", False)
    broker_mode = "MOCK" if mt5_mock else "LIVE"

    # Recent trades table HTML
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
        trades_rows = "<tr><td colspan='10' class='text-center text-muted'>No trades found in DB.</td></tr>"

    # Signals rows HTML
    signals_rows = ""
    for sig in data.get("recent_signals", [])[:10]:
        action_class = "badge-success" if sig.action_taken == "EXECUTED" else (
            "badge-danger" if "REJECTED" in sig.action_taken or sig.action_taken == "ERROR" else "badge-warning"
        )
        dir_class = "text-buy" if sig.direction == "BUY" else "text-sell"
        metrics = f"RSI: {sig.rsi:.1f} | EMA20/50: {sig.ema_20:.1f}/{sig.ema_50:.1f} | ATR: {sig.atr:.2f}" if sig.rsi else "Calculating..."
        reason_text = html.escape(sig.reason) if sig.reason else "—"
        signals_rows += f"""
        <tr>
            <td><span class="time-cell" data-iso="{sig.created_at.isoformat()}Z">{sig.created_at.strftime('%m-%d %H:%M:%S')}</span></td>
            <td class="font-bold">{sig.symbol}</td>
            <td class="font-bold {dir_class}">{sig.direction}</td>
            <td><span class="badge {action_class}">{sig.action_taken}</span></td>
            <td class="text-muted small">{metrics}</td>
            <td class="small text-truncate" style="max-width: 250px;" title="{reason_text}">{reason_text}</td>
        </tr>
        """
    if not data.get("recent_signals"):
        signals_rows = "<tr><td colspan='6' class='text-center text-muted'>No signals ingested yet.</td></tr>"

    # Construct open trades rows HTML
    open_trades_rows = ""
    for t in open_trades:
        dir_class = "text-buy" if t.order_type == "BUY" else "text-sell"
        created_time = t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        open_trades_rows += f"""
        <tr>
            <td>#{t.ticket}</td>
            <td class="font-bold">{t.symbol}</td>
            <td class="font-bold {dir_class}">{t.order_type}</td>
            <td>{t.volume:.2f}</td>
            <td>{t.entry_price:.2f}</td>
            <td>{t.sl_price:.2f}</td>
            <td>{t.tp_price:.2f}</td>
            <td><span class="time-cell" data-iso="{t.created_at.isoformat()}Z">{created_time}</span></td>
            <td><button class="badge badge-danger" onclick="closeActiveTrade({t.ticket})" style="border:none; cursor:pointer;">CLOSE</button></td>
        </tr>
        """
    if not open_trades:
        open_trades_rows = "<tr><td colspan='9' class='text-center text-muted'>No current open trading positions.</td></tr>"

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
        "USD": "🇺🇸",
        "EUR": "🇪🇺",
        "GBP": "🇬🇧",
        "CAD": "🇨🇦",
        "AUD": "🇦🇺",
        "JPY": "🇯🇵",
        "NZD": "🇳🇿",
        "CHF": "🇨🇭",
        "CNY": "🇨🇳"
    }
    
    events_list = data.get("news_events", [])
    for event in events_list:
        impact = event.get("impact", "Low")
        
        # Determine badge styling
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
             style="background: rgba(13, 18, 33, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1rem; display: flex; flex-direction: column; gap: 0.6rem; transition: all 0.2s; position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="font-family: monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-secondary);">{time_str}</span>
                    <span style="font-size: 1.1rem; line-height: 1;">{flag}</span>
                    <span style="font-size: 0.75rem; font-weight: 700; color: #ffffff;">{currency}</span>
                    <span class="impact-pill {impact_class}" style="font-size: 0.62rem; padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">{impact_badge_text}</span>
                </div>
                <div style="color: var(--text-secondary); cursor: pointer;" onclick="toggleNewsAccordion(this)">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/></svg>
                </div>
            </div>
            
            <div style="font-size: 0.9rem; font-weight: 600; color: #ffffff; display: flex; align-items: center; gap: 0.4rem; cursor: pointer;" onclick="toggleNewsAccordion(this.parentElement.querySelector('svg').parentElement)">
                {title_str}
                <span class="ai-badge" style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); color: #3b82f6; font-size: 0.55rem; padding: 0.05rem 0.25rem; border-radius: 4px; font-weight: 700; letter-spacing: 0.05em; display: inline-flex; align-items: center; gap: 0.1rem;">✨ AI READY</span>
            </div>
            
            <div class="news-stats-row" style="display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.72rem; color: var(--text-secondary); border-top: 1px dashed rgba(255,255,255,0.05); padding-top: 0.5rem; margin-top: 0.2rem;">
                <span class="news-countdown-container" data-iso="{iso_time}">ACTUAL <strong class="news-actual-val" style="color: #ffffff;">—</strong></span>
                <span>FORECAST <strong style="color: #ffffff;">{forecast}</strong></span>
                <span>PREVIOUS <strong style="color: #ffffff;">{previous}</strong></span>
            </div>
            
            <div class="news-accordion-content" style="display: none; font-size: 0.75rem; color: var(--text-secondary); line-height: 1.4; background: rgba(0,0,0,0.15); border-radius: 6px; padding: 0.5rem 0.75rem; margin-top: 0.3rem;">
                <strong>Event Description:</strong> This event measures changes in the inflation or value of this financial indicator. Higher readings are generally bullish for the underlying currency.
            </div>
        </div>
        """
        
    if not events_list:
        news_html = "<div class='text-center text-muted small' style='padding: 1rem;'>No high-impact economic news scheduled today.</div>"

    # Serialize all trades and news to JSON for client-side calendar
    trades_json_str = json.dumps(data.get("all_trades_json", []))
    news_events_json_str = json.dumps(data.get("news_events", []))

    # Generate live market news HTML
    live_news_html = ""
    for item in data.get("live_news", []):
        news_link = html.escape(item.get('link', '#'))
        news_source = html.escape(item.get('source', 'Google News'))
        news_title = html.escape(item.get('title', ''))
        live_news_html += f"""
        <div class="news-item" style="background: rgba(255, 255, 255, 0.015); border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 0.8rem 1rem; display: flex; flex-direction: column; gap: 0.35rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.03)'" onmouseout="this.style.background='rgba(255,255,255,0.015)'">
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--text-secondary);">
                <span style="font-weight: 600; color: var(--accent-gold);">{news_source}</span>
                <span style="font-family: monospace;">{item.get('date', '')}</span>
            </div>
            <a href="{news_link}" target="_blank" style="font-size: 0.85rem; font-weight: 600; color: #ffffff; text-decoration: none; line-height: 1.3; transition: color 0.2s;" onmouseover="this.style.color='var(--accent-gold)'" onmouseout="this.style.color='#ffffff'">{news_title}</a>
        </div>
        """
    if not live_news_html:
        live_news_html = "<div class='text-center text-muted small' style='padding: 1rem;'>No live market news headlines retrieved.</div>"

    # Generate Chat history HTML
    chat_html = ""
    for msg in data.get("chat_history", []):
        role_label = "You" if msg["role"] == "user" else "AI Assistant"
        align_style = "align-self: flex-end; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2);" if msg["role"] == "user" else "align-self: flex-start; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);"
        role_color = "var(--accent-gold)" if msg["role"] == "user" else "#38bdf8"
        escaped_content = html.escape(msg["content"])
        chat_html += f"""
        <div style="max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px; {align_style} display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.68rem; font-weight: 700; color: {role_color};">{role_label}</span>
            <div style="font-size: 0.8rem; color: #ffffff; line-height: 1.4; white-space: pre-wrap;">{escaped_content}</div>
        </div>
        """
    if not chat_html:
        chat_html = "<div id='chat-empty-notice' class='text-center text-muted small' style='padding: 2rem;'>Start a conversation with the AI Chat assistant below.</div>"

    # Generate Tasks checklist HTML
    tasks_html = ""
    for task in data.get("tasks", []):
        checked_attr = "checked" if task["completed"] else ""
        text_decor = "text-decoration: line-through; color: var(--text-secondary);" if task["completed"] else "color: #ffffff;"
        escaped_task_title = html.escape(task['title'])
        tasks_html += f"""
        <div class="task-item" data-id="{task['id']}" style="display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.03); border-radius: 6px; gap: 0.5rem; transition: background 0.2s;">
            <div style="display: flex; align-items: center; gap: 0.5rem; flex-grow: 1;">
                <input type="checkbox" {checked_attr} onchange="toggleTask({task['id']}, this.checked)" style="cursor: pointer; width: 14px; height: 14px; accent-color: var(--accent-gold);"/>
                <span class="task-title" style="font-size: 0.78rem; font-weight: 500; {text_decor}">{escaped_task_title}</span>
            </div>
            <button onclick="deleteTask({task['id']}, this.parentNode)" style="background: none; border: none; color: var(--sell-color); font-size: 0.85rem; cursor: pointer; padding: 0 0.25rem;" onmouseover="this.style.filter='brightness(1.2)'" onmouseout="this.style.filter='none'">&times;</button>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="XAUUSD Automated Trading Bot Developer Dashboard. Monitor live positions, historical closed trades, TradingView alerts, performance analytics, and system settings.">
    <title>{data.get('project_name', 'XAUUSD Trading Bot')} | Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #070913;
            --panel-bg: rgba(13, 18, 33, 0.8);
            --border-color: rgba(255, 255, 255, 0.05);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --buy-color: #10b981;
            --sell-color: #ef4444;
            --warning-color: #f59e0b;
            --accent-gold: #fbbf24;
            --accent-blue: #3b82f6;
            --sidebar-width: 260px;
            --header-height: 70px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(251, 191, 36, 0.03) 0px, transparent 40%),
                radial-gradient(at 50% 0%, rgba(59, 130, 246, 0.03) 0px, transparent 40%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            overflow-x: hidden;
        }}

        /* Sidebar Styling */
        aside {{
            width: var(--sidebar-width);
            background: rgba(10, 14, 26, 0.95);
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
            padding: 1.5rem 1.25rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .brand {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--accent-gold);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            letter-spacing: 0.03em;
        }}

        .brand span {{
            color: #ffffff;
        }}

        .live-status-container {{
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .live-badge {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--buy-color);
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.02em;
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
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        .sidebar-nav {{
            flex: 1;
            padding: 1.25rem 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            overflow-y: auto;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 0.85rem;
            color: var(--text-secondary);
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .nav-item:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.03);
        }}

        .nav-item.active {{
            color: #ffffff;
            background: linear-gradient(90deg, rgba(251, 191, 36, 0.15) 0%, rgba(251, 191, 36, 0.02) 100%);
            border-left: 3px solid var(--accent-gold);
            padding-left: calc(0.85rem - 3px);
            font-weight: 600;
        }}

        .sidebar-footer {{
            padding: 1.25rem;
            border-top: 1px solid var(--border-color);
            background: rgba(8, 11, 20, 0.5);
        }}

        .footer-metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.6rem;
            font-size: 0.75rem;
        }}

        .footer-label {{
            color: var(--text-secondary);
        }}

        .footer-val {{
            font-weight: 600;
            color: #ffffff;
        }}

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
            justify-content: flex-end;
            align-items: center;
            padding: 0 2rem;
            gap: 1.5rem;
            background: rgba(10, 14, 26, 0.4);
            backdrop-filter: blur(8px);
        }}

        .time-display {{
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .alert-bell {{
            position: relative;
            cursor: pointer;
            font-size: 1.1rem;
            color: var(--text-secondary);
            transition: color 0.2s ease;
        }}

        .alert-bell:hover {{
            color: #ffffff;
        }}

        .alert-badge {{
            position: absolute;
            top: -2px;
            right: -2px;
            width: 7px;
            height: 7px;
            background-color: var(--sell-color);
            border-radius: 50%;
        }}

        .view-content {{
            padding: 1.5rem 2rem 3rem 2rem;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .tab-view {{
            display: none;
            flex-direction: column;
            gap: 1.5rem;
            animation: viewFade 0.25s ease-out;
        }}

        .tab-view.active {{
            display: flex;
        }}

        @keyframes viewFade {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 1rem;
        }}

        @media (max-width: 1400px) {{
            .metrics-grid {{
                grid-template-columns: repeat(4, 1fr);
            }}
        }}

        @media (max-width: 1000px) {{
            .metrics-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        .widget-card {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
            transition: border-color 0.2s ease;
        }}

        .widget-card:hover {{
            border-color: rgba(255, 255, 255, 0.08);
        }}

        .widget-label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}

        .widget-value-row {{
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
        }}

        .widget-value {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
        }}

        .widget-trend {{
            font-size: 0.72rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.2rem;
        }}

        .trend-up {{ color: var(--buy-color); }}
        .trend-down {{ color: var(--sell-color); }}

        /* Sparkline Graphics */
        .graphic-container {{
            height: 25px;
            display: flex;
            align-items: flex-end;
        }}

        .sparkline {{
            stroke: var(--buy-color);
            stroke-width: 1.5;
            fill: none;
        }}

        /* Donut Win Rate Graphic */
        .donut-container {{
            width: 30px;
            height: 30px;
            transform: rotate(-90deg);
        }}

        .donut-ring {{
            fill: none;
            stroke: rgba(255, 255, 255, 0.05);
            stroke-width: 3.5;
        }}

        .donut-segment {{
            fill: none;
            stroke: #8b5cf6;
            stroke-dasharray: {win_rate} 100;
            stroke-linecap: round;
            stroke-width: 3.5;
        }}

        /* Main Workspace Split */
        .workspace-split {{
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 1.25rem;
            align-items: start;
        }}

        @media (max-width: 1100px) {{
            .workspace-split {{
                grid-template-columns: 1fr;
            }}
        }}

        .panel {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            padding-bottom: 0.75rem;
            margin-bottom: 1rem;
        }}

        .panel-title-container {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .panel-title {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
        }}

        /* Active Signal details styling */
        .active-signal-details {{
            display: flex;
            flex-direction: column;
            gap: 0.9rem;
        }}

        .active-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .symbol-pair {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .symbol-subtext {{
            font-size: 0.72rem;
            color: var(--text-secondary);
            margin-top: -0.1rem;
        }}

        .price-badge {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
            padding-bottom: 0.5rem;
        }}

        .metric-label {{
            color: var(--text-secondary);
        }}

        .metric-value {{
            font-weight: 600;
            color: #ffffff;
        }}

        .metric-value.val-tp1 {{ color: var(--buy-color); }}
        .metric-value.val-sl {{ color: var(--sell-color); }}

        .close-btn {{
            width: 100%;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.25);
            color: var(--sell-color);
            border-radius: 8px;
            padding: 0.75rem;
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 0.5rem;
        }}

        .close-btn:hover {{
            background: var(--sell-color);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
        }}

        /* TradingView Candlestick Chart Card styling */
        .chart-panel {{
            display: flex;
            flex-direction: column;
            height: 100%;
            min-height: 440px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

        /* Session colour strip */
        .session-strip {{
            display: flex;
            align-items: center;
            gap: 0;
            height: 6px;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 0 0.25rem 0;
            background: rgba(255,255,255,0.04);
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

        /* Session legend pills row */
        .session-legend {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
            flex-wrap: wrap;
            padding: 0.35rem 0.5rem;
            background: rgba(8, 11, 20, 0.6);
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 0.25rem;
        }}
        .session-pill {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            color: var(--text-secondary);
            padding: 0.2rem 0.55rem;
            border-radius: 20px;
            border: 1px solid transparent;
            transition: all 0.4s ease;
            cursor: default;
            user-select: none;
        }}
        .session-pill .pill-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            flex-shrink: 0;
            transition: box-shadow 0.4s ease;
        }}
        .session-pill.sess-active {{
            color: #fff;
            border-color: rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.04);
        }}
        .session-pill.sess-active .pill-dot {{
            animation: dotPulse 1.5s ease-in-out infinite;
        }}
        @keyframes dotPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.35); }}
        }}
        .session-pill .sess-time {{
            font-size: 0.58rem;
            font-weight: 400;
            opacity: 0.7;
        }}
        .sess-overlap-badge {{
            font-size: 0.58rem;
            background: linear-gradient(90deg, rgba(16,185,129,0.2), rgba(251,191,36,0.2));
            border: 1px solid rgba(255,255,255,0.1);
            color: #fbbf24;
            padding: 0.15rem 0.5rem;
            border-radius: 20px;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-left: auto;
        }}
        }}

        .chart-panel.full-screen-chart {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 99999 !important;
            background: #070913 !important;
            padding: 1.5rem !important;
            box-sizing: border-box !important;
            border-radius: 0 !important;
        }}

        .chart-panel.full-screen-chart .chart-wrapper,
        .chart-panel.full-screen-chart .chart-container-div {{
            height: calc(100vh - 100px) !important;
        }}

        .chart-panel.minimized-chart {{
            min-height: auto !important;
            height: auto !important;
        }}

        .chart-panel.minimized-chart .chart-wrapper {{
            display: none !important;
        }}

        .chart-control-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }}

        .chart-control-btn:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .chart-control-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

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

        .chart-container-div {{
            flex: 1;
            width: 100%;
            height: 380px;
            border-radius: 8px;
            background: #080b14;
            position: relative;
        }}

        .chart-wrapper {{
            position: relative;
            width: 100%;
            height: 380px;
            border-radius: 8px;
            overflow: hidden;
        }}

        #session-canvas, #vp-canvas {{
            position: absolute;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 2;
        }}

        /* Table Styling */
        .table-panel {{
            margin-top: 0.5rem;
        }}

        .table-container {{
            width: 100%;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.82rem;
        }}

        th {{
            color: var(--text-secondary);
            font-weight: 500;
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
        }}

        /* Badges */
        .badge {{
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            display: inline-block;
        }}

        .badge-buy {{ background: rgba(16, 185, 129, 0.12); color: var(--buy-color); border: 1px solid rgba(16, 185, 129, 0.15); }}
        .badge-sell {{ background: rgba(239, 68, 68, 0.12); color: var(--sell-color); border: 1px solid rgba(239, 68, 68, 0.15); }}
        
        .badge-success {{ background: rgba(16, 185, 129, 0.15); color: var(--buy-color); border: 1px solid rgba(16, 185, 129, 0.2); }}
        .badge-danger {{ background: rgba(239, 68, 68, 0.15); color: var(--sell-color); border: 1px solid rgba(239, 68, 68, 0.2); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.15); color: var(--warning-color); border: 1px solid rgba(245, 158, 11, 0.2); }}
        .badge-secondary {{ background: rgba(156, 163, 175, 0.15); color: var(--text-secondary); border: 1px solid rgba(156, 163, 175, 0.2); }}

        .text-buy {{ color: var(--buy-color); }}
        .text-sell {{ color: var(--sell-color); }}
        .font-bold {{ font-weight: 600; }}
        .small {{ font-size: 0.75rem; }}
        .text-muted {{ color: var(--text-secondary); }}

        /* Calendar tab custom styling */
        .calendar-container {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
        }}

        .calendar-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }}

        .calendar-title {{
            font-size: 1.15rem;
            color: #ffffff;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
        }}

        .calendar-btn {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .calendar-btn:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.12);
        }}

        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.45rem;
        }}

        .calendar-weekday {{
            text-align: center;
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-secondary);
            padding: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .calendar-cell {{
            aspect-ratio: 1.2;
            background: rgba(255, 255, 255, 0.005);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.45rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
            position: relative;
            min-height: 70px;
        }}

        .calendar-cell.empty {{
            background: transparent;
            border: none;
        }}

        .calendar-cell.has-trades {{
            background: rgba(59, 130, 246, 0.02);
            border-color: rgba(59, 130, 246, 0.1);
            cursor: pointer;
        }}

        .calendar-cell.has-trades:hover {{
            background: rgba(59, 130, 246, 0.06);
            border-color: rgba(59, 130, 246, 0.25);
            transform: translateY(-1px);
            z-index: 10;
        }}

        .cell-num {{
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-secondary);
        }}

        .cell-pnl {{
            font-size: 0.72rem;
            font-weight: 700;
            text-align: right;
        }}

        .cell-acc {{
            font-size: 0.58rem;
            color: var(--text-secondary);
            text-align: right;
        }}

        /* Side Drawer Overlay styling */
        .drawer-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            z-index: 999;
            display: none;
            opacity: 0;
            transition: opacity 0.2s ease;
        }}

        .drawer {{
            position: fixed;
            top: 0;
            right: -460px;
            width: 100%;
            max-width: 460px;
            height: 100vh;
            background: #0b0f19;
            border-left: 1px solid var(--border-color);
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
            z-index: 1000;
            transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            color: var(--text-primary);
        }}

        .drawer.open {{
            right: 0;
        }}

        .drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
            margin-bottom: 1.25rem;
        }}

        .drawer-title {{
            font-size: 1.15rem;
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
        }}

        .drawer-close {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.35rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }}

        .drawer-close:hover {{
            color: #ffffff;
        }}

        .drawer-content {{
            overflow-y: auto;
            flex: 1;
            padding-right: 0.25rem;
        }}

        .drawer-metric-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.85rem;
            margin-bottom: 1.25rem;
            display: flex;
            justify-content: space-between;
        }}

        .drawer-trade-card {{
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.85rem;
            margin-bottom: 0.75rem;
            position: relative;
        }}

        .drawer-trade-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.4rem;
        }}

        .drawer-trade-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.4rem;
            font-size: 0.75rem;
            color: var(--text-secondary);
            border-top: 1px dashed var(--border-color);
            padding-top: 0.4rem;
            margin-top: 0.4rem;
        }}

        .drawer-trade-val {{
            color: #ffffff;
            font-weight: 500;
        }}

        /* Spinner */
        .spinner {{
            width: 24px;
            height: 24px;
            border: 3px solid rgba(251, 191, 36, 0.1);
            border-top: 3px solid var(--accent-gold);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* Floating Chat Widget CSS */
        .chat-bubble-btn {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-gold) 0%, #d97706 100%);
            border: none;
            box-shadow: 0 4px 20px rgba(217, 119, 6, 0.4);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 1.5rem;
            z-index: 10000;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        .chat-bubble-btn:hover {{
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 8px 30px rgba(217, 119, 6, 0.6);
        }}

        .chat-bubble-btn:active {{
            transform: scale(0.95);
        }}

        .chat-widget-container {{
            position: fixed;
            bottom: 96px;
            right: 24px;
            width: 380px;
            height: 540px;
            max-height: calc(100vh - 140px);
            max-width: calc(100vw - 48px);
            background: rgba(10, 15, 30, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(251, 191, 36, 0.15); /* Premium gold tint border */
            border-radius: 16px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
            z-index: 10000;
            opacity: 0;
            transform: translateY(20px) scale(0.95);
            pointer-events: none;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }}

        .chat-widget-container.active {{
            opacity: 1;
            transform: translateY(0) scale(1);
            pointer-events: all;
        }}

        .chat-widget-header {{
            padding: 1rem 1.25rem;
            background: rgba(30, 41, 59, 0.4);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .chat-widget-header-title {{
            display: flex;
            flex-direction: column;
        }}

        .chat-widget-title {{
            font-size: 0.9rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .chat-widget-subtitle {{
            font-size: 0.7rem;
            color: var(--text-secondary);
            margin-top: 0.15rem;
        }}

        .chat-widget-close {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary);
            font-size: 0.85rem;
            cursor: pointer;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .chat-widget-close:hover {{
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.4);
            color: #ef4444;
            transform: rotate(90deg);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
        }}

        .chat-widget-messages {{
            flex: 1;
            padding: 1.25rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            scrollbar-width: thin;
            scrollbar-color: rgba(251, 191, 36, 0.2) transparent;
        }}

        .chat-widget-messages::-webkit-scrollbar {{
            width: 6px;
        }}

        .chat-widget-messages::-webkit-scrollbar-thumb {{
            background: rgba(251, 191, 36, 0.2);
            border-radius: 3px;
        }}

        .chat-widget-footer {{
            padding: 1rem 1.25rem;
            background: rgba(15, 23, 42, 0.6);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            align-items: center;
            gap: 0.6rem;
            box-sizing: border-box;
        }}

        .chat-widget-container.active + .chat-bubble-btn {{
            opacity: 0;
            pointer-events: none;
            transform: scale(0.8);
        }}

        /* Voice mic active keyframe animation */
        @keyframes micPulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5);
                background: rgba(239, 68, 68, 0.2);
                border-color: rgba(239, 68, 68, 0.4);
            }}
            70% {{
                box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
                background: rgba(239, 68, 68, 0.35);
                border-color: rgba(239, 68, 68, 0.6);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
                background: rgba(239, 68, 68, 0.2);
                border-color: rgba(239, 68, 68, 0.4);
            }}
        }}

        .mic-active {{
            animation: micPulse 1.5s infinite;
            color: #ef4444 !important;
        }}

        /* Economic Calendar styling */
        .calendar-tab-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 0.4rem 0.8rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border-bottom: 2px solid transparent;
            white-space: nowrap;
        }}

        .calendar-tab-btn:hover {{
            color: #ffffff;
        }}

        .calendar-tab-btn.active {{
            color: var(--accent-blue);
            border-bottom: 2px solid var(--accent-blue);
        }}

        .impact-filter-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary);
            padding: 0.35rem 0.7rem;
            border-radius: 8px;
            font-size: 0.72rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .impact-filter-btn:hover {{
            border-color: rgba(255,255,255,0.15);
            color: #ffffff;
        }}

        .impact-filter-btn.active#filter-impact-high {{
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.25);
            color: #ef4444;
        }}
        .impact-filter-btn.active#filter-impact-medium {{
            background: rgba(245, 158, 11, 0.1);
            border-color: rgba(245, 158, 11, 0.25);
            color: #fbbf24;
        }}
        .impact-filter-btn.active#filter-impact-low {{
            background: rgba(16, 185, 129, 0.1);
            border-color: rgba(16, 185, 129, 0.25);
            color: #10b981;
        }}

        .us-only-btn.active {{
            background: rgba(59, 130, 246, 0.1) !important;
            border-color: rgba(59, 130, 246, 0.25) !important;
            color: #3b82f6 !important;
        }}

        .news-card:hover {{
            background: rgba(255,255,255,0.02) !important;
            border-color: rgba(255,255,255,0.08) !important;
        }}

        /* Toast notification */
        .toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(16, 185, 129, 0.95);
            border: 1px solid rgba(16, 185, 129, 0.25);
            color: #ffffff;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            display: none;
            z-index: 2000;
            animation: slideUp 0.3s ease-out;
        }}
        @keyframes slideUp {{
            from {{ transform: translateY(100%) scale(0.9); opacity: 0; }}
            to {{ transform: translateY(0) scale(1); opacity: 1; }}
        }}
    </style>
    <!-- TradingView Lightweight Charts Library & TV Advanced Widget -->
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
</head>
<body>
    <!-- Sidebar Navigation -->
    <aside>
        <div class="sidebar-header">
            <h1 class="brand">⚜️ <span>XAUUSD</span> BOT</h1>
            <div class="live-status-container">
                <span class="live-badge">LIVE</span>
                <span class="pulse-dot {broker_pulse}"></span>
                <span class="connection-text">{broker_status}</span>
            </div>
        </div>
        
        <div class="sidebar-nav">
            <div class="nav-item active" id="nav-dashboard" onclick="switchTab('dashboard-view', this)">📊 Dashboard</div>
            <div class="nav-item" id="nav-trades" onclick="switchTab('trades-view', this)">📈 Live Trades</div>
            <div class="nav-item" id="nav-history" onclick="switchTab('history-view', this)">🗄️ Trade History</div>
            <div class="nav-item" id="nav-signals" onclick="switchTab('signals-view', this)">📡 Webhook Signals</div>
            <div class="nav-item" id="nav-calendar" onclick="switchTab('calendar-view', this)">📅 Trading Calendar</div>
            <div class="nav-item" id="nav-performance" onclick="switchTab('performance-view', this)">🏆 Performance</div>
            <div class="nav-item" id="nav-news" onclick="switchTab('news-view', this)">📰 Live News</div>
            <div class="nav-item" id="nav-settings" onclick="switchTab('settings-view', this)">⚙️ Settings</div>
            <a class="nav-item" id="nav-logout" href="/logout" style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 1rem;">🚪 Logout</a>
        </div>

        <div class="sidebar-footer">
            <div class="footer-metric">
                <span class="footer-label">Account Balance</span>
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
                <span class="footer-label">Margin Used</span>
                <span class="footer-val">{sidebar_margin_used_str}</span>
            </div>
            <div class="footer-metric">
                <span class="footer-label">Margin Level</span>
                <span class="footer-val">{sidebar_margin_level_str}</span>
            </div>
        </div>
    </aside>

    <!-- Main Container -->
    <main>
        <!-- Header -->
        <header>
            <div class="header-clocks" style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <div class="clock-box" id="clock-box-kol" onclick="setTimezonePreference('Asia/Kolkata')" title="Set dashboard timezone to Kolkata (IST)" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s ease;">
                    <span style="color: var(--accent-gold); font-weight: 600;">KOL</span>
                    <span id="clock-kol" style="font-family: monospace; color: #ffffff; font-weight: 500;">--:--:--</span>
                </div>
                <div class="clock-box" id="clock-box-utc" onclick="setTimezonePreference('UTC')" title="Set dashboard timezone to UTC" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s ease;">
                    <span style="color: var(--accent-gold); font-weight: 600;">UTC</span>
                    <span id="clock-utc" style="font-family: monospace; color: #ffffff; font-weight: 500;">--:--:--</span>
                </div>
                <div class="clock-box" id="clock-box-ny" onclick="setTimezonePreference('America/New_York')" title="Set dashboard timezone to New York" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s ease;">
                    <span style="color: var(--accent-gold); font-weight: 600;">NY</span>
                    <span id="clock-ny" style="font-family: monospace; color: #ffffff; font-weight: 500;">--:--:--</span>
                </div>
                <div class="clock-box" id="clock-box-ldn" onclick="setTimezonePreference('Europe/London')" title="Set dashboard timezone to London" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s ease;">
                    <span style="color: var(--accent-gold); font-weight: 600;">LDN</span>
                    <span id="clock-ldn" style="font-family: monospace; color: #ffffff; font-weight: 500;">--:--:--</span>
                </div>
                <div class="clock-box" id="clock-box-tok" onclick="setTimezonePreference('Asia/Tokyo')" title="Set dashboard timezone to Tokyo" style="background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s ease;">
                    <span style="color: var(--accent-gold); font-weight: 600;">TOK</span>
                    <span id="clock-tok" style="font-family: monospace; color: #ffffff; font-weight: 500;">--:--:--</span>
                </div>
            </div>
            <div class="alert-bell" style="margin-left: 1rem;">
                🔔
                <span class="alert-badge"></span>
            </div>
        </header>

        <!-- View Content Area -->
        <div class="view-content">
            
            <!-- 1. DASHBOARD VIEW (ACTIVE) -->
            <div id="dashboard-view" class="tab-view active">
                
                <!-- Metric widgets grid (Top metrics) -->
                <div class="metrics-grid">
                    <div class="widget-card">
                        <div class="widget-label">Total Balance</div>
                        <div class="widget-value-row">
                            <div class="widget-value">${sidebar_balance:,.2f}</div>
                            <div class="widget-trend trend-up">↑ 1.23% Today</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem;">
                            <!-- Sparkline path -->
                            <svg class="sparkline" viewBox="0 0 100 25" width="100%" height="25">
                                <path d="M0,20 Q10,12 20,18 T40,8 T60,15 T80,5 T100,10" fill="none" stroke="#10b981" stroke-width="1.5"></path>
                            </svg>
                        </div>
                    </div>

                    <div class="widget-card">
                        <div class="widget-label">Open Trades</div>
                        <div class="widget-value-row">
                            <div class="widget-value">{len(open_trades)}</div>
                            <div class="text-muted" style="font-size: 0.72rem;">0 Pending</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem; display: flex; gap: 4px; justify-content: flex-end;">
                            <span style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2); color: var(--accent-blue); padding: 0.15rem 0.35rem; border-radius: 4px; font-size: 0.65rem; font-weight: 600;">ACTIVE</span>
                        </div>
                    </div>

                    <div class="widget-card">
                        <div class="widget-label">Daily PNL</div>
                        <div class="widget-value-row">
                            <div class="widget-value" id="daily-pnl-val">${daily_pnl:+.2f}</div>
                            <div class="widget-trend trend-up">↑ 1.21%</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem;">
                            <svg class="sparkline" viewBox="0 0 100 25" width="100%" height="25">
                                <path d="M0,15 L20,18 L40,10 L60,20 L80,5 L100,8" fill="none" stroke="#10b981" stroke-width="1.5"></path>
                            </svg>
                        </div>
                    </div>

                    <div class="widget-card">
                        <div class="widget-label">Win Rate</div>
                        <div class="widget-value-row">
                            <div class="widget-value">{win_rate:.2f}%</div>
                            <div class="text-muted" style="font-size: 0.72rem;">({wins} / {total_trades})</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem; justify-content: flex-end;">
                            <div class="donut-container">
                                <svg viewBox="0 0 36 36" style="width: 100%; height: 100%;">
                                    <path class="donut-ring" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                    <path class="donut-segment" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"></path>
                                </svg>
                            </div>
                        </div>
                    </div>

                    <div class="widget-card">
                        <div class="widget-label">Risk Per Trade</div>
                        <div class="widget-value-row">
                            <div class="widget-value">{data.get('risk_percent_per_trade', 0.01)*100.0:.2f}%</div>
                            <div class="text-muted" style="font-size: 0.72rem;">Fixed Risk</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem; justify-content: flex-end; align-items: center;">
                            🛡️
                        </div>
                    </div>

                    <div class="widget-card" id="broker-connection-widget">
                        <div class="widget-label">Broker Connection</div>
                        <div class="widget-value-row">
                            <div class="widget-value" id="broker-conn-val" style="color: { 'var(--buy-color)' if broker_connected else 'var(--sell-color)' }; font-size: 1.05rem; display: flex; align-items: center; gap: 0.35rem;">
                                <span class="pulse-dot {broker_pulse}" style="width: 8px; height: 8px;"></span>
                                {broker_status}
                            </div>
                            <div class="text-muted" style="font-size: 0.65rem;">ID: {mt5_login} | {broker_mode}</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.65rem; color: var(--text-secondary);">
                            <span class="text-truncate" style="max-width: 90px;" title="{mt5_server}">{mt5_server}</span>
                            <button id="btn-reconnect-broker" onclick="reconnectBroker()" title="Reconnect to MT5 terminal"
                                style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.35); color: #10b981;
                                       border-radius: 6px; padding: 0.2rem 0.5rem; font-size: 0.65rem; font-weight: 700;
                                       cursor: pointer; display: flex; align-items: center; gap: 0.3rem; transition: all 0.2s;">
                                <span id="reconnect-icon">⚡</span> Reconnect
                            </button>
                        </div>
                    </div>

                    <div class="widget-card">
                        <div class="widget-label">Bot Status</div>
                        <div class="widget-value-row">
                            <div class="widget-value" style="color: var(--buy-color); font-size: 1.05rem;">RUNNING</div>
                            <div class="text-muted" style="font-size: 0.65rem;">All Systems Ok</div>
                        </div>
                        <div class="graphic-container" style="margin-top: 0.5rem; justify-content: flex-end; align-items: center;">
                            🤖
                        </div>
                    </div>
                </div>

                <!-- Session Indicators Timeline Panel -->
                <div class="panel" style="margin-top: 0.25rem; padding: 1rem 1.25rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <span class="panel-title" style="font-size: 0.75rem; letter-spacing: 0.05em; font-weight: 600;">🌍 Global Trading Sessions</span>
                        <span id="session-time-text" style="font-size: 0.72rem; color: var(--text-secondary); font-weight: 500;"></span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;" id="sessions-container">
                        <!-- Sydney Session Card -->
                        <div class="widget-card" id="session-card-sydney" style="padding: 0.75rem; border-color: var(--border-color); flex-direction: row; align-items: center; justify-content: space-between;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">Sydney</div>
                                <div style="font-size: 0.65rem; color: var(--text-secondary);" id="session-hours-sydney">22:00 - 07:00 UTC</div>
                            </div>
                            <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">
                                <span class="badge" id="session-badge-sydney" style="font-size: 0.55rem; padding: 0.1rem 0.35rem;">CLOSED</span>
                                <span style="font-size: 0.6rem; color: var(--text-secondary); margin-top: 0.15rem;" id="session-timer-sydney">—</span>
                            </div>
                        </div>
                        
                        <!-- Tokyo Session Card -->
                        <div class="widget-card" id="session-card-tokyo" style="padding: 0.75rem; border-color: var(--border-color); flex-direction: row; align-items: center; justify-content: space-between;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">Tokyo</div>
                                <div style="font-size: 0.65rem; color: var(--text-secondary);" id="session-hours-tokyo">00:00 - 09:00 UTC</div>
                            </div>
                            <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">
                                <span class="badge" id="session-badge-tokyo" style="font-size: 0.55rem; padding: 0.1rem 0.35rem;">CLOSED</span>
                                <span style="font-size: 0.6rem; color: var(--text-secondary); margin-top: 0.15rem;" id="session-timer-tokyo">—</span>
                            </div>
                        </div>

                        <!-- London Session Card -->
                        <div class="widget-card" id="session-card-london" style="padding: 0.75rem; border-color: var(--border-color); flex-direction: row; align-items: center; justify-content: space-between;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">London</div>
                                <div style="font-size: 0.65rem; color: var(--text-secondary);" id="session-hours-london">08:00 - 17:00 UTC</div>
                            </div>
                            <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">
                                <span class="badge" id="session-badge-london" style="font-size: 0.55rem; padding: 0.1rem 0.35rem;">CLOSED</span>
                                <span style="font-size: 0.6rem; color: var(--text-secondary); margin-top: 0.15rem;" id="session-timer-london">—</span>
                            </div>
                        </div>

                        <!-- New York Session Card -->
                        <div class="widget-card" id="session-card-newyork" style="padding: 0.75rem; border-color: var(--border-color); flex-direction: row; align-items: center; justify-content: space-between;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">New York</div>
                                <div style="font-size: 0.65rem; color: var(--text-secondary);" id="session-hours-newyork">13:00 - 22:00 UTC</div>
                            </div>
                            <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">
                                <span class="badge" id="session-badge-newyork" style="font-size: 0.55rem; padding: 0.1rem 0.35rem;">CLOSED</span>
                                <span style="font-size: 0.6rem; color: var(--text-secondary); margin-top: 0.15rem;" id="session-timer-newyork">—</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Visual overlap timeline progress bar -->
                    <div style="position: relative; height: 18px; background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); border-radius: 6px; margin-top: 1rem; overflow: hidden; display: flex;">
                        <!-- Timeline intervals -->
                        <div style="position: absolute; left: 0; top: 0; height: 100%; width: 100%; display: flex; justify-content: space-between; font-size: 0.58rem; color: var(--text-secondary); padding: 0 4px; pointer-events: none; align-items: center;">
                            <span>00h</span><span>04h</span><span>08h</span><span>12h</span><span>16h</span><span>20h</span><span>24h</span>
                        </div>
                        <!-- Sydney block (22h to 31h -> wraps to 0-7h and 22-24h) -->
                        <div style="position: absolute; left: 91.6%; width: 8.4%; height: 100%; background: rgba(59,130,246,0.06); border-left: 1px dashed rgba(59,130,246,0.15);"></div>
                        <div style="position: absolute; left: 0%; width: 29.1%; height: 100%; background: rgba(59,130,246,0.06); border-right: 1px dashed rgba(59,130,246,0.15);"></div>
                        
                        <!-- Tokyo block (0h to 9h) -->
                        <div style="position: absolute; left: 0%; width: 37.5%; height: 100%; background: rgba(139,92,246,0.06); border-right: 1px dashed rgba(139,92,246,0.15);"></div>
                        
                        <!-- London block (8h to 17h) -->
                        <div style="position: absolute; left: 33.3%; width: 37.5%; height: 100%; background: rgba(16,185,129,0.06); border-left: 1px dashed rgba(16,185,129,0.15); border-right: 1px dashed rgba(16,185,129,0.15);"></div>
                        
                        <!-- New York block (13h to 22h) -->
                        <div style="position: absolute; left: 54.1%; width: 37.5%; height: 100%; background: rgba(251,191,36,0.06); border-left: 1px dashed rgba(251,191,36,0.15); border-right: 1px dashed rgba(251,191,36,0.15);"></div>
                        
                        <!-- Current time marker -->
                        <div id="session-timeline-marker" style="position: absolute; top: 0; left: 0%; width: 3px; height: 100%; background: var(--sell-color); box-shadow: 0 0 8px var(--sell-color); transition: left 1s linear; z-index: 2;"></div>
                    </div>
                </div>

                <!-- Main Grid Layout (Active signal & Chart) -->
                <div class="workspace-split">
                    <!-- Left: Active signal/trade & Economic News -->
                    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                        <div class="panel">
                            <div class="panel-header">
                                <div class="panel-title-container">
                                    🔔 <span class="panel-title">Active Signal / Trade</span>
                                </div>
                                <span class="badge {"badge-success" if has_active else "badge-secondary"}" id="active-status-top-badge" style="font-size: 0.65rem;">{active_direction}</span>
                            </div>
                            
                            <div class="active-signal-details">
                                <div class="active-header-row">
                                    <div>
                                        <div class="symbol-pair" id="active-symbol-pair">{active_symbol}</div>
                                        <div class="symbol-subtext">Gold / US Dollar</div>
                                    </div>
                                    <div class="price-badge text-buy" id="live-symbol-price">
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
                                        <span class="metric-value small" id="active-trade-time" data-iso="{active_time_iso}">{active_time}</span>
                                    </div>
                                    <div class="metric-row" id="active-pnl-row" style="display: {"flex" if has_active else "none"};">
                                        <span class="metric-label">Floating PnL</span>
                                        <span class="metric-value font-bold" id="active-floating-pnl">$0.00</span>
                                    </div>
                                    <div class="metric-row">
                                        <span class="metric-label">Timeframe</span>
                                        <span class="metric-value" id="active-timeframe">M15</span>
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
                                        <span class="metric-label">Status</span>
                                        <span class="metric-value badge {"badge-success" if has_active else "badge-secondary"}" id="active-status-badge" style="padding: 0.15rem 0.45rem;">{active_status}</span>
                                    </div>
                                </div>
     
                                <div id="active-close-btn-container">
                                    {f'<button class="close-btn" id="btn-close-active-trade" onclick="closeActiveTrade({active_trade.ticket})">Close Trade</button>' if active_trade and active_trade.status == 'OPEN' else '<button class="close-btn" id="btn-close-active-trade" style="opacity: 0.5; cursor: not-allowed;" disabled>No Active Positions</button>'}
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
                                    <select id="pred-timeframe" style="background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-color); color: #ffffff; padding: 0.35rem 0.5rem; border-radius: 6px; font-size: 0.78rem; font-family: 'Outfit', sans-serif; cursor: pointer; outline: none; flex-grow: 1;">
                                        <option value="M1">M1 (1 Minute)</option>
                                        <option value="M5">M5 (5 Minutes)</option>
                                        <option value="M15" selected>M15 (15 Minutes)</option>
                                        <option value="M30">M30 (30 Minutes)</option>
                                        <option value="H1">H1 (1 Hour)</option>
                                        <option value="H4">H4 (4 Hours)</option>
                                        <option value="D1">D1 (Daily)</option>
                                    </select>
                                </div>
                                
                                <button id="btn-run-prediction" onclick="runAiPrediction()" style="background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); border: none; color: #060913; padding: 0.75rem; border-radius: 8px; font-family: 'Outfit', sans-serif; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(217,119,6,0.15);" onmouseover="this.style.filter='brightness(1.15)'" onmouseout="this.style.filter='none'">
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
                                </div>
                            </div>
                        </div>

                        <!-- Tasks Checklist panel -->
                        <div class="panel" style="padding: 1.25rem;">
                            <div class="panel-header" style="margin-bottom: 0.75rem; padding-bottom: 0.5rem;">
                                <div class="panel-title-container">
                                    📋 <span class="panel-title">Tasks & Memory Checklist</span>
                                </div>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; gap: 0.5rem;">
                                    <input type="text" id="new-task-input" placeholder="Add a new task..." style="flex-grow: 1; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.45rem 0.6rem; border-radius: 6px; font-size: 0.78rem; outline: none;" onkeydown="if(event.key === 'Enter') addDashboardTask()"/>
                                    <button onclick="addDashboardTask()" style="background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); border: none; color: #060913; padding: 0.45rem 0.75rem; border-radius: 6px; font-size: 0.78rem; font-weight: 600; cursor: pointer;">Add</button>
                                </div>
                                <div id="dashboard-tasks-list" style="display: flex; flex-direction: column; gap: 0.5rem; max-height: 200px; overflow-y: auto;">
                                    {tasks_html}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right: interactive candlestick chart & Economic Calendar -->
                    <div style="display: flex; flex-direction: column; gap: 1.25rem; width: 100%;">
                        <div class="panel chart-panel">
                            <div class="chart-controls-row">
                                <div class="tf-selector">
                                    <button class="tf-btn" id="btn-tf-m1" onclick="changeChartTimeframe('M1', this)">M1</button>
                                    <button class="tf-btn" id="btn-tf-m5" onclick="changeChartTimeframe('M5', this)">M5</button>
                                    <button class="tf-btn active" id="btn-tf-m15" onclick="changeChartTimeframe('M15', this)">M15</button>
                                    <button class="tf-btn" id="btn-tf-m30" onclick="changeChartTimeframe('M30', this)">M30</button>
                                    <button class="tf-btn" id="btn-tf-h1" onclick="changeChartTimeframe('H1', this)">H1</button>
                                    <button class="tf-btn" id="btn-tf-h4" onclick="changeChartTimeframe('H4', this)">H4</button>
                                    <button class="tf-btn" id="btn-tf-d1" onclick="changeChartTimeframe('D1', this)">D1</button>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <select class="indicators-dropdown">
                                        <option>Indicators (EMA, RSI)</option>
                                    </select>
                                    <button class="chart-control-btn" id="btn-chart-minimize" onclick="toggleMinimizeChart()" title="Minimize Chart">🗕 Minimize</button>
                                    <button class="chart-control-btn" id="btn-chart-fullscreen" onclick="toggleFullScreenChart()" title="Toggle Fullscreen">🗖 Fullscreen</button>
                                </div>
                            </div>

                            <!-- Live Session Colour Legend Strip -->
                            <div class="session-legend" id="session-legend-strip">
                                <!-- Sydney -->
                                <div class="session-pill" id="spill-sydney">
                                    <span class="pill-dot" style="background:#3b82f6;"></span>
                                    <span>Sydney</span>
                                    <span class="sess-time">22:00–07:00</span>
                                </div>
                                <!-- Tokyo -->
                                <div class="session-pill" id="spill-tokyo">
                                    <span class="pill-dot" style="background:#8b5cf6;"></span>
                                    <span>Tokyo</span>
                                    <span class="sess-time">00:00–09:00</span>
                                </div>
                                <!-- London -->
                                <div class="session-pill" id="spill-london">
                                    <span class="pill-dot" style="background:#10b981;"></span>
                                    <span>London</span>
                                    <span class="sess-time">08:00–17:00</span>
                                </div>
                                <!-- New York -->
                                <div class="session-pill" id="spill-newyork">
                                    <span class="pill-dot" style="background:#fbbf24;"></span>
                                    <span>New York</span>
                                    <span class="sess-time">13:00–22:00</span>
                                </div>
                                <!-- Overlap badge -->
                                <span class="sess-overlap-badge" id="sess-overlap-badge" style="display:none;">⚡ OVERLAP</span>
                                <!-- UTC clock -->
                                <span style="margin-left:auto;font-size:0.62rem;color:var(--text-secondary);font-family:monospace;" id="sess-utc-clock"></span>
                            </div>

                            <!-- Colour band strip (thin bar showing session zones proportionally) -->
                            <div class="session-strip" id="session-color-strip">
                                <div class="session-strip-segment" id="sstrip-sydney"  style="background:#3b82f6;opacity:0.25;"></div>
                                <div class="session-strip-segment" id="sstrip-tokyo"   style="background:#8b5cf6;opacity:0.25;"></div>
                                <div class="session-strip-segment" id="sstrip-london"  style="background:#10b981;opacity:0.25;"></div>
                                <div class="session-strip-segment" id="sstrip-newyork" style="background:#fbbf24;opacity:0.25;"></div>
                            </div>

                            <div class="chart-wrapper" id="chart-wrapper">
                                <div class="chart-container-div" id="tv-chart-container">
                                    <!-- TV Lightweight charts renders here -->
                                </div>
                                <!-- Session background canvas (drawn under candles) -->
                                <canvas id="session-canvas" style="width:100%;height:100%;"></canvas>
                            </div>
                        </div>

                        <!-- Economic Calendar news feed panel -->
                        <div class="panel" style="padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 16px;">
                            <div class="panel-header" style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 0.75rem; margin-bottom: 0;">
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <h2 class="panel-title" style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0;">
                                        📅 Economic Calendar
                                    </h2>
                                    <span style="font-size: 0.8rem; color: var(--text-secondary);">Track high-impact economic events and news that move the markets</span>
                                </div>
                                <button class="chart-control-btn" onclick="refreshEconomicCalendar(event)" title="Refresh Calendar Events" style="background: rgba(251, 191, 36, 0.08); border: 1px solid rgba(251, 191, 36, 0.15); color: var(--accent-gold); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 0.3rem; font-weight: 600;">
                                    🔄 Refresh
                                </button>
                            </div>

                            <!-- Live Timezone and Update indicator -->
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: var(--text-secondary); background: rgba(255, 255, 255, 0.01); padding: 0.5rem 0.75rem; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.03);">
                                <div style="display: flex; align-items: center; gap: 0.4rem;">
                                    📍 <span id="calendar-timezone-text">Kolkata GMT+5:30</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.4rem;">
                                    <span style="display: inline-block; width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981;"></span>
                                    <span style="font-weight: 600; color: #10b981; text-transform: uppercase; font-size: 0.65rem; letter-spacing: 0.05em;">LIVE</span>
                                    <span id="calendar-last-updated" style="font-family: monospace;">Updated 12:36:20</span>
                                </div>
                            </div>



                            <!-- Date Tabs -->
                            <div style="display: flex; gap: 0.25rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 0.5rem; overflow-x: auto;">
                                <button type="button" class="calendar-tab-btn active" onclick="switchCalendarTab('upcoming', this)">Upcoming</button>
                                <button type="button" class="calendar-tab-btn" onclick="switchCalendarTab('today', this)">Today</button>
                                <button type="button" class="calendar-tab-btn" onclick="switchCalendarTab('tomorrow', this)">Tomorrow</button>
                                <button type="button" class="calendar-tab-btn" onclick="switchCalendarTab('thisweek', this)">This Week</button>
                                <button type="button" class="calendar-tab-btn" onclick="switchCalendarTab('all', this)">All</button>
                            </div>

                            <!-- Filter & Search Controls Row -->
                            <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; justify-content: space-between; align-items: center;">
                                <!-- Impact Badges (Multiselect filters) -->
                                <div style="display: flex; gap: 0.4rem; align-items: center;">
                                    <button type="button" class="impact-filter-btn active" id="filter-impact-high" onclick="toggleImpactFilter('High')">🔴 High</button>
                                    <button type="button" class="impact-filter-btn active" id="filter-impact-medium" onclick="toggleImpactFilter('Medium')">🟡 Med</button>
                                    <button type="button" class="impact-filter-btn active" id="filter-impact-low" onclick="toggleImpactFilter('Low')">🟢 Low</button>
                                </div>

                                <!-- US Only & Search input -->
                                <div style="display: flex; gap: 0.5rem; align-items: center; flex-grow: 1; max-width: 320px;">
                                    <button type="button" class="us-only-btn" id="filter-us-only" onclick="toggleUsOnlyFilter()">
                                        🇺🇸 US Only
                                    </button>
                                    <div style="position: relative; flex-grow: 1;">
                                        <span style="position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); font-size: 0.8rem; color: var(--text-secondary);">🔍</span>
                                        <input type="text" id="calendar-search-input" oninput="filterCalendarEvents()" placeholder="Search events..." style="width: 100%; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255,255,255,0.08); color: #ffffff; padding: 0.45rem 0.75rem 0.45rem 1.8rem; border-radius: 8px; font-size: 0.78rem; outline: none; transition: border-color 0.2s;"/>
                                    </div>
                                </div>
                            </div>

                            <!-- Events Count & Container -->
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--text-secondary); margin-top: 0.25rem;">
                                <span id="calendar-events-count">0 Events</span>
                            </div>

                            <div id="news-list" style="display: flex; flex-direction: column; gap: 0.75rem; max-height: 480px; overflow-y: auto; padding-right: 2px;">
                                {news_html}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bottom: Recent trades table -->
                <div class="panel table-panel">
                    <div class="panel-header">
                        <div class="panel-title-container">
                            📊 <span class="panel-title">Recent Trades Log</span>
                        </div>
                        <a href="javascript:void(0)" onclick="goToTab('history-view')" style="color: var(--accent-gold); font-size: 0.75rem; text-decoration: none; font-weight: 500;">View All Trades</a>
                    </div>
                    
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Symbol</th>
                                    <th>Type</th>
                                    <th>Entry Price</th>
                                    <th>Stop Loss</th>
                                    <th>Take Profit</th>
                                    <th>Open Time (UTC)</th>
                                    <th>Close Time (UTC)</th>
                                    <th>Status</th>
                                    <th>PnL</th>
                                </tr>
                            </thead>
                            <tbody>
                                {trades_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- 2. LIVE TRADES VIEW (PLACEHOLDER & OPEN POSITIONS) -->
            <div id="trades-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Current Open Positions</span>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Ticket</th>
                                    <th>Symbol</th>
                                    <th>Direction</th>
                                    <th>Lots</th>
                                    <th>Entry Price</th>
                                    <th>Stop Loss</th>
                                    <th>Take Profit</th>
                                    <th>Created At</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {open_trades_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 3. TRADE HISTORY VIEW -->
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
                                    <th>Remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 4. WEBHOOK SIGNALS VIEW -->
            <div id="signals-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Ingested Webhook Signal Logs</span>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Timestamp (UTC)</th>
                                    <th>Symbol</th>
                                    <th>Direction</th>
                                    <th>Status</th>
                                    <th>Confluence Indicators</th>
                                    <th>Remarks / Reject Reason</th>
                                </tr>
                            </thead>
                            <tbody>
                                {signals_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 5. TRADING CALENDAR VIEW -->
            <div id="calendar-view" class="tab-view">
                <div class="calendar-container">
                    <div class="calendar-controls">
                        <h2 class="calendar-title" id="calendar-header-title">Calendar</h2>
                        <div>
                            <button class="calendar-btn" id="btn-calendar-prev" onclick="navigateMonth(-1)">&larr; Previous</button>
                            <button class="calendar-btn" id="btn-calendar-next" onclick="navigateMonth(1)">Next &rarr;</button>
                        </div>
                    </div>
                    <div class="calendar-grid" id="calendar-days-grid">
                        <!-- Javascript populates cells -->
                    </div>
                </div>
            </div>

            <!-- 6. PERFORMANCE VIEW -->
            <div id="performance-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Performance Report Details</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-top: 1rem;">
                        <div class="widget-card">
                            <div class="widget-label">Total Trades Closed</div>
                            <div class="widget-value">{total_trades}</div>
                        </div>
                        <div class="widget-card">
                            <div class="widget-label">Net Profit/Loss</div>
                            <div class="widget-value { 'text-buy' if net_pnl > 0 else 'text-sell' }">${net_pnl:+.2f}</div>
                        </div>
                        <div class="widget-card">
                            <div class="widget-label">Win Count / Loss Count</div>
                            <div class="widget-value">{wins} Wins / {total_trades - wins} Losses</div>
                        </div>
                        <div class="widget-card">
                            <div class="widget-label">Average Win / Loss</div>
                            <div class="widget-value">${stats.get('avg_win', 0.0):,.2f} Win / ${stats.get('avg_loss', 0.0):,.2f} Loss</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 7. LIVE NEWS VIEW -->
            <div id="news-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Live Forex & Gold Market News</span>
                    </div>
                    <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 1.25rem;">
                        Real-time global news headlines and market reports from Google News.
                    </div>
                    <div id="live-news-list" style="display: flex; flex-direction: column; gap: 0.85rem; max-height: calc(100vh - 220px); overflow-y: auto; padding-right: 4px;">
                        {live_news_html}
                    </div>
                </div>
            </div>



            <!-- 9. SETTINGS VIEW -->
            <div id="settings-view" class="tab-view">
                <div class="panel">
                    <div class="panel-header">
                        <span class="panel-title">Trading System Settings</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-top: 1rem;">
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

                <div class="panel" style="margin-top: 1.25rem;">
                    <div class="panel-header" style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">
                        <span class="panel-title">⚙️ Configure Broker & API Credentials</span>
                    </div>
                    
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <!-- MT5 settings -->
                        <div>
                            <h4 style="font-size: 0.85rem; font-weight: 600; color: var(--accent-gold); margin-bottom: 0.5rem;">MetaTrader 5 Account Settings</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem;">
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">MT5 Login</label>
                                    <input type="number" id="setting-mt5-login" value="{data.get('mt5_login', 0)}" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">MT5 Password</label>
                                    <input type="password" id="setting-mt5-password" value="{data.get('mt5_password', '')}" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">MT5 Server</label>
                                    <input type="text" id="setting-mt5-server" value="{data.get('mt5_server', '')}" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">Broker Mode</label>
                                    <select id="setting-mt5-mock" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none; cursor: pointer;">
                                        <option value="false" {"selected" if not data.get('mt5_mock') else ""}>Live Broker (AtlasFunded)</option>
                                        <option value="true" {"selected" if data.get('mt5_mock') else ""}>Mock Simulation Mode</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- API keys -->
                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem; margin-top: 0.5rem;">
                            <h4 style="font-size: 0.85rem; font-weight: 600; color: var(--accent-gold); margin-bottom: 0.5rem;">AI LLM Provider Keys</h4>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">Gemini API Key</label>
                                    <input type="password" id="setting-gemini-key" value="{data.get('gemini_api_key', '')}" placeholder="Paste Gemini API Key..." style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">OpenAI API Key</label>
                                    <input type="password" id="setting-openai-key" value="{data.get('openai_api_key', '')}" placeholder="Paste OpenAI API Key..." style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                                <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                    <label style="font-size: 0.72rem; color: var(--text-secondary);">Claude (Anthropic) API Key</label>
                                    <input type="password" id="setting-claude-key" value="{data.get('claude_api_key', '')}" placeholder="Paste Claude API Key..." style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); color: #ffffff; padding: 0.5rem; border-radius: 6px; font-size: 0.78rem; outline: none;"/>
                                </div>
                            </div>
                        </div>

                        <!-- Save button -->
                        <div style="display: flex; justify-content: flex-end; margin-top: 0.5rem;">
                            <button id="btn-save-settings" onclick="saveSystemSettings()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border: none; color: #ffffff; padding: 0.6rem 1.5rem; border-radius: 6px; font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.filter='brightness(1.15)'" onmouseout="this.style.filter='none'">
                                Save Configuration & Reconnect
                            </button>
                        </div>
                    </div>
                </div>

                <div class="panel" style="margin-top: 1.25rem;">
                    <div class="panel-header">
                        <span class="panel-title">Database & History Maintenance</span>
                    </div>
                    <p style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 1.25rem; line-height: 1.4;">
                        Synchronize your local trade history database with your broker account state. Clearing history deletes local logs and triggers a clean re-sync of past orders from the MT5 terminal.
                    </p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <button id="btn-clear-history" onclick="clearHistoryAndSync()" style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); color: var(--sell-color); padding: 0.75rem; border-radius: 8px; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.2)'" onmouseout="this.style.background='rgba(239,68,68,0.08)'">
                            🧹 Clear History & Re-Sync
                        </button>
                        <button id="btn-reset-pnl" onclick="resetDailyPnL()" style="background: rgba(251, 191, 36, 0.08); border: 1px solid rgba(251, 191, 36, 0.2); color: var(--accent-gold); padding: 0.75rem; border-radius: 8px; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(251,191,36,0.2)'" onmouseout="this.style.background='rgba(251,191,36,0.08)'">
                            🔄 Reset Daily PNL
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </main>

    <!-- Trade Detail Side Drawer Overlay (Calendar view clicks) -->
    <div class="drawer-backdrop" id="drawer-bg" onclick="closeTradeDrawer()"></div>
    <div class="drawer" id="trade-drawer">
        <div class="drawer-header">
            <h3 class="drawer-title" id="drawer-date-title">Trades on Date</h3>
            <button class="drawer-close" onclick="closeTradeDrawer()">&times;</button>
        </div>
        <div class="drawer-content">
            <div class="drawer-metric-card">
                <div>
                    <div class="widget-label" style="margin-bottom: 0.25rem;">Net Profit/Loss</div>
                    <div class="widget-value" id="drawer-day-profit">$0.00</div>
                </div>
                <div style="text-align: right;">
                    <div class="widget-label" style="margin-bottom: 0.25rem;">Accuracy</div>
                    <div class="widget-value" id="drawer-day-accuracy">0%</div>
                </div>
            </div>
            <div id="drawer-trades-list">
                <!-- Javascript populates cards -->
            </div>
        </div>
    </div>

    <!-- Floating Chat Widget Bubble and Container -->
    <div class="chat-widget-container" id="chat-widget">
        <div class="chat-widget-header">
            <div class="chat-widget-header-title">
                <span class="chat-widget-title">💬 AI Chat Assistant</span>
                <span class="chat-widget-subtitle">Powered by Claude, OpenAI, or Gemini</span>
            </div>
            <button class="chat-widget-close" onclick="toggleChatWidget()" title="Close Chat">✕</button>
        </div>
        <div class="chat-widget-messages" id="chat-messages">
            {chat_html}
        </div>
        <div class="chat-widget-footer">
            <input type="text" id="chat-input" placeholder="Type your message here..." style="flex-grow: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255, 255, 255, 0.08); color: #ffffff; padding: 0.6rem 0.85rem; border-radius: 8px; font-family: 'Outfit', sans-serif; font-size: 0.82rem; outline: none;" onkeydown="if(event.key === 'Enter') sendChatMessage()"/>
            <button id="btn-voice-chat" onclick="toggleVoiceTyping()" style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: var(--text-secondary); padding: 0.6rem 0.8rem; border-radius: 8px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; font-size: 1rem;" onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(255,255,255,0.04)'" title="Voice Typing">🎙️</button>
            <button id="btn-send-chat" onclick="sendChatMessage()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border: none; color: #ffffff; padding: 0.6rem 1.2rem; border-radius: 8px; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.filter='brightness(1.1)'" onmouseout="this.style.filter='none'">Send</button>
        </div>
    </div>
    <button class="chat-bubble-btn" id="chat-toggle-btn" onclick="toggleChatWidget()">💬</button>

    <!-- Client-side trades database JSON injection -->
    <script id="all-trades-data" type="application/json">
        {trades_json_str}
    </script>
    <script id="all-news-events-data" type="application/json">
        {news_events_json_str}
    </script>

    <script>
        // Economic Calendar State
        let activeCalendarTab = 'upcoming';
        let activeImpactFilters = {{ High: true, Medium: true, Low: true }};
        let usOnlyFilter = false;

        function toggleNewsAccordion(el) {{
            const card = el.closest('.news-card');
            if (!card) return;
            const content = card.querySelector('.news-accordion-content');
            const svg = card.querySelector('svg');
            if (content) {{
                if (content.style.display === 'none') {{
                    content.style.display = 'block';
                    if (svg) svg.style.transform = 'rotate(180deg)';
                }} else {{
                    content.style.display = 'none';
                    if (svg) svg.style.transform = 'rotate(0deg)';
                }}
            }}
        }}

        function switchCalendarTab(tabId, el) {{
            activeCalendarTab = tabId;
            const tabBtns = document.querySelectorAll('.calendar-tab-btn');
            tabBtns.forEach(btn => btn.classList.remove('active'));
            el.classList.add('active');
            filterCalendarEvents();
        }}

        function toggleImpactFilter(impact) {{
            activeImpactFilters[impact] = !activeImpactFilters[impact];
            const btn = document.getElementById('filter-impact-' + impact.toLowerCase());
            if (btn) {{
                if (activeImpactFilters[impact]) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }}
            filterCalendarEvents();
        }}

        function toggleUsOnlyFilter() {{
            usOnlyFilter = !usOnlyFilter;
            const btn = document.getElementById('filter-us-only');
            if (btn) {{
                if (usOnlyFilter) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }}
            filterCalendarEvents();
        }}

        function getYearMonthDayString(date, timezone) {{
            const options = {{ year: 'numeric', month: '2-digit', day: '2-digit' }};
            if (timezone !== 'local' && timezone !== '') options.timeZone = timezone;
            try {{
                const parts = new Intl.DateTimeFormat('en-US', options).formatToParts(date);
                const y = parts.find(p => p.type === 'year').value;
                const m = parts.find(p => p.type === 'month').value;
                const d = parts.find(p => p.type === 'day').value;
                return `${{m}}-${{d}}-${{y}}`;
            }} catch(e) {{
                const y = date.getUTCFullYear();
                const m = String(date.getUTCMonth() + 1).padStart(2, '0');
                const d = String(date.getUTCDate()).padStart(2, '0');
                return `${{m}}-${{d}}-${{y}}`;
            }}
        }}

        function filterCalendarEvents() {{
            const tz = getTimezonePreference();
            const tzName = tz === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : tz;
            
            const now = new Date();
            const todayStr = getYearMonthDayString(now, tzName);
            const tomorrowStr = getYearMonthDayString(new Date(now.getTime() + 86400000), tzName);
            
            const searchInput = document.getElementById('calendar-search-input');
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            
            const cards = document.querySelectorAll('.news-card');
            let visibleCount = 0;
            
            cards.forEach(card => {{
                const date = card.getAttribute('data-date');
                const country = card.getAttribute('data-country');
                const impact = card.getAttribute('data-impact');
                const iso = card.getAttribute('data-iso');
                const title = card.getAttribute('data-title');
                
                let matchesTab = false;
                const eventTime = iso ? new Date(iso) : null;
                
                if (activeCalendarTab === 'all') {{
                    matchesTab = true;
                }} else if (activeCalendarTab === 'upcoming') {{
                    matchesTab = eventTime ? (eventTime.getTime() > now.getTime()) : true;
                }} else if (activeCalendarTab === 'today') {{
                    matchesTab = (date === todayStr);
                }} else if (activeCalendarTab === 'tomorrow') {{
                    matchesTab = (date === tomorrowStr);
                }} else if (activeCalendarTab === 'thisweek') {{
                    if (eventTime) {{
                        const diffTime = eventTime.getTime() - now.getTime();
                        const diffDays = diffTime / (1000 * 60 * 60 * 24);
                        matchesTab = (diffDays >= 0 && diffDays <= 7);
                    }} else {{
                        matchesTab = true;
                    }}
                }}
                
                const matchesImpact = activeImpactFilters[impact];
                const matchesUsOnly = !usOnlyFilter || (country === 'USD');
                const matchesSearch = !query || title.includes(query);
                
                if (matchesTab && matchesImpact && matchesUsOnly && matchesSearch) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            const countEl = document.getElementById('calendar-events-count');
            if (countEl) {{
                countEl.textContent = `${{visibleCount}} Events`;
            }}
            
            updateCalendarTimezoneText();
        }}

        function updateCalendarTimecounts() {{
            const now = new Date();
            const countdownContainers = document.querySelectorAll('.news-countdown-container');
            
            countdownContainers.forEach(container => {{
                const card = container.closest('.news-card');
                if (!card) return;
                const iso = card.getAttribute('data-iso');
                if (!iso) return;
                
                const eventTime = new Date(iso);
                
                if (eventTime.getTime() > now.getTime()) {{
                    const diffMs = eventTime.getTime() - now.getTime();
                    const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
                    const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
                    
                    let timeText = '';
                    if (diffHrs > 0) {{
                        timeText = `${{diffHrs}}h ${{diffMins}}m left`;
                    }} else {{
                        timeText = `${{diffMins}}m left`;
                    }}
                    container.innerHTML = `ACTUAL <strong class="news-actual-val" style="color: #fbbf24; background: rgba(251,191,36,0.1); padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.68rem; margin-left: 0.2rem;">${{timeText}}</strong>`;
                }} else {{
                    const statsRow = container.closest('.news-stats-row');
                    let forecastText = '—';
                    if (statsRow) {{
                        const forecastEl = statsRow.querySelector('span:nth-child(2) strong');
                        forecastText = forecastEl ? forecastEl.textContent : '—';
                    }}
                    let actualVal = '—';
                    if (forecastText && forecastText !== '—') {{
                        actualVal = forecastText; 
                    }}
                    
                    const diffMs = now.getTime() - eventTime.getTime();
                    const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
                    const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
                    let timeAgoText = '';
                    if (diffHrs > 0) {{
                        timeAgoText = `${{diffHrs}}h ${{diffMins}}m ago`;
                    }} else {{
                        timeAgoText = `${{diffMins}}m ago`;
                    }}
                    
                    container.innerHTML = `ACTUAL <strong class="news-actual-val" style="color: #10b981;">${{actualVal}}</strong> <span style="font-size: 0.65rem; color: var(--text-secondary); margin-left: 0.3rem;">(${{timeAgoText}})</span>`;
                }}
            }});
            
            const updatedEl = document.getElementById('calendar-last-updated');
            if (updatedEl) {{
                const formatter = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }});
                updatedEl.textContent = `Updated ${{formatter.format(now)}}`;
            }}
        }}
        
        function updateCalendarTimezoneText() {{
            const tz = getTimezonePreference();
            const tzName = tz === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : tz;
            try {{
                const now = new Date();
                const tzString = new Intl.DateTimeFormat('en-US', {{ timeZoneName: 'longOffset', timeZone: tzName }}).format(now);
                const offsetMatch = tzString.match(/GMT[+-]\\d+(:\\d+)?/);
                const offset = offsetMatch ? offsetMatch[0] : 'GMT+0';
                const displayCity = tzName.split('/').pop().replace('_', ' ');
                const tzTextEl = document.getElementById('calendar-timezone-text');
                if (tzTextEl) {{
                    tzTextEl.textContent = `${{displayCity}} ${{offset}}`;
                }}
            }} catch (e) {{
                console.error("Error setting timezone text: ", e);
            }}
        }}

        function renderNewsEventHtml(event) {{
            const flags = {{
                "USD": "🇺🇸",
                "EUR": "🇪🇺",
                "GBP": "🇬🇧",
                "CAD": "🇨🇦",
                "AUD": "🇦🇺",
                "JPY": "🇯🇵",
                "NZD": "🇳🇿",
                "CHF": "🇨🇭",
                "CNY": "🇨🇳"
            }};
            const impact = event.impact || 'Low';
            let impactClass = 'badge-secondary';
            let impactBadgeText = '🟢 LOW';
            if (impact === 'High') {{
                impactClass = 'badge-danger';
                impactBadgeText = '🔴 HIGH';
            }} else if (impact === 'Medium') {{
                impactClass = 'badge-warning';
                impactBadgeText = '🟡 MED';
            }}
            
            const currency = event.country || 'USD';
            const flag = flags[currency] || '🌐';
            const timeStr = event.time || '—';
            const titleEscaped = escapeHtml(event.title || '—');
            const forecastEscaped = escapeHtml(event.forecast || '—');
            const prevEscaped = escapeHtml(event.previous || '—');
            const isoTime = event.iso_time || '';
            const dateStr = event.date || '';
            
            return `
                <div class="news-card" 
                     data-date="${{dateStr}}"
                     data-country="${{currency}}"
                     data-impact="${{impact}}"
                     data-iso="${{isoTime}}"
                     data-title="${{titleEscaped.toLowerCase()}}"
                     style="background: rgba(13, 18, 33, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1rem; display: flex; flex-direction: column; gap: 0.6rem; transition: all 0.2s; position: relative;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.6rem;">
                            <span style="font-family: monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-secondary);">${{timeStr}}</span>
                            <span style="font-size: 1.1rem; line-height: 1;">${{flag}}</span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: #ffffff;">${{currency}}</span>
                            <span class="impact-pill ${{impactClass}}" style="font-size: 0.62rem; padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">${{impactBadgeText}}</span>
                        </div>
                        <div style="color: var(--text-secondary); cursor: pointer;" onclick="toggleNewsAccordion(this)">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/></svg>
                        </div>
                    </div>
                    
                    <div style="font-size: 0.9rem; font-weight: 600; color: #ffffff; display: flex; align-items: center; gap: 0.4rem; cursor: pointer;" onclick="toggleNewsAccordion(this.parentElement.querySelector('svg').parentElement)">
                        ${{titleEscaped}}
                        <span class="ai-badge" style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); color: #3b82f6; font-size: 0.55rem; padding: 0.05rem 0.25rem; border-radius: 4px; font-weight: 700; letter-spacing: 0.05em; display: inline-flex; align-items: center; gap: 0.1rem;">✨ AI READY</span>
                    </div>
                    
                    <div class="news-stats-row" style="display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.72rem; color: var(--text-secondary); border-top: 1px dashed rgba(255,255,255,0.05); padding-top: 0.5rem; margin-top: 0.2rem;">
                        <span class="news-countdown-container" data-iso="${{isoTime}}">ACTUAL <strong class="news-actual-val" style="color: #ffffff;">—</strong></span>
                        <span>FORECAST <strong style="color: #ffffff;">${{forecastEscaped}}</strong></span>
                        <span>PREVIOUS <strong style="color: #ffffff;">${{prevEscaped}}</strong></span>
                    </div>
                    
                    <div class="news-accordion-content" style="display: none; font-size: 0.75rem; color: var(--text-secondary); line-height: 1.4; background: rgba(0,0,0,0.15); border-radius: 6px; padding: 0.5rem 0.75rem; margin-top: 0.3rem;">
                        <strong>Event Description:</strong> This event measures changes in the inflation or value of this financial indicator. Higher readings are generally bullish for the underlying currency.
                    </div>
                </div>
            `;
        }}

        // Tab switching engine
        function switchTab(tabId, el) {{
            // Hide all tab views
            const views = document.querySelectorAll('.tab-view');
            views.forEach(v => v.classList.remove('active'));
            
            // Show target view
            const targetView = document.getElementById(tabId);
            if (targetView) {{
                targetView.classList.add('active');
            }}
            
            // Update active sidebar nav button style
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => item.classList.remove('active'));
            if (el) {{
                el.classList.add('active');
            }}
        }}

        function toggleChatWidget() {{
            const widget = document.getElementById('chat-widget');
            if (widget) {{
                widget.classList.toggle('active');
                if (widget.classList.contains('active')) {{
                    const messagesContainer = document.getElementById('chat-messages');
                    if (messagesContainer) {{
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    }}
                    const chatInput = document.getElementById('chat-input');
                    if (chatInput) chatInput.focus();
                }}
            }}
        }}

        function goToTab(tabId) {{
            const navItems = document.querySelectorAll('.nav-item');
            let matchedEl = null;
            if (tabId === 'history-view') {{
                matchedEl = Array.from(navItems).find(i => i.textContent.includes('History'));
            }}
            switchTab(tabId, matchedEl);
        }}

        // Timezone Preference Manager
        function getTimezonePreference() {{
            return localStorage.getItem('dashboard_timezone') || 'Asia/Kolkata';
        }}

        function setTimezonePreference(tz) {{
            localStorage.setItem('dashboard_timezone', tz);
            applyTimezoneFormatting();
            updateSessions();
            if (typeof renderCalendar === 'function') {{
                renderCalendar(currentYear, currentMonth);
            }}
        }}

        function formatDateTime(isoString, timeZoneSetting) {{
            if (!isoString) return '—';
            try {{
                const date = new Date(isoString);
                let options = {{
                    year: 'numeric', month: '2-digit', day: '2-digit',
                    hour: '2-digit', minute: '2-digit', second: '2-digit',
                    hour12: false
                }};
                if (timeZoneSetting !== 'local') {{
                    options.timeZone = timeZoneSetting;
                }}
                return new Intl.DateTimeFormat('en-US', options).format(date);
            }} catch (e) {{
                console.error("Error formatting date: ", isoString, e);
                return isoString;
            }}
        }}

        function formatEventTime(isoString, etTime, timeZoneSetting) {{
            if (!etTime) return '—';
            const lowerTime = etTime.toLowerCase();
            if (lowerTime.includes('day') || lowerTime.includes('tentative') || lowerTime.includes('tba') || lowerTime.includes('tent')) {{
                return etTime;
            }}
            if (!isoString) return etTime;
            try {{
                const date = new Date(isoString);
                let options = {{
                    hour: '2-digit', minute: '2-digit',
                    hour12: false
                }};
                if (timeZoneSetting !== 'local' && timeZoneSetting !== 'UTC' && timeZoneSetting !== '') {{
                    options.timeZone = timeZoneSetting;
                }} else if (timeZoneSetting === 'UTC') {{
                    options.timeZone = 'UTC';
                }}
                return new Intl.DateTimeFormat('en-US', options).format(date);
            }} catch (e) {{
                console.error("Error formatting news time: ", isoString, e);
                return etTime;
            }}
        }}

        function applyTimezoneFormatting() {{
            const tz = getTimezonePreference();
            
            // Remove active style from all clock boxes
            const clockBoxes = document.querySelectorAll('.clock-box');
            clockBoxes.forEach(box => {{
                box.style.borderColor = 'var(--border-color)';
                box.style.background = 'rgba(255, 255, 255, 0.02)';
                box.style.boxShadow = 'none';
            }});
            
            // Highlight selected clock box
            let activeBoxId = '';
            if (tz === 'UTC') activeBoxId = 'clock-box-utc';
            else if (tz === 'America/New_York') activeBoxId = 'clock-box-ny';
            else if (tz === 'Europe/London') activeBoxId = 'clock-box-ldn';
            else if (tz === 'Asia/Tokyo') activeBoxId = 'clock-box-tok';
            else if (tz === 'Asia/Kolkata') activeBoxId = 'clock-box-kol';
            
            const activeBox = document.getElementById(activeBoxId);
            if (activeBox) {{
                activeBox.style.borderColor = 'var(--accent-gold)';
                activeBox.style.background = 'rgba(251, 191, 36, 0.05)';
                activeBox.style.boxShadow = '0 0 12px rgba(251, 191, 36, 0.15)';
            }}
            
            const elements = document.querySelectorAll('.time-cell');
            elements.forEach(el => {{
                const iso = el.getAttribute('data-iso');
                if (iso) {{
                    el.textContent = formatDateTime(iso, tz);
                }}
            }});
            
            const activeEl = document.getElementById('active-trade-time');
            if (activeEl) {{
                const raw = activeEl.getAttribute('data-iso');
                if (raw) {{
                    activeEl.textContent = formatDateTime(raw, tz);
                }}
            }}

            const newsTimeCells = document.querySelectorAll('.news-time-cell');
            newsTimeCells.forEach(el => {{
                const iso = el.getAttribute('data-iso');
                const et = el.getAttribute('data-et-time');
                el.textContent = formatEventTime(iso, et, tz);
            }});
        }}

        // Header Clock
        function updateClock() {{
            const now = new Date();
            
            const formatterKOL = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' }});
            const formatterUTC = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' }});
            const formatterNY = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'America/New_York' }});
            const formatterLDN = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'Europe/London' }});
            const formatterTOK = new Intl.DateTimeFormat('en-US', {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'Asia/Tokyo' }});
            
            const clockKol = document.getElementById('clock-kol');
            const clockUtc = document.getElementById('clock-utc');
            const clockNy = document.getElementById('clock-ny');
            const clockLdn = document.getElementById('clock-ldn');
            const clockTok = document.getElementById('clock-tok');
            
            if (clockKol) clockKol.textContent = formatterKOL.format(now);
            if (clockUtc) clockUtc.textContent = formatterUTC.format(now);
            if (clockNy) clockNy.textContent = formatterNY.format(now);
            if (clockLdn) clockLdn.textContent = formatterLDN.format(now);
            if (clockTok) clockTok.textContent = formatterTOK.format(now);
            
            // Also trigger session timeline marker movement and card states on every clock tick
            updateSessions();
            if (typeof updateCalendarTimecounts === 'function') {{
                updateCalendarTimecounts();
            }}
        }}
        setInterval(updateClock, 1000);
        
        // Session Indicators Calculator
        function updateSessions() {{
            const now = new Date();
            const currentUTC = now.getUTCHours() + (now.getUTCMinutes() / 60) + (now.getUTCSeconds() / 3600);
            const tz = getTimezonePreference();
            
            const sessionTimeText = document.getElementById('session-time-text');
            if (sessionTimeText) {{
                let options = {{ hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }};
                if (tz !== 'local') options.timeZone = tz;
                sessionTimeText.textContent = 'Current time: ' + new Intl.DateTimeFormat('en-US', options).format(now) + ' (' + (tz === 'local' ? 'Local' : tz.split('/').pop().replace('_', ' ')) + ')';
            }}
            
            const marker = document.getElementById('session-timeline-marker');
            if (marker) {{
                const markerPos = (currentUTC / 24) * 100;
                marker.style.left = markerPos + '%';
            }}
            
            const sessions = [
                {{ name: 'sydney', start: 22, end: 7, color: 'rgba(59, 130, 246, 0.4)', text: '#60a5fa', badgeBg: 'rgba(59, 130, 246, 0.15)' }},
                {{ name: 'tokyo', start: 0, end: 9, color: 'rgba(139, 92, 246, 0.4)', text: '#a78bfa', badgeBg: 'rgba(139, 92, 246, 0.15)' }},
                {{ name: 'london', start: 8, end: 17, color: 'rgba(16, 185, 129, 0.4)', text: '#34d399', badgeBg: 'rgba(16, 185, 129, 0.15)' }},
                {{ name: 'newyork', start: 13, end: 22, color: 'rgba(251, 191, 36, 0.4)', text: '#fcd34d', badgeBg: 'rgba(251, 191, 36, 0.15)' }}
            ];
            
            sessions.forEach(sess => {{
                let isActive = false;
                if (sess.start < sess.end) {{
                    isActive = (currentUTC >= sess.start && currentUTC < sess.end);
                }} else {{
                    isActive = (currentUTC >= sess.start || currentUTC < sess.end);
                }}
                
                const card = document.getElementById('session-card-' + sess.name);
                const badge = document.getElementById('session-badge-' + sess.name);
                const timer = document.getElementById('session-timer-' + sess.name);
                const hoursEl = document.getElementById('session-hours-' + sess.name);
                
                if (card && badge && timer) {{
                    if (isActive) {{
                        card.style.borderColor = sess.color;
                        badge.className = 'badge';
                        badge.style.background = sess.badgeBg;
                        badge.style.color = sess.text;
                        badge.style.borderColor = sess.color;
                        badge.style.border = `1px solid ${{sess.color}}`;
                        badge.textContent = 'ACTIVE';
                        
                        let remaining;
                        if (sess.start < sess.end) {{
                            remaining = sess.end - currentUTC;
                        }} else {{
                            remaining = (currentUTC >= sess.start) ? (24 - currentUTC + sess.end) : (sess.end - currentUTC);
                        }}
                        const remH = Math.floor(remaining);
                        const remM = Math.floor((remaining - remH) * 60);
                        timer.textContent = `Closes in ${{remH}}h ${{remM}}m`;
                        timer.style.color = sess.text;
                    }} else {{
                        card.style.borderColor = 'var(--border-color)';
                        badge.className = 'badge badge-secondary';
                        badge.style.background = '';
                        badge.style.color = '';
                        badge.style.borderColor = '';
                        badge.style.border = '';
                        badge.textContent = 'CLOSED';
                        
                        let until;
                        if (sess.start < sess.end) {{
                            until = (currentUTC < sess.start) ? (sess.start - currentUTC) : (24 - currentUTC + sess.start);
                        }} else {{
                            until = (currentUTC >= sess.end && currentUTC < sess.start) ? (sess.start - currentUTC) : 0;
                        }}
                        const untH = Math.floor(until);
                        const untM = Math.floor((until - untH) * 60);
                        timer.textContent = `Opens in ${{untH}}h ${{untM}}m`;
                        timer.style.color = 'var(--text-secondary)';
                    }}
                }}
                
                if (hoursEl) {{
                    hoursEl.textContent = formatSessionHours(sess.start, sess.end, tz);
                }}
            }});
        }}

        function formatSessionHours(startUTC, endUTC, timezone) {{
            const today = new Date();
            const startDate = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate(), startUTC, 0, 0));
            const endDate = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate(), endUTC, 0, 0));
            
            let options = {{ hour: '2-digit', minute: '2-digit', hour12: false }};
            if (timezone !== 'local') {{
                options.timeZone = timezone;
            }}
            
            const startStr = new Intl.DateTimeFormat('en-US', options).format(startDate);
            const endStr = new Intl.DateTimeFormat('en-US', options).format(endDate);
            
            return `${{startStr}} - ${{endStr}}`;
        }}

        // Close trade api handler
        function closeActiveTrade(ticketId) {{
            if (!confirm("Are you sure you want to close position #" + ticketId + "?")) return;
            
            fetch('/api/v1/close-trade?ticket=' + ticketId, {{
                method: 'POST'
            }}).then(res => res.json())
              .then(data => {{
                  alert("Position close request sent. Response: " + (data.message || data.detail || JSON.stringify(data)));
                  window.location.reload();
              }})
              .catch(err => {{
                  console.error(err);
                  alert("Failed to dispatch close action.");
              }});
        }}

        function clearHistoryAndSync() {{
            if (!confirm("Are you sure you want to purge all local signals/trades history and re-synchronize clean from your broker account? This will reload the page.")) return;
            
            const btn = document.getElementById("btn-clear-history");
            if (btn) {{
                btn.disabled = true;
                btn.textContent = "🧹 Clearing & Syncing...";
            }}
            
            fetch('/api/v1/maintenance/clear-history', {{
                method: 'POST'
            }}).then(res => res.json())
              .then(data => {{
                  if (data.status === "SUCCESS") {{
                      alert("Database cleaned and successfully synced with broker account deals!");
                      window.location.reload();
                  }} else {{
                      alert("Failed: " + data.message);
                      if (btn) {{
                          btn.disabled = false;
                          btn.textContent = "🧹 Clear History & Re-Sync";
                      }}
                  }}
              }})
              .catch(err => {{
                  console.error(err);
                  alert("Failed to contact maintenance API.");
                  if (btn) {{
                      btn.disabled = false;
                      btn.textContent = "🧹 Clear History & Re-Sync";
                  }}
              }});
        }}

        function resetDailyPnL() {{
            if (!confirm("Are you sure you want to reset today's database trade logs and drawdown metrics snapshots? This will reload the page.")) return;
            
            const btn = document.getElementById("btn-reset-pnl");
            if (btn) {{
                btn.disabled = true;
                btn.textContent = "🔄 Resetting PNL...";
            }}
            
            fetch('/api/v1/maintenance/reset-daily-pnl', {{
                method: 'POST'
            }}).then(res => res.json())
              .then(data => {{
                  if (data.status === "SUCCESS") {{
                      alert("Daily PNL reset complete!");
                      window.location.reload();
                  }} else {{
                      alert("Failed: " + data.message);
                      if (btn) {{
                          btn.disabled = false;
                          btn.textContent = "🔄 Reset Daily PNL";
                      }}
                  }}
              }})
              .catch(err => {{
                  console.error(err);
                  alert("Failed to contact reset daily PNL API.");
                  if (btn) {{
                      btn.disabled = false;
                      btn.textContent = "🔄 Reset Daily PNL";
                  }}
              }});
        }}

        // Candlestick Chart Engine Setup
        let chart = null;
        let candleSeries = null;
        let activeEntryPrice = {active_entry if has_active else 'null'};
        let activeSlPrice = {active_sl if has_active else 'null'};
        let activeTpPrice = {active_tp1 if has_active else 'null'};

        // Volume Profile Drawer
        function drawVolumeProfile(candles) {{
            const canvas = document.getElementById('vp-canvas');
            if (!canvas || !candleSeries || !chart) return;
            
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width * window.devicePixelRatio;
            canvas.height = rect.height * window.devicePixelRatio;
            
            const ctx = canvas.getContext('2d');
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
            ctx.clearRect(0, 0, rect.width, rect.height);
            
            if (!candles || candles.length === 0) return;
            
            let minPrice = Infinity;
            let maxPrice = -Infinity;
            candles.forEach(c => {{
                if (c.low < minPrice) minPrice = c.low;
                if (c.high > maxPrice) maxPrice = c.high;
            }});
            
            if (minPrice === Infinity || maxPrice === -Infinity || minPrice === maxPrice) return;
            
            const numBins = 24;
            const binSize = (maxPrice - minPrice) / numBins;
            const volumeBins = new Array(numBins).fill(0);
            
            candles.forEach(c => {{
                const price = c.close;
                const binIndex = Math.floor((price - minPrice) / binSize);
                if (binIndex >= 0 && binIndex < numBins) {{
                    volumeBins[binIndex] += c.volume;
                }}
            }});
            
            const maxVolume = Math.max(...volumeBins);
            if (maxVolume === 0) return;
            
            for (let i = 0; i < numBins; i++) {{
                const binPriceStart = minPrice + (i * binSize);
                const binPriceEnd = binPriceStart + binSize;
                
                const yTop = candleSeries.priceToCoordinate(binPriceEnd);
                const yBottom = candleSeries.priceToCoordinate(binPriceStart);
                
                if (yTop === null || yBottom === null) continue;
                
                const barHeight = Math.abs(yBottom - yTop);
                const barWidth = (volumeBins[i] / maxVolume) * rect.width;
                
                ctx.fillStyle = 'rgba(251, 191, 36, 0.12)';
                ctx.strokeStyle = 'rgba(251, 191, 36, 0.2)';
                ctx.lineWidth = 0.5;
                
                const xPos = rect.width - barWidth;
                ctx.fillRect(xPos, yTop, barWidth, barHeight - 1);
                ctx.strokeRect(xPos, yTop, barWidth, barHeight - 1);
            }}
        }}

        // Spread Lines — draw Bid/Ask lines on chart
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

        // Session Background Bands — canvas overlay
        const SESSION_DEFS = [
            {{ name: 'Sydney',   startH: 22, endH: 7,  color: 'rgba(59, 130, 246, 0.07)',  border: 'rgba(59, 130, 246, 0.25)' }},
            {{ name: 'Tokyo',    startH: 0,  endH: 9,  color: 'rgba(139, 92, 246, 0.07)', border: 'rgba(139, 92, 246, 0.25)' }},
            {{ name: 'London',   startH: 8,  endH: 17, color: 'rgba(16, 185, 129, 0.07)', border: 'rgba(16, 185, 129, 0.25)' }},
            {{ name: 'New York', startH: 13, endH: 22, color: 'rgba(251, 191, 36, 0.07)',  border: 'rgba(251, 191, 36, 0.25)' }},
        ];

        function drawSessionBands() {{
            if (!chart || !window.cachedCandles || window.cachedCandles.length === 0) return;

            const sc = document.getElementById('session-canvas');
            const wrapper = document.getElementById('chart-wrapper');
            if (!sc || !wrapper) return;

            const w = wrapper.offsetWidth;
            const h = wrapper.offsetHeight;
            if (w === 0 || h === 0) return;

            const dpr = window.devicePixelRatio || 1;
            sc.width  = w * dpr;
            sc.height = h * dpr;

            const ctx = sc.getContext('2d');
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            ctx.clearRect(0, 0, w, h);

            const timeScale = chart.timeScale();
            const visibleRange = timeScale.getVisibleRange();
            if (!visibleRange) return;

            const fromTs = visibleRange.from;
            const toTs   = visibleRange.to;
            const DAY    = 86400;
            const startDay = Math.floor(fromTs / DAY) * DAY - DAY;
            const endDay   = Math.ceil(toTs   / DAY) * DAY + DAY;

            // Helper: unix timestamp -> canvas x pixel
            function tsToX(ts) {{
                const coord = timeScale.timeToCoordinate(ts);
                return coord;
            }}

            for (let dayStart = startDay; dayStart <= endDay; dayStart += DAY) {{
                SESSION_DEFS.forEach(sess => {{
                    let sStart, sEnd;
                    if (sess.startH < sess.endH) {{
                        sStart = dayStart + sess.startH * 3600;
                        sEnd   = dayStart + sess.endH   * 3600;
                    }} else {{
                        // overnight: e.g. Sydney 22→7
                        sStart = dayStart + sess.startH * 3600 - DAY;
                        sEnd   = dayStart + sess.endH   * 3600;
                    }}

                    const clampStart = Math.max(sStart, fromTs);
                    const clampEnd   = Math.min(sEnd,   toTs);
                    if (clampEnd <= clampStart) return;

                    const x1 = tsToX(clampStart);
                    const x2 = tsToX(clampEnd);
                    if (x1 === null || x2 === null) return;

                    const bw = Math.max(1, x2 - x1);

                    // Fill band
                    ctx.fillStyle = sess.color;
                    ctx.fillRect(x1, 0, bw, h);

                    // Left dashed border
                    ctx.save();
                    ctx.strokeStyle = sess.border;
                    ctx.lineWidth = 1;
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.moveTo(x1, 0);
                    ctx.lineTo(x1, h);
                    ctx.stroke();
                    ctx.setLineDash([]);
                    ctx.restore();

                    // Label if wide enough
                    if (bw > 40) {{
                        ctx.save();
                        ctx.font = '700 9px Inter, sans-serif';
                        ctx.fillStyle = sess.border;
                        ctx.globalAlpha = 0.9;
                        ctx.textBaseline = 'top';
                        const tw = ctx.measureText(sess.name).width;
                        const lx = x1 + (bw / 2) - (tw / 2);
                        if (lx > 2 && lx + tw < w - 2) {{
                            ctx.fillText(sess.name, lx, 6);
                        }}
                        ctx.restore();
                    }}
                }});
            }}
        }}


        function generateMockCandles(timeframe, count) {{
            const candles = [];
            const seconds = (tf => {{
                switch(tf) {{
                    case 'M1': return 60;
                    case 'M5': return 5 * 60;
                    case 'M15': return 15 * 60;
                    case 'M30': return 30 * 60;
                    case 'H1': return 3600;
                    case 'H4': return 4 * 3600;
                    case 'D1': return 86400;
                    default: return 15 * 60;
                }}
            }})(timeframe);
            
            let time = Math.floor(Date.now() / 1000) - count * seconds;
            let close = 2320.0;
            
            for (let i = 0; i < count; i++) {{
                const change = (Math.random() - 0.5) * 8;
                const open = close;
                close = open + change;
                const high = Math.max(open, close) + Math.random() * 2;
                const low = Math.min(open, close) - Math.random() * 2;
                
                candles.push({{
                    time: time,
                    open: parseFloat(open.toFixed(2)),
                    high: parseFloat(high.toFixed(2)),
                    low: parseFloat(low.toFixed(2)),
                    close: parseFloat(close.toFixed(2)),
                    volume: Math.floor(Math.random() * 100) + 10
                }});
                time += seconds;
            }}
            return candles;
        }}

        function useMockChartFallback(timeframe, count) {{
            console.log("Using client-side mock chart data fallback for timeframe: " + timeframe);
            const mockData = generateMockCandles(timeframe, count || 120);
            candleSeries.setData(mockData);
            window.cachedCandles = mockData;
            window.lastCandle = mockData[mockData.length - 1];
            
            if (window.lastCandle) {{
                const bid = window.lastCandle.close;
                const ask = bid + 0.15;
                updateSpreadLines(bid, ask);
            }}
            
            // Clear old price lines if any
            if (window.entryLineObj) candleSeries.removePriceLine(window.entryLineObj);
            if (window.slLineObj) candleSeries.removePriceLine(window.slLineObj);
            if (window.tpLineObj) candleSeries.removePriceLine(window.tpLineObj);

            if (window.predEntryLine) {{ try {{ candleSeries.removePriceLine(window.predEntryLine); }} catch(e){{}} window.predEntryLine = null; }}
            if (window.predSlLine) {{ try {{ candleSeries.removePriceLine(window.predSlLine); }} catch(e){{}} window.predSlLine = null; }}
            if (window.predTp1Line) {{ try {{ candleSeries.removePriceLine(window.predTp1Line); }} catch(e){{}} window.predTp1Line = null; }}
            if (window.predTp2Line) {{ try {{ candleSeries.removePriceLine(window.predTp2Line); }} catch(e){{}} window.predTp2Line = null; }}

            if (activeEntryPrice) {{
                window.entryLineObj = candleSeries.createPriceLine({{
                    price: activeEntryPrice,
                    color: '#3b82f6',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'Entry (' + activeEntryPrice + ')',
                }});
            }}
            if (activeSlPrice) {{
                window.slLineObj = candleSeries.createPriceLine({{
                    price: activeSlPrice,
                    color: '#ef4444',
                    lineWidth: 1.5,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'SL (' + activeSlPrice + ')',
                }});
            }}
            if (activeTpPrice) {{
                window.tpLineObj = candleSeries.createPriceLine({{
                    price: activeTpPrice,
                    color: '#10b981',
                    lineWidth: 1.5,
                    lineStyle: LightweightCharts.LineStyle.Dashed,
                    axisLabelVisible: true,
                    title: 'TP (' + activeTpPrice + ')',
                }});
            }}

            const container = document.getElementById('tv-chart-container');
            let vpCanvas = document.getElementById('vp-canvas');
            if (!vpCanvas && container) {{
                vpCanvas = document.createElement('canvas');
                vpCanvas.id = 'vp-canvas';
                vpCanvas.style.position = 'absolute';
                vpCanvas.style.top = '0';
                vpCanvas.style.right = '60px';
                vpCanvas.style.width = '120px';
                vpCanvas.style.height = '100%';
                vpCanvas.style.zIndex = '10';
                vpCanvas.style.pointerEvents = 'none';
                container.style.position = 'relative';
                container.appendChild(vpCanvas);
            }}

            drawVolumeProfile(window.cachedCandles);
            drawSessionBands();
            chart.timeScale().fitContent();
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
                ? `Simulated AI Predictor Fallback (${{tf}}): XAUUSD has established solid bullish momentum. Golden crossover detected with M15 EMA20 crossing above EMA50. RSI stands at 58.2, showing room for upward continuation towards 2360 resistance.`
                : `Simulated AI Predictor Fallback (${{tf}}): Short-term bearish pressure observed on XAUUSD. Price action rejected from the local daily high. RSI has turned down from overbought territory (68 -> 52), favoring short continuation.`;
            
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
            
            drawPredictedLines(entry, sl, tp1, tp2);
            showToast("Mock AI prediction generated (unreachable backend fallback).");
        }}

        let tvWidget = null;

        function loadTradingViewWidget(timeframe) {{
            const container = document.getElementById('tv-chart-container');
            if (!container) return;
            
            // Map timeframe string to TradingView Widget interval
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
                    "studies": [
                        {{
                            "id": "Sessions@tv-basicstudies",
                            "inputs": {{
                                "sessSpec_0": "0000-2400:23456",
                                "color0":  "rgba(59, 130, 246, 0.12)",
                                "color1":  "rgba(139, 92, 246, 0.12)",
                                "color2":  "rgba(16, 185, 129, 0.12)",
                                "color3":  "rgba(251, 191, 36, 0.12)"
                            }}
                        }}
                    ],
                    "studies_overrides": {{
                        "sessions.sydney.color": "rgba(59, 130, 246, 0.15)",
                        "sessions.tokyo.color": "rgba(139, 92, 246, 0.15)",
                        "sessions.london.color": "rgba(16, 185, 129, 0.15)",
                        "sessions.newyork.color": "rgba(251, 191, 36, 0.15)"
                    }}
                }});
            }} else {{
                // Fallback to embedded iframe if script didn't load yet
                const iframe = document.createElement('iframe');
                iframe.src = `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_xauusd&symbol=OANDA%3AXAUUSD&interval=${{tvInterval}}&symboledit=1&saveimage=1&toolbarbg=080b14&studies=%5B%5D&theme=dark&style=1&timezone=exchange&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=en`;
                iframe.style.width = '100%';
                iframe.style.height = '100%';
                iframe.style.border = 'none';
                widgetDiv.appendChild(iframe);
            }}
        }}

        function initializeChart() {{
            loadTradingViewWidget('M15');
        }}

        function loadChartData(timeframe) {{
            loadTradingViewWidget(timeframe);
        }}

        function changeChartTimeframe(tf, btn) {{
            const btns = btn.parentNode.querySelectorAll('.tf-btn');
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadChartData(tf);
        }}

        function toggleFullScreenChart() {{
            const panel = document.querySelector('.chart-panel');
            panel.classList.toggle('full-screen-chart');
            const btn = document.getElementById('btn-chart-fullscreen');
            const isFullScreen = panel.classList.contains('full-screen-chart');
            btn.innerHTML = isFullScreen ? '🗗 Exit Fullscreen' : '🗖 Fullscreen';
            
            if (chart) {{
                const container = document.getElementById('tv-chart-container');
                chart.resize(container.clientWidth, container.clientHeight);
                const vpCanvas = document.getElementById('vp-canvas');
                if (vpCanvas) {{
                    vpCanvas.style.height = container.clientHeight + 'px';
                }}
                if (window.cachedCandles) {{
                    drawVolumeProfile(window.cachedCandles);
                    drawSessionBands();
                }}
            }}
        }}

        function toggleMinimizeChart() {{
            const panel = document.querySelector('.chart-panel');
            panel.classList.toggle('minimized-chart');
            const btn = document.getElementById('btn-chart-minimize');
            const isMinimized = panel.classList.contains('minimized-chart');
            btn.innerHTML = isMinimized ? '🗕 Expand' : '🗕 Minimize';
            
            if (!isMinimized && chart) {{
                setTimeout(() => {{
                    const container = document.getElementById('tv-chart-container');
                    chart.resize(container.clientWidth, container.clientHeight);
                    if (window.cachedCandles) {{
                        drawVolumeProfile(window.cachedCandles);
                        drawSessionBands();
                    }}
                }}, 50);
            }}
        }}

        function refreshEconomicCalendar(e) {{
            const btn = e ? e.currentTarget : null;
            if (btn) {{
                btn.disabled = true;
                btn.textContent = '🔄 Loading...';
            }}
            fetch('/api/v1/live-state?force_refresh=true')
                .then(res => {{
                    if (res.status === 401) {{
                        window.location.href = '/login';
                        return;
                    }}
                    return res.json();
                }})
                .then(data => {{
                    if (data && data.news_events) {{
                        let newsHtml = '';
                        data.news_events.forEach(event => {{
                            newsHtml += renderNewsEventHtml(event);
                        }});
                        const newsListContainer = document.getElementById('news-list');
                        if (newsListContainer) {{
                            newsListContainer.innerHTML = newsHtml;
                            filterCalendarEvents();
                            updateCalendarTimecounts();
                        }}
                        showToast("Economic calendar refreshed successfully.");
                    }} else {{
                        const newsListContainer = document.getElementById('news-list');
                        if (newsListContainer) {{
                            newsListContainer.innerHTML = "<div class='text-center text-muted small' style='padding: 1rem;'>No high-impact economic news scheduled today.</div>";
                        }}
                    }}
                }})
                .catch(err => {{
                    console.error("Error refreshing calendar: ", err);
                    showToast("Failed to refresh economic calendar.", true);
                }})
                .finally(() => {{
                    if (btn) {{
                        btn.disabled = false;
                        btn.textContent = '🔄 Refresh';
                    }}
                }});
        }}

        // Calendar Logic
        const tradesData = JSON.parse(document.getElementById('all-trades-data').textContent);
        let currentYear = new Date().getUTCFullYear();
        let currentMonth = new Date().getUTCMonth(); // 0-11
        const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const monthNames = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];

        function getTradesByDate() {{
            const grouped = {{}};
            const tz = getTimezonePreference();
            tradesData.forEach(trade => {{
                const rawTime = trade.closed_at || trade.created_at;
                if (!rawTime) return;
                try {{
                    const date = new Date(rawTime);
                    let options = {{ year: 'numeric', month: '2-digit', day: '2-digit' }};
                    if (tz !== 'local') {{
                        options.timeZone = tz;
                    }}
                    const dateStr = new Intl.DateTimeFormat('en-CA', options).format(date);
                    if (dateStr) {{
                        if (!grouped[dateStr]) {{
                            grouped[dateStr] = [];
                        }}
                        grouped[dateStr].push(trade);
                    }}
                }} catch (e) {{
                    console.error("Error grouping calendar trades: ", rawTime, e);
                }}
            }});
            return grouped;
        }}

        function renderCalendar(year, month) {{
            const grid = document.getElementById('calendar-days-grid');
            const title = document.getElementById('calendar-header-title');
            if (!grid || !title) return;

            const tradesByDate = getTradesByDate();
            grid.innerHTML = '';
            title.textContent = monthNames[month] + " " + year;

            weekdays.forEach(day => {{
                const el = document.createElement('div');
                el.className = 'calendar-weekday';
                el.textContent = day;
                grid.appendChild(el);
            }});

            const firstDayIndex = new Date(Date.UTC(year, month, 1)).getUTCDay();
            const totalDays = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();

            for (let i = 0; i < firstDayIndex; i++) {{
                const el = document.createElement('div');
                el.className = 'calendar-cell empty';
                grid.appendChild(el);
            }}

            for (let day = 1; day <= totalDays; day++) {{
                const el = document.createElement('div');
                el.className = 'calendar-cell';

                const dateKey = `${{year}}-${{String(month + 1).padStart(2, '0')}}-${{String(day).padStart(2, '0')}}`;
                const dayTrades = tradesByDate[dateKey] || [];

                const numEl = document.createElement('span');
                numEl.className = 'cell-num';
                numEl.textContent = day;
                el.appendChild(numEl);

                if (dayTrades.length > 0) {{
                    el.classList.add('has-trades');

                    let netProfit = 0;
                    let wins = 0;
                    dayTrades.forEach(tr => {{
                        netProfit += (tr.profit || 0.0);
                        if (tr.profit > 0.0) {{
                            wins++;
                        }}
                    }});

                    const pnlEl = document.createElement('div');
                    pnlEl.className = 'cell-pnl';
                    if (netProfit > 0) {{
                        pnlEl.className += ' text-buy';
                        pnlEl.textContent = `+$${{netProfit.toFixed(2)}}`;
                    }} else if (netProfit < 0) {{
                        pnlEl.className += ' text-sell';
                        pnlEl.textContent = `-$${{Math.abs(netProfit).toFixed(2)}}`;
                    }} else {{
                        pnlEl.className += ' text-muted';
                        pnlEl.textContent = `$0.00`;
                    }}
                    el.appendChild(pnlEl);

                    const accEl = document.createElement('div');
                    accEl.className = 'cell-acc';
                    const accPct = Math.round((wins / dayTrades.length) * 100);
                    accEl.textContent = `Acc: ${{accPct}}%`;
                    el.appendChild(accEl);

                    el.onclick = () => openTradeDrawer(dateKey, dayTrades, netProfit, wins);
                }}
                grid.appendChild(el);
            }}
        }}

        function navigateMonth(direction) {{
            currentMonth += direction;
            if (currentMonth < 0) {{
                currentMonth = 11;
                currentYear--;
            }} else if (currentMonth > 11) {{
                currentMonth = 0;
                currentYear++;
            }}
            renderCalendar(currentYear, currentMonth);
        }}

        function openTradeDrawer(dateStr, trades, netProfit, wins) {{
            const drawer = document.getElementById('trade-drawer');
            const bg = document.getElementById('drawer-bg');
            const dateTitle = document.getElementById('drawer-date-title');
            const profitEl = document.getElementById('drawer-day-profit');
            const accuracyEl = document.getElementById('drawer-day-accuracy');
            const listEl = document.getElementById('drawer-trades-list');

            const parsedDate = new Date(dateStr + "T00:00:00Z");
            dateTitle.textContent = parsedDate.toLocaleDateString("en-US", {{
                month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC'
            }});

            profitEl.textContent = (netProfit >= 0 ? "+" : "-") + "$" + Math.abs(netProfit).toFixed(2);
            profitEl.className = "widget-value " + (netProfit >= 0 ? "text-buy" : "text-sell");

            const accVal = trades.length > 0 ? Math.round((wins / trades.length) * 100) : 0;
            accuracyEl.textContent = accVal + "%";
            accuracyEl.className = "widget-value " + (accVal >= 70 ? "text-buy" : (accVal >= 40 ? "text-warning" : "text-sell"));

            listEl.innerHTML = '';
            trades.forEach(tr => {{
                const item = document.createElement('div');
                item.className = 'drawer-trade-card';

                const typeClass = tr.order_type === 'BUY' ? 'text-buy' : 'text-sell';
                const pnlClass = (tr.profit || 0) >= 0 ? 'text-buy font-bold' : 'text-sell font-bold';
                const statusBadge = tr.status === 'OPEN' ? 'badge-success' : 'badge-secondary';
                const timeStr = tr.closed_at ? tr.closed_at.split('T')[1].substring(0, 8) : 
                                (tr.created_at ? tr.created_at.split('T')[1].substring(0, 8) : '—');

                item.innerHTML = `
                    <div class="drawer-trade-header">
                        <span class="font-bold">#${{tr.ticket || '—'}}</span>
                        <span class="badge ${{statusBadge}}">${{tr.status}}</span>
                    </div>
                    <div class="drawer-trade-grid">
                        <div>Type: <span class="font-bold ${{typeClass}}">${{tr.order_type}}</span></div>
                        <div style="text-align: right;">Lots: <span class="drawer-trade-val">${{tr.volume.toFixed(2)}}</span></div>
                        
                        <div>Entry: <span class="drawer-trade-val">${{tr.entry_price.toFixed(2)}}</span></div>
                        <div style="text-align: right;">Exit: <span class="drawer-trade-val">${{tr.exit_price ? tr.exit_price.toFixed(2) : '—'}}</span></div>
                        
                        <div>Stop Loss: <span class="drawer-trade-val">${{tr.sl_price.toFixed(2)}}</span></div>
                        <div style="text-align: right;">Take Profit: <span class="drawer-trade-val">${{tr.tp_price.toFixed(2)}}</span></div>
                        
                        <div style="grid-column: span 2; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 0.25rem; padding-top: 0.25rem; display: flex; justify-content: space-between;">
                            <span>PnL: <span class="${{pnlClass}}">${{tr.profit !== null ? (tr.profit >= 0 ? '+' : '-') + '$' + Math.abs(tr.profit).toFixed(2) : 'Floating'}}</span></span>
                            <span class="text-muted small">${{timeStr}} UTC</span>
                        </div>
                    </div>
                    ${{tr.comment ? `<div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.4rem; padding-top: 0.2rem; border-top: 1px dashed rgba(255,255,255,0.03);">Comment: ${{tr.comment}}</div>` : ''}}
                `;
                listEl.appendChild(item);
            }});

            bg.style.display = 'block';
            setTimeout(() => {{
                bg.style.opacity = '1';
                drawer.classList.add('open');
            }}, 10);
        }}

        function closeTradeDrawer() {{
            const drawer = document.getElementById('trade-drawer');
            const bg = document.getElementById('drawer-bg');

            if (drawer) drawer.classList.remove('open');
            if (bg) bg.style.opacity = '0';
            setTimeout(() => {{
                if (bg) bg.style.display = 'none';
            }}, 300);
        }}

        // Dynamic dashboard updates and polling setup
        let liveStateInterval = null;
        let lastLiveTickPrice = null;
        let chartReloadCounter = 0;

        function startLiveStatePolling() {{
            if (liveStateInterval) clearInterval(liveStateInterval);
            
            liveStateInterval = setInterval(() => {{
                fetch('/api/v1/live-state')
                    .then(res => {{
                        if (res.status === 401) {{
                            clearInterval(liveStateInterval);
                            window.location.href = '/login';
                            return;
                        }}
                        return res.json();
                    }})
                    .then(data => {{
                        if (data && data.status === 'SUCCESS') {{
                            updateLiveDashboard(data);
                        }}
                    }})
                    .catch(err => console.error("Error polling live state: ", err));

            }}, 1500);
        }}

        function updateLiveDashboard(data) {{
            // 1. Connection Badge
            const brokerPulse = document.querySelector('.pulse-dot');
            const connectionText = document.querySelector('.connection-text');
            if (brokerPulse && connectionText) {{
                if (data.broker_connected) {{
                    brokerPulse.className = 'pulse-dot pulse-green';
                    connectionText.textContent = 'CONNECTED';
                }} else {{
                    brokerPulse.className = 'pulse-dot pulse-red';
                    connectionText.textContent = 'DISCONNECTED';
                }}
            }}

            // 2. Account parameters in sidebar and top widgets
            const balanceVal = data.balance;
            const equityVal = data.equity;
            const freeMarginVal = data.free_margin;
            const marginUsedVal = data.margin;
            const marginLevelVal = data.margin_level;

            const sidebarElements = document.querySelectorAll('aside .footer-val');
            if (sidebarElements.length >= 5) {{
                sidebarElements[0].textContent = '$' + balanceVal.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
                sidebarElements[1].textContent = '$' + equityVal.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
                sidebarElements[2].textContent = '$' + freeMarginVal.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
                sidebarElements[3].textContent = '$' + marginUsedVal.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
                sidebarElements[4].textContent = marginUsedVal > 0 ? marginLevelVal.toFixed(2) + '%' : '—';
            }}

            const widgetValues = document.querySelectorAll('.widget-value');
            if (widgetValues.length >= 3) {{
                widgetValues[0].textContent = '$' + balanceVal.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
                widgetValues[1].textContent = data.open_trades.length;
                
                const dailyPnl = data.daily_pnl;
                const pnlEl = document.getElementById('daily-pnl-val');
                if (pnlEl) {{
                    pnlEl.textContent = (dailyPnl >= 0 ? '+' : '') + '$' + dailyPnl.toFixed(2);
                    const trendEl = pnlEl.nextElementSibling;
                    if (trendEl) {{
                        if (dailyPnl > 0) {{
                            trendEl.className = 'widget-trend trend-up';
                            trendEl.textContent = '↑ ' + ((dailyPnl / balanceVal) * 100).toFixed(2) + '%';
                        }} else if (dailyPnl < 0) {{
                            trendEl.className = 'widget-trend trend-down';
                            trendEl.textContent = '↓ ' + (Math.abs(dailyPnl / balanceVal) * 100).toFixed(2) + '%';
                        }} else {{
                            trendEl.className = 'text-muted';
                            trendEl.textContent = '0.00%';
                        }}
                    }}
                }}
            }}

            // 3. Bid/Ask and Spread
            if (data.tick) {{
                const bid = data.tick.bid;
                const ask = data.tick.ask;
                const spreadPips = data.tick.spread_pips;
                const spreadPoints = data.tick.spread_points;

                const priceBadge = document.getElementById('live-symbol-price');
                if (priceBadge && bid > 0) {{
                    let directionArrow = '▲';
                    let directionClass = 'text-buy';
                    if (lastLiveTickPrice !== null && bid < lastLiveTickPrice) {{
                        directionArrow = '▼';
                        directionClass = 'text-sell';
                    }}
                    lastLiveTickPrice = bid;
                    priceBadge.className = 'price-badge ' + directionClass;
                    
                    const spreadWarningHtml = data.tick.spread_warning ? 
                        ` <span style="font-size: 0.65rem; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239,68,68,0.4); color: var(--sell-color); padding: 0.1rem 0.3rem; border-radius: 4px; vertical-align: middle; margin-left: 0.5rem; font-weight: 700;">HIGH SPREAD</span>` : '';
                    
                    priceBadge.innerHTML = bid.toFixed(2) + ` <span style="font-size: 0.8rem;">${{directionArrow}}</span>` + spreadWarningHtml;
                }}

                const activeEntryEl = document.getElementById('active-entry-price');
                if (activeEntryEl) {{
                    let spreadRow = document.getElementById('active-spread-row');
                    if (!spreadRow) {{
                        spreadRow = document.createElement('div');
                        spreadRow.id = 'active-spread-row';
                        spreadRow.className = 'metric-row';
                        activeEntryEl.closest('.active-signal-details').querySelector('div[style*="flex-direction: column"]').insertBefore(spreadRow, activeEntryEl.parentElement);
                    }}
                    const spreadColorClass = data.tick.spread_warning ? 'text-sell font-bold' : 'text-muted';
                    spreadRow.innerHTML = `
                        <span class="metric-label">Current Spread</span>
                        <span class="metric-value ${{spreadColorClass}}">${{spreadPips.toFixed(1)}} Pips (${{spreadPoints.toFixed(0)}} pts)</span>
                    `;
                }}

                if (bid > 0 && ask > 0) {{
                    updateSpreadLines(bid, ask);
                }}

                if (bid > 0) {{
                    updateLiveChartPrice(bid);
                }}
            }}

            // 4. Active Signal / Trade Card
            const openTrades = data.open_trades;
            const lastSignal = data.last_signal;
            const activeDetails = document.querySelector('.active-signal-details');
            
            if (activeDetails) {{
                const directionBadge = activeDetails.parentElement.querySelector('.badge');
                const symbolPair = document.getElementById('active-symbol-pair');
                const ticketEl = document.getElementById('active-ticket-id');
                const entryEl = document.getElementById('active-entry-price');
                const slEl = document.getElementById('active-sl-price');
                const tpEl = document.getElementById('active-tp-price');
                const tp2El = document.getElementById('active-tp2-price');
                const timeEl = document.getElementById('active-trade-time');
                const rrEl = document.getElementById('active-rr');
                const lotsEl = document.getElementById('active-lots');
                const statusBadge = document.getElementById('active-status-badge');
                const closeBtnContainer = document.getElementById('active-close-btn-container');
                const pnlRow = document.getElementById('active-pnl-row');
                const pnlVal = document.getElementById('active-floating-pnl');

                if (openTrades.length > 0) {{
                    const trade = openTrades[0];
                    
                    if (directionBadge) {{
                        directionBadge.textContent = trade.order_type;
                        directionBadge.className = 'badge ' + (trade.order_type === 'BUY' ? 'badge-success' : 'badge-danger');
                    }}
                    if (symbolPair) symbolPair.textContent = trade.symbol;
                    if (ticketEl) ticketEl.textContent = '#' + trade.ticket;
                    if (entryEl) entryEl.textContent = trade.entry_price.toFixed(2);
                    if (slEl) slEl.textContent = trade.sl_price.toFixed(2);
                    if (tpEl) tpEl.textContent = trade.tp_price.toFixed(2);
                    if (tp2El) tp2El.textContent = (trade.tp_price + (trade.tp_price - trade.entry_price) * 0.5).toFixed(2);
                    if (timeEl) {{
                        timeEl.setAttribute('data-iso', trade.created_at);
                        timeEl.textContent = formatDateTime(trade.created_at, getTimezonePreference());
                    }}
                    if (rrEl) {{
                        const diffSl = Math.abs(trade.entry_price - trade.sl_price);
                        const diffTp = Math.abs(trade.tp_price - trade.entry_price);
                        const rrRatio = diffSl > 0 ? (diffTp / diffSl).toFixed(2) : '2.0';
                        rrEl.textContent = '1 : ' + rrRatio;
                    }}
                    if (lotsEl) lotsEl.textContent = trade.volume.toFixed(2) + ' Lots';
                    
                    if (statusBadge) {{
                        statusBadge.textContent = 'OPEN';
                        statusBadge.className = 'badge badge-success';
                    }}

                    if (data.tick && data.tick.bid > 0) {{
                        const bid = data.tick.bid;
                        const ask = data.tick.ask;
                        const currentPrice = trade.order_type === 'BUY' ? bid : ask;
                        const multiplier = 100.0;
                        let profit = 0.0;
                        if (trade.order_type === 'BUY') {{
                            profit = (currentPrice - trade.entry_price) * trade.volume * multiplier;
                        }} else {{
                            profit = (trade.entry_price - currentPrice) * trade.volume * multiplier;
                        }}
                        
                        if (pnlRow && pnlVal) {{
                            pnlRow.style.display = 'flex';
                            pnlVal.textContent = (profit >= 0 ? '+' : '') + '$' + profit.toFixed(2);
                            pnlVal.className = 'metric-value font-bold ' + (profit >= 0 ? 'text-buy' : 'text-sell');
                        }}
                    }}

                    if (closeBtnContainer) {{
                        closeBtnContainer.innerHTML = `<button class="close-btn" id="btn-close-active-trade" onclick="closeActiveTrade(${{trade.ticket}})">Close Trade</button>`;
                    }}
                    
                    activeEntryPrice = trade.entry_price;
                    activeSlPrice = trade.sl_price;
                    activeTpPrice = trade.tp_price;
                    
                }} else {{
                    if (pnlRow) pnlRow.style.display = 'none';
                    activeEntryPrice = null;
                    activeSlPrice = null;
                    activeTpPrice = null;
                    
                    if (window.entryLineObj) {{ candleSeries.removePriceLine(window.entryLineObj); window.entryLineObj = null; }}
                    if (window.slLineObj) {{ candleSeries.removePriceLine(window.slLineObj); window.slLineObj = null; }}
                    if (window.tpLineObj) {{ candleSeries.removePriceLine(window.tpLineObj); window.tpLineObj = null; }}

                    if (directionBadge) {{
                        directionBadge.textContent = '—';
                        directionBadge.className = 'badge badge-secondary';
                    }}
                    if (symbolPair) symbolPair.textContent = 'XAUUSD';
                    if (ticketEl) ticketEl.textContent = '—';
                    if (entryEl) entryEl.textContent = '—';
                    if (slEl) slEl.textContent = '—';
                    if (tpEl) tpEl.textContent = '—';
                    if (tp2El) tp2El.textContent = '—';
                    if (timeEl) {{
                        timeEl.removeAttribute('data-iso');
                        timeEl.textContent = '—';
                    }}
                    if (rrEl) rrEl.textContent = '—';
                    if (lotsEl) lotsEl.textContent = '—';
                    if (statusBadge) {{
                        statusBadge.textContent = 'NO ACTIVE POSITION';
                        statusBadge.className = 'badge badge-secondary';
                    }}

                    if (closeBtnContainer) {{
                        closeBtnContainer.innerHTML = '<button class="close-btn" id="btn-close-active-trade" style="opacity: 0.5; cursor: not-allowed;" disabled>No Active Positions</button>';
                    }}
                }}
            }}
            
            // 5. Open Positions Table
            const openTableBody = document.querySelector('#trades-view table tbody');
            if (openTableBody) {{
                if (openTrades.length > 0) {{
                    let tableHtml = '';
                    openTrades.forEach(t => {{
                        const dirClass = t.order_type === 'BUY' ? 'text-buy' : 'text-sell';
                        tableHtml += `
                            <tr>
                                <td>#${{t.ticket}}</td>
                                <td class="font-bold">${{t.symbol}}</td>
                                <td class="font-bold ${{dirClass}}">${{t.order_type}}</td>
                                <td>${{t.volume.toFixed(2)}}</td>
                                <td>${{t.entry_price.toFixed(2)}}</td>
                                <td>${{t.sl_price.toFixed(2)}}</td>
                                <td>${{t.tp_price.toFixed(2)}}</td>
                                <td><span class="time-cell" data-iso="${{t.created_at}}">${{formatDateTime(t.created_at, getTimezonePreference())}}</span></td>
                                <td><button class="badge badge-danger" onclick="closeActiveTrade(${{t.ticket}})" style="border:none; cursor:pointer;">CLOSE</button></td>
                            </tr>
                        `;
                    }});
                    openTableBody.innerHTML = tableHtml;
                }} else {{
                    openTableBody.innerHTML = `<tr><td colspan="9" class="text-center text-muted">No current open trading positions.</td></tr>`;
                }}
            }}
            
            // 6. Economic news feed updates
            const newsListContainer = document.getElementById('news-list');
            if (newsListContainer && data.news_events) {{
                if (data.news_events.length > 0) {{
                    let newsHtml = '';
                    data.news_events.forEach(event => {{
                        newsHtml += renderNewsEventHtml(event);
                    }});
                    newsListContainer.innerHTML = newsHtml;
                    filterCalendarEvents();
                    updateCalendarTimecounts();
                }} else {{
                    newsListContainer.innerHTML = "<div class='text-center text-muted small' style='padding: 1rem;'>No high-impact economic news scheduled today.</div>";
                }}
            }}
        }}

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
            drawVolumeProfile(window.cachedCandles);
        }}

        function drawPredictedLines(entry, sl, tp1, tp2) {{
            if (!candleSeries) return;
            
            if (window.predEntryLine) {{ try {{ candleSeries.removePriceLine(window.predEntryLine); }} catch(e){{}} window.predEntryLine = null; }}
            if (window.predSlLine) {{ try {{ candleSeries.removePriceLine(window.predSlLine); }} catch(e){{}} window.predSlLine = null; }}
            if (window.predTp1Line) {{ try {{ candleSeries.removePriceLine(window.predTp1Line); }} catch(e){{}} window.predTp1Line = null; }}
            if (window.predTp2Line) {{ try {{ candleSeries.removePriceLine(window.predTp2Line); }} catch(e){{}} window.predTp2Line = null; }}
            
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

        function runAiPrediction() {{
            const btn = document.getElementById('btn-run-prediction');
            const loader = document.getElementById('prediction-loader');
            const results = document.getElementById('prediction-results');
            
            if (btn) btn.disabled = true;
            if (loader) loader.style.display = 'flex';
            if (results) results.style.display = 'none';
            
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

        function reconnectBroker() {{
            const btn = document.getElementById('btn-reconnect-broker');
            const icon = document.getElementById('reconnect-icon');
            if (btn) btn.disabled = true;
            if (icon) icon.textContent = '⏳';

            fetch('/api/v1/reconnect', {{ method: 'POST' }})
                .then(res => {{
                    if (res.status === 401) {{ window.location.href = '/login'; return; }}
                    return res.json();
                }})
                .then(data => {{
                    if (btn) btn.disabled = false;
                    if (icon) icon.textContent = '⚡';

                    if (data && data.status === 'SUCCESS') {{
                        showToast('✅ ' + data.message);
                        // Update broker status widget inline
                        const connVal = document.getElementById('broker-conn-val');
                        if (connVal) {{
                            const dot = connVal.querySelector('.pulse-dot');
                            if (dot) {{ dot.className = 'pulse-dot pulse-green'; dot.style.width='8px'; dot.style.height='8px'; }}
                            const textNodes = [...connVal.childNodes].filter(n => n.nodeType === 3);
                            if (textNodes.length > 0) textNodes[0].textContent = ' CONNECTED';
                            connVal.style.color = 'var(--buy-color)';
                        }}
                        const sidebarStatus = document.querySelector('.connection-text');
                        if (sidebarStatus) sidebarStatus.textContent = 'CONNECTED';
                        const sidebarDot = document.querySelector('aside .pulse-dot');
                        if (sidebarDot) sidebarDot.className = 'pulse-dot pulse-green';
                    }} else {{
                        const msg = data ? data.message : 'Connection failed';
                        showToast('❌ ' + msg, true);
                        if (icon) icon.textContent = '❌';
                        setTimeout(() => {{ if (icon) icon.textContent = '⚡'; }}, 3000);
                    }}
                }})
                .catch(err => {{
                    console.error(err);
                    if (btn) btn.disabled = false;
                    if (icon) icon.textContent = '⚡';
                    showToast('Network error during reconnect attempt.', true);
                }});
        }}

        function saveSystemSettings() {{
            const btn = document.getElementById('btn-save-settings');
            if (btn) btn.disabled = true;

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
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(payload)
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (btn) btn.disabled = false;
                if (data && (data.status === 'SUCCESS' || data.status === 'success')) {{
                    showToast("Configuration saved successfully. System reconnected.");
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 1500);
                }} else {{
                    showToast("Failed to save settings: " + (data ? data.message : "unknown error"), true);
                }}
            }})
            .catch(err => {{
                console.error(err);
                if (btn) btn.disabled = false;
                showToast("Network error trying to save settings.", true);
            }});
        }}

        function addDashboardTask() {{
            const input = document.getElementById('new-task-input');
            const title = input ? input.value.trim() : '';
            if (!title) return;
            
            fetch('/api/v1/tasks', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ title: title }})
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (data && (data.status === 'SUCCESS' || data.status === 'success')) {{
                    if (input) input.value = '';
                    reloadTasksList();
                    showToast("Task added successfully.");
                }} else {{
                    showToast("Failed to add task.", true);
                }}
            }})
            .catch(err => {{
                console.error(err);
                showToast("Error adding task.", true);
            }});
        }}

        function toggleTask(taskId, completed) {{
            fetch('/api/v1/tasks/' + taskId, {{
                method: 'PUT',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ completed: completed }})
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (data && (data.status === 'SUCCESS' || data.status === 'success')) {{
                    const taskItem = document.querySelector(`.task-item[data-id="${{taskId}}"]`);
                    if (taskItem) {{
                        const titleSpan = taskItem.querySelector('.task-title');
                        if (titleSpan) {{
                            if (completed) {{
                                titleSpan.style.textDecoration = 'line-through';
                                titleSpan.style.color = 'var(--text-secondary)';
                            }} else {{
                                titleSpan.style.textDecoration = 'none';
                                titleSpan.style.color = '#ffffff';
                            }}
                        }}
                    }}
                    showToast("Task updated.");
                }} else {{
                    showToast("Failed to update task.", true);
                }}
            }})
            .catch(err => {{
                console.error(err);
                showToast("Error updating task.", true);
            }});
        }}

        function deleteTask(taskId, el) {{
            fetch('/api/v1/tasks/' + taskId, {{
                method: 'DELETE'
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (data && (data.status === 'SUCCESS' || data.status === 'success')) {{
                    if (el) {{
                        el.remove();
                    }}
                    showToast("Task deleted.");
                }} else {{
                    showToast("Failed to delete task.", true);
                }}
            }})
            .catch(err => {{
                console.error(err);
                showToast("Error deleting task.", true);
            }});
        }}

        function reloadTasksList() {{
            fetch('/api/v1/tasks')
            .then(res => res.json())
            .then(tasks => {{
                const list = document.getElementById('dashboard-tasks-list');
                if (!list) return;
                list.innerHTML = '';
                tasks.forEach(task => {{
                    const checkedAttr = task.completed ? 'checked' : '';
                    const textDecor = task.completed ? 'text-decoration: line-through; color: var(--text-secondary);' : 'color: #ffffff;';
                    const div = document.createElement('div');
                    div.className = 'task-item';
                    div.dataset.id = task.id;
                    div.style = 'display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.03); border-radius: 6px; gap: 0.5rem; transition: background 0.2s;';
                    div.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 0.5rem; flex-grow: 1;">
                            <input type="checkbox" ${{checkedAttr}} onchange="toggleTask(${{task.id}}, this.checked)" style="cursor: pointer; width: 14px; height: 14px; accent-color: var(--accent-gold);"/>
                            <span class="task-title" style="font-size: 0.78rem; font-weight: 500; ${{textDecor}}">${{task.title}}</span>
                        </div>
                        <button onclick="deleteTask(${{task.id}}, this.parentNode)" style="background: none; border: none; color: var(--sell-color); font-size: 0.85rem; cursor: pointer; padding: 0 0.25rem;">&times;</button>
                    `;
                    list.appendChild(div);
                }});
            }})
            .catch(err => console.error("Error loading tasks:", err));
        }}

        function sendChatMessage() {{
            const input = document.getElementById('chat-input');
            const btn = document.getElementById('btn-send-chat');
            const message = input ? input.value.trim() : '';
            if (!message) return;
            
            const messagesContainer = document.getElementById('chat-messages');
            const emptyNotice = document.getElementById('chat-empty-notice');
            if (emptyNotice) emptyNotice.remove();
            
            const userBubble = document.createElement('div');
            userBubble.style = 'max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px; align-self: flex-end; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); display: flex; flex-direction: column; gap: 0.25rem;';
            userBubble.innerHTML = `
                <span style="font-size: 0.68rem; font-weight: 700; color: var(--accent-gold);">You</span>
                <div style="font-size: 0.8rem; color: #ffffff; line-height: 1.4; white-space: pre-wrap;">${{escapeHtml(message)}}</div>
            `;
            messagesContainer.appendChild(userBubble);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            if (input) input.value = '';
            if (btn) btn.disabled = true;
            
            const loaderBubble = document.createElement('div');
            loaderBubble.id = 'chat-loader-bubble';
            loaderBubble.style = 'align-self: flex-start; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px; display: flex; align-items: center; gap: 0.5rem;';
            loaderBubble.innerHTML = `
                <div class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></div>
                <span style="font-size: 0.75rem; color: var(--text-secondary);">AI is processing...</span>
            `;
            messagesContainer.appendChild(loaderBubble);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            fetch('/api/v1/chat', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ message: message }})
            }})
            .then(res => {{
                if (res.status === 401) {{
                    window.location.href = '/login';
                    return;
                }}
                return res.json();
            }})
            .then(data => {{
                if (btn) btn.disabled = false;
                const loader = document.getElementById('chat-loader-bubble');
                if (loader) loader.remove();
                
                if (data && (data.status === 'SUCCESS' || data.status === 'success')) {{
                    const aiBubble = document.createElement('div');
                    aiBubble.style = 'align-self: flex-start; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px; display: flex; flex-direction: column; gap: 0.25rem;';
                    aiBubble.innerHTML = `
                        <span style="font-size: 0.68rem; font-weight: 700; color: #38bdf8;">AI Assistant</span>
                        <div style="font-size: 0.8rem; color: #ffffff; line-height: 1.4; white-space: pre-wrap;">${{escapeHtml(data.response)}}</div>
                    `;
                    messagesContainer.appendChild(aiBubble);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }} else {{
                    const errorBubble = document.createElement('div');
                    errorBubble.style = 'align-self: flex-start; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px;';
                    errorBubble.innerHTML = `<span style="font-size: 0.8rem; color: #f87171;">Failed to get AI response. Please verify keys in Settings.</span>`;
                    messagesContainer.appendChild(errorBubble);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }}
            }})
            .catch(err => {{
                console.error(err);
                if (btn) btn.disabled = false;
                const loader = document.getElementById('chat-loader-bubble');
                if (loader) loader.remove();
                
                const errorBubble = document.createElement('div');
                errorBubble.style = 'align-self: flex-start; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); max-width: 80%; padding: 0.75rem 1rem; border-radius: 8px;';
                errorBubble.innerHTML = `<span style="font-size: 0.8rem; color: #f87171;">Network error connecting to Chat Assistant.</span>`;
                messagesContainer.appendChild(errorBubble);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }});
        }}

        let recognition = null;
        let isListening = false;

        function toggleVoiceTyping() {{
            const btn = document.getElementById('btn-voice-chat');
            const input = document.getElementById('chat-input');
            
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                showToast("Web Speech API is not supported in this browser.", true);
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
                btn.classList.add('mic-active');
                btn.innerHTML = '🎤';
                input.placeholder = "Listening...";
            }};
            
            recognition.onerror = function(event) {{
                console.error("Speech recognition error", event.error);
                showToast("Speech recognition error: " + event.error, true);
                stopRecognition();
            }};
            
            recognition.onend = function() {{
                stopRecognition();
            }};
            
            recognition.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;
                if (transcript) {{
                    const currentVal = input.value.trim();
                    input.value = currentVal ? currentVal + " " + transcript : transcript;
                }}
            }};
            
            function stopRecognition() {{
                isListening = false;
                btn.classList.remove('mic-active');
                btn.innerHTML = '🎙️';
                input.placeholder = "Type your message here...";
            }}
            
            recognition.start();
        }}
        
        function escapeHtml(text) {{
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        function showToast(message, isError = false) {{
            const toast = document.getElementById('toast');
            if (toast) {{
                toast.textContent = message;
                toast.style.background = isError ? 'rgba(239, 68, 68, 0.95)' : 'rgba(16, 185, 129, 0.95)';
                toast.style.display = 'block';
                setTimeout(() => {{
                    toast.style.display = 'none';
                }}, 4000);
            }}
        }}

        // Initialization
        window.onload = function() {{
            initializeChart();
            renderCalendar(currentYear, currentMonth);
            applyTimezoneFormatting();
            updateClock();
            startLiveStatePolling();
            
            // Economic Calendar initialization
            filterCalendarEvents();
            updateCalendarTimecounts();
            setInterval(updateCalendarTimecounts, 1000);
            
            const msgContainer = document.getElementById('chat-messages');
            if (msgContainer) {{
                msgContainer.scrollTop = msgContainer.scrollHeight;
            }}
        }};
    </script>
    <!-- Toast Notification -->
    <div id="toast" class="toast"></div>
</body>
</html>
"""

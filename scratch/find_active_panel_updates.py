with open('app/utils/dashboard_template.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'active-symbol-pair' in line or 'active-ticket-id' in line or 'active-entry-price' in line or 'active-sl-price' in line or 'active-tp-price' in line or 'active-tp2-price' in line or 'active-trade-time' in line or 'active-timeframe' in line or 'active-rr' in line or 'active-lots' in line or 'active-status-badge' in line:
            print(f"Line {idx+1}: {line.strip()}")

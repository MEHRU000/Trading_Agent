with open('app/utils/dashboard_template.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'ACTIVE' in line.upper() and 'TRADE' in line.upper():
            print(f"Line {idx+1}: {line.strip()}")

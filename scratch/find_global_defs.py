with open("app/utils/dashboard_template.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "sidebar_balance" in line or "mt5_server" in line:
        if "=" in line:
            print(f"Line {i}: {line}")

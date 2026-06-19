with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "weekly_pnl =" in line or "monthly_pnl =" in line:
        print(f"Line {i}: {line}")

with open("app/database/trade_history.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
found = False
for i, line in enumerate(lines, 1):
    if "def get_performance_stats" in line:
        found = True
        print(f"Found on line {i}: {line}")
        # print next 30 lines
        for j in range(i, min(i+35, len(lines))):
            print(f"{j+1}: {lines[j]}")
        break

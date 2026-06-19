with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

for i, line in enumerate(content.splitlines(), 1):
    if "class " in line and "Schema" in line or "class MarketIntelRequest" in line:
        print(f"{i}: {line}")

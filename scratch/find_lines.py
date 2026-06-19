filepath = r"c:\Users\mehru\.gemini\antigravity\scratch\trading-agent\app\utils\dashboard_template.py"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("\n=== Context around L3950 ===")
for idx in range(3940, 4085):
    try:
        print(f"L{idx+1}: {lines[idx].rstrip()}")
    except Exception:
        print(f"L{idx+1}: {lines[idx].rstrip().encode('ascii', 'replace').decode('ascii')}")

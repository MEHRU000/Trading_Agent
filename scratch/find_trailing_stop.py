with open("app/utils/dashboard_template.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
found = False
for i, line in enumerate(lines, 1):
    if "toggleTrailingStop" in line:
        found = True
        print(f"Line {i}: {line}")
if not found:
    print("toggleTrailingStop not found in dashboard_template.py")

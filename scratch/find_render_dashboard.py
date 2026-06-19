with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "render_dashboard(" in line:
        print(f"Found on line {i}: {line}")
        # print next 25 lines
        for j in range(i-5, min(i+40, len(lines))):
            print(f"{j+1}: {lines[j]}")
        break

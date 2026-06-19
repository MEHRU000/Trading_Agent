with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i, line in enumerate(lines, 1):
    if "uvicorn.run" in line:
        print(f"Line {i}: {line}")
        # print next 5 lines
        for j in range(i, min(i+5, len(lines))):
            print(f"{j+1}: {lines[j]}")

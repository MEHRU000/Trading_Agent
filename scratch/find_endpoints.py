import re

with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

for i, line in enumerate(content.splitlines(), 1):
    if "/api/v1/" in line:
        print(f"{i}: {line}")

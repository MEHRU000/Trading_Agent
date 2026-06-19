with open("rendered_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

for line in content.splitlines():
    if "let currentB =" in line:
        print(line)

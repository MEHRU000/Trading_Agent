import os

def search_files():
    for root, dirs, files in os.walk("app"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                if "trailing" in content.lower():
                    print(f"File: {path}")
                    for line in content.splitlines():
                        if "def " in line and "trailing" in line.lower() or "class " in line and "trailing" in line.lower():
                            print(f"  {line}")

search_files()

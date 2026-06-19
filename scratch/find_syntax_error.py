import re

with open(r"c:\Users\mehru\.gemini\antigravity\scratch\trading-agent\app\utils\dashboard_template.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find f-strings. A simple regex for f""" ... """
# or we can write a script to find curly braces that are not doubled.
# Since the whole body of render_dashboard uses return f"""...""",
# let's locate all f""" or f''' and extract the f-string content.

fstring_matches = list(re.finditer(r'f"""(.*?)"""', content, re.DOTALL))
print(f"Found {len(fstring_matches)} multiline f-strings.")

for i, match in enumerate(fstring_matches):
    start_pos = match.start()
    end_pos = match.end()
    # Find the line number
    start_line = content[:start_pos].count("\n") + 1
    end_line = content[:end_pos].count("\n") + 1
    print(f"F-string {i+1}: lines {start_line} to {end_line}")
    
    # Check for single { or } in this f-string
    f_body = match.group(1)
    
    # We want to check for occurrences of single { or }
    # A single { is a '{' not preceded by '{' and not followed by '{'
    # Wait, in regex, we can find single '{' by looking for (?<!{){(?!{)
    # and single '}' by (?<!})}(?!})
    
    single_opens = []
    for m in re.finditer(r'(?<!{){(?!{)', f_body):
        offset = start_pos + len('f"""') + m.start()
        line = content[:offset].count("\n") + 1
        col = offset - content[:offset].rfind("\n")
        # Extract surrounding context
        ctx = content[offset-50:offset+50].replace("\n", " ")
        single_opens.append((line, col, ctx))
        
    single_closes = []
    for m in re.finditer(r'(?<!})}(?!})', f_body):
        offset = start_pos + len('f"""') + m.start()
        line = content[:offset].count("\n") + 1
        col = offset - content[:offset].rfind("\n")
        ctx = content[offset-50:offset+50].replace("\n", " ")
        single_closes.append((line, col, ctx))
        
    print(f"  Single opens: {len(single_opens)}")
    for line, col, ctx in single_opens[:15]:
        print(f"    Line {line}, Col {col}: ... {ctx} ...")
    if len(single_opens) > 15:
        print("    ...")
        
    print(f"  Single closes: {len(single_closes)}")
    for line, col, ctx in single_closes[:15]:
        print(f"    Line {line}, Col {col}: ... {ctx} ...")
    if len(single_closes) > 15:
        print("    ...")

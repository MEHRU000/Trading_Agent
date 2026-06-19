import sys

with open('app/utils/dashboard_template.py', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'active-' in line or 'getElementById' in line:
            print(f"Line {idx+1}: {line.strip()[:100]}")

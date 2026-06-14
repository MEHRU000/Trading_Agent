import json
import os

transcript_path = r"C:\Users\mehru\.gemini\antigravity-ide\brain\eeefbee9-5d8d-4e9a-8048-3a03d1b96cb2\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(transcript_path):
        print(f"File not found: {transcript_path}")
        return
        
    print("Reading transcript.jsonl...")
    steps = []
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                steps.append(json.loads(line))
            except Exception:
                pass
                
    print(f"Total steps loaded: {len(steps)}")
    last_20 = steps[-20:]
    for i, step in enumerate(last_20):
        idx = len(steps) - 20 + i
        step_type = step.get("type", "unknown")
        source = step.get("source", "unknown")
        content = step.get("content", "")
        tc_names = [tc.get("function", "") for tc in step.get("tool_calls", [])]
        print(f"\n[{idx}] Source: {source} | Type: {step_type} | Tools: {tc_names}")
        if content:
            print(f"Content: {content[:300]}")



if __name__ == "__main__":
    main()


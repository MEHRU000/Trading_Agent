import urllib.request
import json
import hmac
import hashlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.config import settings

def test_live_state():
    url = "http://127.0.0.1:8000/api/v1/live-state"
    try:
        req = urllib.request.Request(url)
        payload = f"{settings.DASHBOARD_USERNAME}:{settings.DASHBOARD_PASSWORD}"
        sig = hmac.new(
            settings.WEBHOOK_SECRET.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        req.add_header("Cookie", f"session_id={sig}")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print("=== Selected live-state keys ===")
            print(f"status: {data.get('status')}")
            print(f"broker_connected: {data.get('broker_connected')}")
            print(f"balance: {data.get('balance')}")
            print(f"equity: {data.get('equity')}")
            print(f"tick: {data.get('tick')}")
            print(f"open_trades count: {len(data.get('open_trades', []))}")
            if data.get('open_trades'):
                for t in data.get('open_trades'):
                    print(f"Trade: {t}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_live_state()

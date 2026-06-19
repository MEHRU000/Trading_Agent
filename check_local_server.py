import urllib.request
import json
import hmac
import hashlib
from app.utils.config import settings

def test_live_state():
    url = "http://127.0.0.1:7999/api/v1/live-state"
    try:
        req = urllib.request.Request(url)
        payload = f"{settings.DASHBOARD_USERNAME}:{settings.DASHBOARD_PASSWORD}"
        sig = hmac.new(
            settings.WEBHOOK_SECRET.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        req.add_header("Cookie", f"session_id={sig}")
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            print("=== Selected live-state keys ===")
            print(f"broker_connected: {data.get('broker_connected')}")
            print(f"account_mode: {data.get('account_mode')}")
            print(f"balance: {data.get('balance')}")
            print(f"equity: {data.get('equity')}")
            print(f"tick: {data.get('tick')}")
            print(f"open_trades: {data.get('open_trades')}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_live_state()

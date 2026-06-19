import urllib.request
import hmac
import hashlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.config import settings

def test_dashboard_html():
    url = "http://127.0.0.1:8000/"
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
            html_content = response.read().decode('utf-8')
            print("Successfully retrieved HTML.")
            
            # Check for the dynamic elements we added/modified
            print("Checking HTML contents:")
            check_points = [
                'active-floating-pnl',
                'active-symbol-subtext',
                'active-symbol-pair',
                'updateActiveSignalPanel',
                'Floating PnL'
            ]
            for cp in check_points:
                found = cp in html_content
                print(f"- '{cp}' found: {found}")
                
            # Print a snippet of where active-floating-pnl is rendered
            idx = html_content.find('active-floating-pnl')
            if idx != -1:
                print("\nSnippet near active-floating-pnl:")
                print(html_content[idx-150:idx+150])
                
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_dashboard_html()

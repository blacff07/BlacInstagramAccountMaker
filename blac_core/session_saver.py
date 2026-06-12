import json
import os
from datetime import datetime

def save_account(username, password, email, session_id, session_expiry, filename="accounts.json"):
    accounts = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                accounts = json.load(f)
        except:
            pass
    accounts.append({
        "username": username,
        "password": password,
        "email": email,
        "session_id": session_id,
        "session_expiry": session_expiry,
        "created_at": datetime.now().isoformat()
    })
    with open(filename, 'w') as f:
        json.dump(accounts, f, indent=2)
    print(f"[✓] Saved to {filename}")
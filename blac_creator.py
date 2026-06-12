#!/usr/bin/env python3
"""
Blac – Pure HTTP Instagram Account Creator
No browser, no Selenium. Uses requests and extracted CSRF.
"""
import time
import random
import json
import re
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

from blac_core.proxy_manager import rotate_proxy, test_proxy
from blac_core.account_generator import generate_username, generate_fullname
from blac_core.temp_mail import get_temp_email, get_inbox
from blac_core.verif_code import get_instagram_code
from blac_core.session_saver import save_account

def get_shared_data() -> Dict:
    """Fetch shared_data from Instagram signup page."""
    session = requests.Session()
    # mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.instagram.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    })
    resp = session.get("https://www.instagram.com/accounts/emailsignup/")
    resp.raise_for_status()
    html = resp.text
    # Extract window._sharedData
    match = re.search(r'window\._sharedData\s*=\s*({.*?});</script>', html, re.DOTALL)
    if not match:
        raise Exception("Could not find _sharedData")
    data = json.loads(match.group(1))
    csrf = data['config']['csrf_token']
    rollout = data.get('rollout_hash', '')
    return {"csrf": csrf, "rollout": rollout, "cookies": session.cookies.get_dict()}

def generate_client_id() -> str:
    return f"wp-{''.join(random.choices('abcdef0123456789', k=10))}"

def create_account(proxy: Optional[str] = None) -> bool:
    # 1. Fetch shared_data and CSRF
    try:
        shared = get_shared_data()
        csrf = shared['csrf']
        rollout = shared['rollout']
        init_cookies = shared['cookies']
    except Exception as e:
        print(f"[!] Failed to fetch shared_data: {e}")
        return False

    # 2. Create session with proxy
    sess = requests.Session()
    if proxy:
        sess.proxies = {'http': proxy, 'https': proxy}
    sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-CSRFToken': csrf,
        'X-Instagram-AJAX': f"evo-{rollout}-web",
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.instagram.com/accounts/emailsignup/',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    })
    # Set initial cookies from shared_data request
    for name, value in init_cookies.items():
        sess.cookies.set(name, value, domain='.instagram.com')

    # 3. Generate account data
    email = get_temp_email()
    fullname = generate_fullname()
    username = generate_username()
    password = "blac@123"
    ts = int(time.time())
    enc_password = f"#PWD_INSTAGRAM_BROWSER:10:{ts}:6:{password}"
    client_id = generate_client_id()

    data = {
        'email': email,
        'fullname': fullname,
        'username': username,
        'password': password,
        'enc_password': enc_password,
        'client_id': client_id,
        'seamless_login_enabled': '1',
        'tos_version': 'eu',
        'opt_into_one_tap': 'false',
        'use_new_segmenting': '1'
    }

    # 4. POST to signup endpoint
    try:
        resp = sess.post("https://www.instagram.com/accounts/web_create_ajax/", data=data, timeout=15)
        if resp.status_code != 200:
            print(f"[!] HTTP {resp.status_code} – {resp.text[:200]}")
            return False
        result = resp.json()
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return False

    # 5. Handle response
    if result.get('account_created', False):
        print(f"[✓] Account created: {username}")
        # Get session ID from cookies
        session_id = sess.cookies.get('sessionid', '')
        if not session_id:
            # try to extract from response headers? fallback
            pass
        expiry = (datetime.now() + timedelta(days=30)).isoformat()
        save_account(username, password, email, session_id, expiry, "accounts.json")
        return True
    elif result.get('checkpoint_url'):
        print(f"[!] Checkpoint required – account likely created but needs verification: {username}")
        # Could still save? usually not usable.
        return False
    elif 'spam' in str(result).lower():
        print(f"[!] IP flagged as spam. Proxy {proxy} is dead.")
        return False
    else:
        print(f"[?] Unknown response: {result}")
        return False

def main():
    print("Blac – Pure HTTP Instagram Account Creator")
    print("Reading proxies from proxies.txt...")
    # Proxies are handled inside rotate_proxy()
    while True:
        proxy = rotate_proxy()  # returns None or proxy dict
        proxy_str = None
        if proxy:
            # format as http://user:pass@host:port (requests format)
            user = proxy.get('user', '')
            pwd = proxy.get('pass', '')
            if user and pwd:
                proxy_str = f"http://{user}:{pwd}@{proxy['host']}:{proxy['port']}"
            else:
                proxy_str = f"http://{proxy['host']}:{proxy['port']}"
            print(f"[*] Using proxy: {proxy['host']}:{proxy['port']}")
        if create_account(proxy_str):
            delay = random.randint(120, 300)
        else:
            delay = random.randint(60, 120)
        print(f"[*] Waiting {delay}s before next attempt...")
        time.sleep(delay)

if __name__ == "__main__":
    main()
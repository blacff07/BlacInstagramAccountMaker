import requests
import random
import string
import time

def get_temp_email() -> str:
    """Generate a random email address at 1secmail.com."""
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8,12)))
    domain = random.choice(["1secmail.com", "1secmail.org", "1secmail.net"])
    return f"{name}@{domain}"

def get_inbox(email: str) -> list:
    """Fetch inbox messages for a 1secmail email."""
    name, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

def read_message(email: str, msg_id: int) -> dict:
    name, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={name}&domain={domain}&id={msg_id}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return {}
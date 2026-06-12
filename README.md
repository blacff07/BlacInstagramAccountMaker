# Blac – Pure HTTP Instagram Account Creator

**For educational purposes only.**

## Features
- No browser, no Selenium – pure HTTP requests
- Rotating proxies (HTTP/SOCKS5)
- Automatic email verification (1secmail)
- Saves session ID + expiry to `accounts.json`
- Indian names, fixed password `blac@123`

## Installation

```bash
git clone https://github.com/blacff07/BlacInstagramAccountMaker.git
cd BlacInstagramAccountMaker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

1. Create `proxies.txt` – one proxy per line (supports `host:port`, `host:port:user:pass`, or `socks5://user:pass@host:port`)
2. Optional: set `USE_PROXY=true` in `.env` (default false)

## Usage

```bash
python blac_creator.py
```

Output: `accounts.json`

## License

MIT
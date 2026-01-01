import requests

def fetch_json(url: str):
    """Fetch JSON data from a URL and return as dict."""
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

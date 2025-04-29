import os
from binance.um_futures import UMFutures
from dotenv import load_dotenv

def load_client():
    load_dotenv(dotenv_path="API.env")

    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API Key and Secret must be set in API.env")

    client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")
    return client
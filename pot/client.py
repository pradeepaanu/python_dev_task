import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    pass


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key, "Content-Type": "application/json"})

    def _sign_payload(self, params: dict) -> str:
        params_copy = dict(params)
        params_copy["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params_copy, doseq=True)
        signature = hmac.new(self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        params_copy["signature"] = signature
        return urlencode(params_copy, doseq=True)

    def _request(self, method: str, endpoint: str, params=None, signed=False, timeout=15):
        url = f"{self.base_url}{endpoint}"
        payload = params or {}
        if signed:
            signed_query = self._sign_payload(payload)
            url = f"{url}?{signed_query}"
            payload = None

        try:
            response = self.session.request(method, url, timeout=timeout)
            data = response.json()
        except requests.RequestException as exc:
            raise BinanceAPIError(f"Network request failed: {exc}") from exc
        except ValueError:
            raise BinanceAPIError(f"Invalid JSON response from Binance: {response.text}")

        if not response.ok:
            msg = data.get("msg") if isinstance(data, dict) else response.text
            raise BinanceAPIError(f"Binance API error {response.status_code}: {msg}")

        return data

    def create_order(self, symbol: str, side: str, order_type: str, quantity, price=None):
        params = {"symbol": symbol, "side": side, "type": order_type, "quantity": str(quantity)}

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("LIMIT order requires a price")
            params.update({"price": str(price), "timeInForce": "GTC"})

        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

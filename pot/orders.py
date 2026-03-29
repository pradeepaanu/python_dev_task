from .client import BinanceFuturesClient
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price


class OrderManager:
    def __init__(self, client: BinanceFuturesClient, logger=None):
        self.client = client
        self.logger = logger

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str = None):
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity_dec = validate_quantity(quantity)

        price_dec = None
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT orders")
            price_dec = validate_price(price)

        if self.logger:
            self.logger.info("Order request: symbol=%s side=%s type=%s quantity=%s price=%s", symbol, side, order_type, quantity_dec, price_dec)

        response = self.client.create_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity_dec, price=price_dec)

        if self.logger:
            self.logger.info("Order response: %s", response)

        out = {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice", "N/A"),
            "symbol": response.get("symbol"),
            "type": response.get("type"),
            "side": response.get("side"),
        }

        return out

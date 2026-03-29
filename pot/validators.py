from decimal import Decimal, InvalidOperation


def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValueError("symbol is required and must be a string")
    symbol = symbol.strip().upper()
    if not symbol.isalnum() or len(symbol) < 6:
        raise ValueError("symbol must be an alphanumeric Binance symbol (e.g., BTCUSDT)")
    return symbol


def validate_side(side: str) -> str:
    if not side or not isinstance(side, str):
        raise ValueError("side is required and must be BUY or SELL")
    normalized = side.strip().upper()
    if normalized not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    return normalized


def validate_order_type(order_type: str) -> str:
    if not order_type or not isinstance(order_type, str):
        raise ValueError("order type is required and must be MARKET or LIMIT")
    order_type = order_type.strip().upper()
    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError("order type must be MARKET or LIMIT")
    return order_type


def _positive_decimal(value: str, field_name: str) -> Decimal:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} must be a numeric value")
    if d <= 0:
        raise ValueError(f"{field_name} must be greater than 0")
    return d


def validate_quantity(quantity: str) -> Decimal:
    return _positive_decimal(quantity, "quantity")


def validate_price(price: str) -> Decimal:
    return _positive_decimal(price, "price")

import argparse
import os
import sys

from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.logging_config import configure_logger
from bot.orders import OrderManager


def parse_args():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet trading bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, choices=["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, help="Price for LIMIT orders")
    parser.add_argument("--api-key", required=False, help="Binance API key (or set BINANCE_API_KEY)")
    parser.add_argument("--api-secret", required=False, help="Binance API secret (or set BINANCE_API_SECRET)")
    parser.add_argument("--base-url", required=False, default="https://testnet.binancefuture.com", help="Binance Futures base URL")

    return parser.parse_args()


def main():
    logger = configure_logger()

    args = parse_args()

    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API credentials not provided. Use --api-key/--api-secret or BINANCE_API_KEY/BINANCE_API_SECRET")
        print("ERROR: API credentials required")
        sys.exit(1)

    if args.order_type == "LIMIT" and not args.price:
        logger.error("LIMIT order requires --price")
        print("ERROR: LIMIT order requires --price")
        sys.exit(1)

    if args.order_type == "MARKET" and args.price:
        logger.warning("Price is ignored for MARKET order")

    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, base_url=args.base_url)
    order_manager = OrderManager(client, logger)

    try:
        result = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        print("\nOrder request summary")
        print(f"  symbol: {args.symbol}")
        print(f"  side: {args.side}")
        print(f"  type: {args.order_type}")
        print(f"  quantity: {args.quantity}")
        if args.order_type == "LIMIT":
            print(f"  price: {args.price}")

        print("\nOrder response details")
        print(f"  orderId: {result.get('orderId')}")
        print(f"  status: {result.get('status')}")
        print(f"  executedQty: {result.get('executedQty')}")
        print(f"  avgPrice: {result.get('avgPrice')}")

        print("\nSUCCESS: Order executed")

    except BinanceAPIError as exc:
        logger.error("Failed API call: %s", exc)
        print(f"ERROR: Binance API call failed: {exc}")
        sys.exit(2)
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(f"ERROR: Validation failed: {exc}")
        sys.exit(3)
    except Exception as exc:
        logger.error("Unexpected error: %s", exc, exc_info=True)
        print(f"ERROR: Unexpected error: {exc}")
        sys.exit(99)


if __name__ == "__main__":
    main()

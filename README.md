# Binance Futures Testnet Trading Bot (Simplified)

## Overview
A small Python CLI trading bot that places MARKET and LIMIT orders on Binance Futures Testnet (USDT-M), with structured code, logging, input validation, and error handling.

## Structure
- `bot/client.py`: Binance API wrapper with signature and request handling
- `bot/orders.py`: order placement business logic and response extraction
- `bot/validators.py`: input validation for symbol, side, type, quantity, price
- `bot/logging_config.py`: logger configuration to file and console
- `cli.py`: CLI entrypoint using `argparse`
- `requirements.txt`: dependencies

## Setup
1. Create and activate Python 3.10+ environment
2. `cd trading_bot`
3. `pip install -r requirements.txt`

### Credentials
Set environment variables or pass CLI arguments:
- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`

## Run examples
### Market order
```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit order
```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

## Notes
- Uses Testnet base URL by default: `https://testnet.binancefuture.com`
- LIMIT orders include `timeInForce=GTC`
- `price` is required for LIMIT, optional/ignored for MARKET

## Logging
- Logs to `logs/trading_bot.log`
- Includes request summary, API response, and errors

## Assumptions
- User provides valid API credentials
- Quantity and price precision are sufficient for test values
- API response keys are in standard Binance format

## Deliverables artifacts (this repo)
- Source code and README
- `logs/market_order.log`, `logs/limit_order.log` (sample logged output)

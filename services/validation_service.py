import ccxt
import asyncio

def validate_exchange(exchange: str):
    """Validate that the provided exchange is supported by CCXT.

    Raises an Exception when the exchange is not supported.
    """
    if exchange not in ccxt.exchanges:
        raise Exception(f"Exchange '{exchange}' not supported.")

async def validate_symbol(exchange: str, symbol: str):
    """Validate that a symbol exists for a given exchange.

    Uses a synchronous CCXT exchange instance to load market metadata and
    confirm that the symbol is listed. Raises an Exception on failure.
    """
    # Use sync CCXT here because only market meta needed
    try:
        ex_class = getattr(ccxt, exchange)
        ex_instance = ex_class()
        markets = ex_instance.load_markets()
        if symbol not in markets:
            raise Exception(f"Symbol '{symbol}' not supported for exchange '{exchange}'")
    except Exception:
        raise Exception(f"Invalid exchange-symbol pair {exchange}:{symbol}")
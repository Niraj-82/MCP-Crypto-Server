import ccxt.async_support as ccxt
import ccxt
import asyncio
import logging

from services.cache_service import cache
from services.validation_service import validate_exchange, validate_symbol
from config import settings

logger = logging.getLogger("exchange_client")

class ExchangeClient:
    """Client wrapper around CCXT exchanges providing cached async data fetches.

    This class lazily initializes ccxt async exchange instances and exposes
    convenience methods to fetch ticker, order book, trades and OHLCV data
    with caching and retry logic.
    """

    _EXCHANGE_INSTANCES = {}

    @staticmethod
    async def get_exchange_instance(exchange: str):
        """Return a cached ccxt async exchange instance, creating it if needed.

        Args:
            exchange: Exchange id string (e.g., 'binance').

        Returns:
            An instantiated ccxt async exchange object.
        """
        if exchange in ExchangeClient._EXCHANGE_INSTANCES:
            return ExchangeClient._EXCHANGE_INSTANCES[exchange]
        try:
            ex_class = getattr(ccxt, exchange)
            ex_instance = ex_class({'enableRateLimit': True, 'rateLimit': 1200})
            ExchangeClient._EXCHANGE_INSTANCES[exchange] = ex_instance
            return ex_instance
        except AttributeError:
            raise Exception(f"Exchange '{exchange}' not supported in CCXT.")

    @staticmethod
    async def get_ticker_price(exchange: str, symbol: str):
        """Fetch the latest ticker price for a symbol on an exchange.

        Validates inputs, checks cache and attempts network fetch with retries.

        Args:
            exchange: Exchange name (e.g., 'binance').
            symbol: Trading pair symbol in CCXT format (e.g., 'BTC/USDT').

        Returns:
            Dict containing exchange, symbol, price and timestamp.
        """
        validate_exchange(exchange)
        await validate_symbol(exchange, symbol)
        cache_key = f"ticker:{exchange}:{symbol}"
        if result := cache.get(cache_key):
            return result
        ex = await ExchangeClient.get_exchange_instance(exchange)
        attempts = 0
        while attempts < 3:
            try:
                ticker = await ex.fetch_ticker(symbol)
                result = {
                    "exchange": exchange,
                    "symbol": symbol,
                    "price": ticker["last"],
                    "timestamp": ticker["timestamp"] // 1000 if ticker["timestamp"] else 0,
                }
                cache.set(cache_key, result, ttl=settings.CACHE_TTL)
                return result
            except Exception as e:
                logger.warning(f"Fetch ticker retry {attempts + 1} error: {e}")
                attempts += 1
                await asyncio.sleep(0.75 * attempts)
        raise Exception(f"Could not fetch ticker for {exchange}:{symbol}")

    @staticmethod
    async def get_order_book(exchange: str, symbol: str, limit: int = 20):
        """Fetch the order book for a given symbol with configurable depth.

        Args:
            exchange: Exchange identifier.
            symbol: Trading pair symbol.
            limit: Depth limit for bids/asks (default 20).

        Returns:
            Dict containing exchange, symbol, bids, asks and timestamp.
        """
        validate_exchange(exchange)
        await validate_symbol(exchange, symbol)
        cache_key = f"orderbook:{exchange}:{symbol}:{limit}"
        if result := cache.get(cache_key):
            return result
        ex = await ExchangeClient.get_exchange_instance(exchange)
        attempts = 0
        while attempts < 3:
            try:
                orderbook = await ex.fetch_order_book(symbol, limit)
                result = {
                    "exchange": exchange,
                    "symbol": symbol,
                    "bids": orderbook.get("bids", []),
                    "asks": orderbook.get("asks", []),
                    "timestamp": orderbook.get("timestamp", 0) // 1000 if orderbook.get("timestamp") else 0,
                }
                cache.set(cache_key, result, ttl=settings.CACHE_TTL)
                return result
            except Exception as e:
                logger.warning(f"Fetch orderbook retry {attempts + 1} error: {e}")
                attempts += 1
                await asyncio.sleep(0.75 * attempts)
        raise Exception(f"Could not fetch order book for {exchange}:{symbol}")

    @staticmethod
    async def get_trade_history(exchange: str, symbol: str, limit: int = 20):
        """Fetch recent trade history for a symbol.

        Args:
            exchange: Exchange identifier.
            symbol: Trading pair symbol.
            limit: Maximum number of trades to return.

        Returns:
            Dict with exchange, symbol and a list of trade items.
        """
        validate_exchange(exchange)
        await validate_symbol(exchange, symbol)
        cache_key = f"tradehistory:{exchange}:{symbol}:{limit}"
        if result := cache.get(cache_key):
            return result
        ex = await ExchangeClient.get_exchange_instance(exchange)
        attempts = 0
        while attempts < 3:
            try:
                trades = await ex.fetch_trades(symbol, limit=limit)
                trade_items = []
                for t in trades[:limit]:
                    trade_items.append({
                        "price": t["price"],
                        "amount": t["amount"],
                        "side": t.get("side", ""),
                        "timestamp": t["timestamp"] // 1000 if t["timestamp"] else 0,
                        "trade_id": str(t.get("id", "")),
                    })
                result = {
                    "exchange": exchange,
                    "symbol": symbol,
                    "trades": trade_items,
                }
                cache.set(cache_key, result, ttl=settings.CACHE_TTL)
                return result
            except Exception as e:
                logger.warning(f"Fetch trades retry {attempts + 1} error: {e}")
                attempts += 1
                await asyncio.sleep(0.75 * attempts)
        raise Exception(f"Could not fetch trades for {exchange}:{symbol}")

    @staticmethod
    async def get_ohlcv(
        exchange: str,
        symbol: str,
        interval: str,
        start_timestamp: int = None,
        end_timestamp: int = None,
        limit: int = 100,
    ):
        """Fetch OHLCV (candlestick) data for a symbol.

        Args:
            exchange: Exchange identifier.
            symbol: Trading pair symbol.
            interval: Timeframe string supported by CCXT (e.g., '1m', '1h').
            start_timestamp: Optional start time (seconds since epoch).
            end_timestamp: Optional end time (seconds since epoch).
            limit: Maximum number of candles to fetch.

        Returns:
            Dict containing exchange, symbol, interval and ohlcv list.
        """
        validate_exchange(exchange)
        await validate_symbol(exchange, symbol)
        if interval not in ['1m', '5m', '15m', '30m', '1h', '4h', '1d']:
            raise Exception(f"Interval '{interval}' not supported.")
        cache_key = f"ohlcv:{exchange}:{symbol}:{interval}:{start_timestamp}:{end_timestamp}:{limit}"
        if result := cache.get(cache_key):
            return result
        ex = await ExchangeClient.get_exchange_instance(exchange)
        attempts = 0
        since = start_timestamp * 1000 if start_timestamp else None
        while attempts < 3:
            try:
                ohlcv = await ex.fetch_ohlcv(symbol, timeframe=interval, since=since, limit=limit)
                # If end_timestamp is set, filter after fetch
                if end_timestamp:
                    ohlcv = [row for row in ohlcv if row[0] // 1000 <= end_timestamp]
                items = []
                for row in ohlcv:
                    items.append(
                        {
                            "timestamp": row[0] // 1000,
                            "open": row[1],
                            "high": row[2],
                            "low": row[3],
                            "close": row[4],
                            "volume": row[5],
                        }
                    )
                result = {
                    "exchange": exchange,
                    "symbol": symbol,
                    "interval": interval,
                    "ohlcv": items,
                }
                cache.set(cache_key, result, ttl=settings.CACHE_TTL)
                return result
            except Exception as e:
                logger.warning(f"Fetch OHLCV retry {attempts + 1} error: {e}")
                attempts += 1
                await asyncio.sleep(0.75 * attempts)
        raise Exception(f"Could not fetch OHLCV for {exchange}:{symbol}:{interval}")

    @staticmethod
    async def get_supported_exchanges():
        """Return the list of exchanges supported by CCXT."""
        return ccxt.exchanges

    @staticmethod
    async def get_symbols(exchange: str):
        """Return a list of tradable symbols for the given exchange.

        Results are cached for a longer TTL since symbols change infrequently.
        """
        validate_exchange(exchange)
        cache_key = f"symbols:{exchange}"
        if result := cache.get(cache_key):
            return result
        ex = await ExchangeClient.get_exchange_instance(exchange)
        markets = await ex.load_markets()
        symbols = list(markets.keys())
        cache.set(cache_key, symbols, ttl=300)
        return symbols
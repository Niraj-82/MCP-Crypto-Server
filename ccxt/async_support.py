
exchanges = ["binance", "kraken", "coinbase"]

class BaseExchange:
    def __init__(self, id):
        self.id = id
        self.markets = {"BTC/USDT": {"symbol":"BTC/USDT"}, "ETH/USDT":{"symbol":"ETH/USDT"}}
    async def load_markets(self):
        return self.markets
    async def fetch_ticker(self, symbol):
        return {"symbol": symbol, "last": 10000.0, "timestamp": 1600000000}
    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None):
        # return list of [timestamp, open, high, low, close, volume]
        return [
            [1600000000, 10000, 10050, 9950, 10020, 15.0],
            [1600000060, 10020, 10060, 9990, 10030, 20.0],
        ][:limit or 2]
    async def fetch_order_book(self, symbol, depth=10):
        return {"bids": [[10000,1]], "asks": [[10010,1]], "timestamp":1600000000}
    async def fetch_trades(self, symbol, limit=10):
        return [
            {"price":10000,"amount":0.5,"side":"buy","timestamp":1600000000,"id":"1"},
            {"price":9998,"amount":0.25,"side":"sell","timestamp":1600000100,"id":"2"},
        ][:limit]
    async def close(self):
        pass

# factory mapping
_exchange_classes = {}

def __getattr__(name):
    # support attribute access like binance()
    raise AttributeError

def exchange_class_for(id):
    return BaseExchange

# mimic module-level newExchange creation
def exchange(id):
    return BaseExchange(id)

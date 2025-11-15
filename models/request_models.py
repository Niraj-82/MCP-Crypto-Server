from pydantic import BaseModel, Field
from typing import Optional

class TickerRequest(BaseModel):
    exchange: str = Field(..., description="Exchange name (e.g., binance)")
    symbol: str = Field(..., description="Symbol in exchange format (e.g., BTC/USDT)")

class OrderBookRequest(BaseModel):
    exchange: str
    symbol: str
    limit: Optional[int] = 20

class TradeHistoryRequest(BaseModel):
    exchange: str
    symbol: str
    limit: Optional[int] = 20

class OHLCVRequest(BaseModel):
    exchange: str
    symbol: str
    interval: str  # e.g., "1m", "5m", "1h", "1d"
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    limit: Optional[int] = 100

class ValidationRequest(BaseModel):
    exchange: str
    symbol: str
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TickerResponse(BaseModel):
    exchange: str
    symbol: str
    price: float
    timestamp: int

class OrderBookResponse(BaseModel):
    exchange: str
    symbol: str
    bids: List[List[float]]
    asks: List[List[float]]
    timestamp: int

class TradeItem(BaseModel):
    price: float
    amount: float
    side: str
    timestamp: int
    trade_id: str

class TradeHistoryResponse(BaseModel):
    exchange: str
    symbol: str
    trades: List[TradeItem]

class OHLCVItem(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

class OHLCVResponse(BaseModel):
    exchange: str
    symbol: str
    interval: str
    ohlcv: List[OHLCVItem]

class ExchangeListResponse(BaseModel):
    exchanges: List[str]

class SymbolListResponse(BaseModel):
    exchange: str
    symbols: List[str]

class ValidationResponse(BaseModel):
    valid: bool
    detail: str

class ServerStatusResponse(BaseModel):
    status: str
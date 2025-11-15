from fastapi import APIRouter, HTTPException
from models.request_models import (
    TickerRequest, OrderBookRequest, TradeHistoryRequest
)
from models.response_models import (
    TickerResponse, OrderBookResponse, TradeHistoryResponse
)
from services.exchange_client import ExchangeClient
from realtime.websocket_handler import stream_prices
from pydantic import BaseModel
from fastapi import WebSocket

class StreamResponse(BaseModel):
    prices: dict[str, float]

router = APIRouter()

@router.post("/ticker", response_model=TickerResponse)
async def get_ticker_price(request: TickerRequest):
    try:
        data = await ExchangeClient.get_ticker_price(request.exchange, request.symbol)
        return TickerResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/order_book", response_model=OrderBookResponse)
async def get_order_book(request: OrderBookRequest):
    try:
        data = await ExchangeClient.get_order_book(request.exchange, request.symbol, request.limit)
        return OrderBookResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/trades", response_model=TradeHistoryResponse)
async def get_trade_history(request: TradeHistoryRequest):
    try:
        data = await ExchangeClient.get_trade_history(request.exchange, request.symbol, request.limit)
        return TradeHistoryResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.websocket("/stream_prices")
async def websocket_stream_prices(websocket: WebSocket):
    await websocket.accept()
    try:
        async def callback(prices):
            await websocket.send_json(StreamResponse(prices=prices).dict())
        await stream_prices(callback)
    except Exception as e:
        await websocket.close(code=1000)

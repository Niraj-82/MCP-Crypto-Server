from fastapi import APIRouter, HTTPException
from models.request_models import OHLCVRequest
from models.response_models import OHLCVResponse
from services.exchange_client import ExchangeClient
from analytics.indicators import sma, ema
from pydantic import BaseModel

class IndicatorRequest(BaseModel):
    exchange: str
    symbol: str
    interval: str
    period: int = 14
    limit: int = 100

class IndicatorResponse(BaseModel):
    exchange: str
    symbol: str
    interval: str
    period: int
    values: list[float]

router = APIRouter()

@router.post("/ohlcv", response_model=OHLCVResponse)
async def get_ohlcv(request: OHLCVRequest):
    try:
        data = await ExchangeClient.get_ohlcv(
            request.exchange,
            request.symbol,
            request.interval,
            request.start_timestamp,
            request.end_timestamp,
            request.limit,
        )
        return OHLCVResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sma", response_model=IndicatorResponse)
async def get_sma(request: IndicatorRequest):
    try:
        # Fetch OHLCV data first
        ohlcv_data = await ExchangeClient.get_ohlcv(
            request.exchange,
            request.symbol,
            request.interval,
            limit=request.limit,
        )
        import pandas as pd
        df = pd.DataFrame(ohlcv_data['ohlcv'])
        sma_values = sma(df, request.period).dropna().tolist()
        return IndicatorResponse(
            exchange=request.exchange,
            symbol=request.symbol,
            interval=request.interval,
            period=request.period,
            values=sma_values
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ema", response_model=IndicatorResponse)
async def get_ema(request: IndicatorRequest):
    try:
        # Fetch OHLCV data first
        ohlcv_data = await ExchangeClient.get_ohlcv(
            request.exchange,
            request.symbol,
            request.interval,
            limit=request.limit,
        )
        import pandas as pd
        df = pd.DataFrame(ohlcv_data['ohlcv'])
        ema_values = ema(df, request.period).dropna().tolist()
        return IndicatorResponse(
            exchange=request.exchange,
            symbol=request.symbol,
            interval=request.interval,
            period=request.period,
            values=ema_values
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

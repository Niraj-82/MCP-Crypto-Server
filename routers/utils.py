from fastapi import APIRouter, HTTPException
from models.request_models import ValidationRequest
from models.response_models import (
    ExchangeListResponse,
    SymbolListResponse,
    ValidationResponse,
    ServerStatusResponse,
)
from config import settings
from services.exchange_client import ExchangeClient
from services.validation_service import validate_exchange, validate_symbol
from analytics.portfolio import calculate_portfolio_value
from pydantic import BaseModel

class PortfolioRequest(BaseModel):
    prices: dict[str, float]
    holdings: dict[str, float]

class PortfolioResponse(BaseModel):
    value: float

router = APIRouter()

@router.get("/exchanges", response_model=ExchangeListResponse)
async def list_supported_exchanges():
    exchanges = await ExchangeClient.get_supported_exchanges()
    return ExchangeListResponse(exchanges=exchanges)

@router.get("/symbols/{exchange}", response_model=SymbolListResponse)
async def list_symbols(exchange: str):
    try:
        symbols = await ExchangeClient.get_symbols(exchange)
        return SymbolListResponse(exchange=exchange, symbols=symbols)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate", response_model=ValidationResponse)
async def validate_exchange_symbol_pair(request: ValidationRequest):
    try:
        validate_exchange(request.exchange)
        await validate_symbol(request.exchange, request.symbol)
        return ValidationResponse(valid=True, detail="Valid exchange-symbol pair")
    except Exception as e:
        return ValidationResponse(valid=False, detail=str(e))

@router.get("/status", response_model=ServerStatusResponse)
async def server_status():
    return ServerStatusResponse(status=settings.MCP_SERVER_STATUS)

@router.post("/portfolio_value", response_model=PortfolioResponse)
async def get_portfolio_value(request: PortfolioRequest):
    try:
        value = calculate_portfolio_value(request.prices, request.holdings)
        return PortfolioResponse(value=value)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

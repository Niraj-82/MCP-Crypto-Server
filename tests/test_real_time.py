import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_ticker_price(mocker):
    fake_ticker = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "price": 10000.0,
        "timestamp": 1600000000,
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_ticker_price",
        return_value=fake_ticker
    )
    response = client.post(
        "/api/v1/real_time/ticker",
        json={"exchange": "binance", "symbol": "BTC/USDT"}
    )
    assert response.status_code == 200
    assert response.json()["price"] == 10000.0

@pytest.mark.asyncio
async def test_get_order_book(mocker):
    fake_order_book = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "bids": [[10000, 1], [9999, 2]],
        "asks": [[10001, 1.5], [10002, 1]],
        "timestamp": 1600000000,
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_order_book",
        return_value=fake_order_book
    )
    response = client.post(
        "/api/v1/real_time/order_book",
        json={"exchange": "binance", "symbol": "BTC/USDT", "limit": 2}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data["bids"]) == 2
    assert len(json_data["asks"]) == 2

@pytest.mark.asyncio
async def test_get_trade_history(mocker):
    fake_trade_history = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "trades": [
            {"price": 10000, "amount": 0.5, "side": "buy", "timestamp": 1600000000, "trade_id": "1"},
            {"price": 9998, "amount": 0.25, "side": "sell", "timestamp": 1600000100, "trade_id": "2"},
        ],
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_trade_history",
        return_value=fake_trade_history
    )
    response = client.post(
        "/api/v1/real_time/trades",
        json={"exchange": "binance", "symbol": "BTC/USDT", "limit": 2}
    )
    assert response.status_code == 200
    assert len(response.json()["trades"]) == 2
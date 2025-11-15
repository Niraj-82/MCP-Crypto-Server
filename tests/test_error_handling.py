import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_error_bad_exchange(mocker):
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_ticker_price",
        side_effect=Exception("Exchange 'badex' not supported.")
    )
    response = client.post(
        "/api/v1/real_time/ticker",
        json={"exchange": "badex", "symbol": "BTC/USDT"}
    )
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]

def test_error_bad_symbol(mocker):
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_order_book",
        side_effect=Exception("Symbol 'FOO/BAR' not supported for exchange 'binance'")
    )
    response = client.post(
        "/api/v1/real_time/order_book",
        json={"exchange": "binance", "symbol": "FOO/BAR"}
    )
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]

def test_exception_handler():
    response = client.post(
        "/api/v1/real_time/ticker",
        json={"exchange": "binance", "symbol": None}
    )
    assert response.status_code == 400 or response.status_code == 500
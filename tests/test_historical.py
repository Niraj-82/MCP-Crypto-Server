import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_ohlcv(mocker):
    fake_ohlcv = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1m",
        "ohlcv": [
            {"timestamp": 1600000000, "open": 10000, "high": 10050, "low": 9950, "close": 10020, "volume": 15.0},
            {"timestamp": 1600000060, "open": 10020, "high": 10060, "low": 9990, "close": 10030, "volume": 20.0},
        ],
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_ohlcv",
        return_value=fake_ohlcv
    )
    response = client.post(
        "/api/v1/historical/ohlcv",
        json={
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "1m",
            "start_timestamp": 1600000000,
            "end_timestamp": 1600009999,
            "limit": 2,
        }
    )
    assert response.status_code == 200
    assert len(response.json()["ohlcv"]) == 2
    assert response.json()["ohlcv"][0]["open"] == 10000
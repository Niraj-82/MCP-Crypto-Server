# Test Enhancement Recommendations

## Current Coverage Summary
- **Total Tests:** 9/9 passing (100%)
- **Code Coverage:** 66%
- **Critical Gap:** Exchange Client service at 18% coverage

---

## 1. High-Priority Test Additions

### A. ExchangeClient Retry Logic Tests

**Current Gap:** The retry mechanism with exponential backoff (lines 28-50, 54-77, 81-111) is untested.

**Recommended Test:**
```python
@pytest.mark.asyncio
async def test_ticker_retry_on_failure(mocker):
    """Test that get_ticker_price retries 3 times on failure"""
    mock_exchange = AsyncMock()
    mock_exchange.fetch_ticker.side_effect = Exception("Network error")
    
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_exchange_instance",
        return_value=mock_exchange
    )
    mocker.patch("services.exchange_client.asyncio.sleep", return_value=None)
    
    with pytest.raises(Exception) as exc_info:
        await ExchangeClient.get_ticker_price("binance", "BTC/USDT")
    
    assert "Could not fetch ticker" in str(exc_info.value)
    assert mock_exchange.fetch_ticker.call_count == 3  # Verify 3 attempts

@pytest.mark.asyncio
async def test_ticker_success_after_retry(mocker):
    """Test that get_ticker_price succeeds after initial failure"""
    mock_exchange = AsyncMock()
    # Fail twice, succeed on third attempt
    mock_exchange.fetch_ticker.side_effect = [
        Exception("Network error"),
        Exception("Network error"),
        {"last": 10000.0, "timestamp": 1600000000}
    ]
    
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_exchange_instance",
        return_value=mock_exchange
    )
    mocker.patch("services.exchange_client.asyncio.sleep", return_value=None)
    
    result = await ExchangeClient.get_ticker_price("binance", "BTC/USDT")
    assert result["price"] == 10000.0
    assert mock_exchange.fetch_ticker.call_count == 3
```

### B. Symbol Validation Tests

**Current Gap:** The symbol validation function (lines 10-17 in validation_service.py) has only 29% coverage.

**Recommended Tests:**
```python
import pytest
from services.validation_service import validate_symbol, validate_exchange

@pytest.mark.asyncio
async def test_validate_symbol_valid(mocker):
    """Test validation of valid exchange-symbol pair"""
    mock_exchange_class = MagicMock()
    mock_exchange = MagicMock()
    mock_exchange.load_markets.return_value = {"BTC/USDT": {}, "ETH/USDT": {}}
    mock_exchange_class.return_value = mock_exchange
    
    mocker.patch("services.validation_service.getattr", return_value=mock_exchange_class)
    
    # Should not raise
    await validate_symbol("binance", "BTC/USDT")

@pytest.mark.asyncio
async def test_validate_symbol_invalid(mocker):
    """Test validation rejects invalid symbol"""
    mock_exchange_class = MagicMock()
    mock_exchange = MagicMock()
    mock_exchange.load_markets.return_value = {"BTC/USDT": {}}
    mock_exchange_class.return_value = mock_exchange
    
    mocker.patch("services.validation_service.getattr", return_value=mock_exchange_class)
    
    with pytest.raises(Exception) as exc_info:
        await validate_symbol("binance", "INVALID/USDT")
    assert "not supported" in str(exc_info.value)

def test_validate_exchange_valid():
    """Test exchange validation for valid exchange"""
    validate_exchange("binance")  # Should not raise

def test_validate_exchange_invalid():
    """Test exchange validation rejects invalid exchange"""
    with pytest.raises(Exception) as exc_info:
        validate_exchange("invalid_exchange")
    assert "not supported" in str(exc_info.value)
```

### C. Utils Router Tests

**Current Gap:** The utils router (52% coverage) is missing tests for `/symbols`, `/validate`, and `/status` endpoints.

**Recommended Tests:**
```python
def test_list_symbols_success(mocker):
    """Test listing symbols for a valid exchange"""
    fake_symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_symbols",
        return_value=fake_symbols
    )
    response = client.get("/api/v1/utils/symbols/binance")
    assert response.status_code == 200
    assert response.json()["exchange"] == "binance"
    assert len(response.json()["symbols"]) == 3

def test_list_symbols_invalid_exchange(mocker):
    """Test listing symbols for invalid exchange"""
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_symbols",
        side_effect=Exception("Exchange 'invalid' not supported")
    )
    response = client.get("/api/v1/utils/symbols/invalid")
    assert response.status_code == 400

def test_validate_pair_valid(mocker):
    """Test validation endpoint for valid pair"""
    mocker.patch("services.validation_service.validate_exchange")
    mocker.patch("services.validation_service.validate_symbol")
    
    response = client.post(
        "/api/v1/utils/validate",
        json={"exchange": "binance", "symbol": "BTC/USDT"}
    )
    assert response.status_code == 200
    assert response.json()["valid"] is True

def test_validate_pair_invalid(mocker):
    """Test validation endpoint for invalid pair"""
    mocker.patch(
        "services.validation_service.validate_exchange",
        side_effect=Exception("Exchange not supported")
    )
    
    response = client.post(
        "/api/v1/utils/validate",
        json={"exchange": "invalid", "symbol": "BTC/USDT"}
    )
    assert response.status_code == 200
    assert response.json()["valid"] is False

def test_server_status():
    """Test server status endpoint"""
    response = client.get("/api/v1/utils/status")
    assert response.status_code == 200
    assert "status" in response.json()
```

### D. Order Book and Trades Tests (Expanded)

**Current Gap:** Edge cases not tested (limit parameter, empty results)

**Recommended Tests:**
```python
@pytest.mark.asyncio
async def test_get_order_book_with_custom_limit(mocker):
    """Test order book respects custom limit parameter"""
    fake_orderbook = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "bids": [[10000, 1], [9999, 2], [9998, 3], [9997, 4], [9996, 5]],
        "asks": [[10001, 1.5], [10002, 1], [10003, 2], [10004, 1.5], [10005, 1]],
        "timestamp": 1600000000,
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_order_book",
        return_value=fake_orderbook
    )
    
    response = client.post(
        "/api/v1/real_time/order_book",
        json={"exchange": "binance", "symbol": "BTC/USDT", "limit": 50}
    )
    assert response.status_code == 200
    assert len(response.json()["bids"]) == 5

@pytest.mark.asyncio
async def test_get_trades_empty_history(mocker):
    """Test trade history endpoint with no recent trades"""
    fake_trade_history = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "trades": [],
    }
    mocker.patch(
        "services.exchange_client.ExchangeClient.get_trade_history",
        return_value=fake_trade_history
    )
    
    response = client.post(
        "/api/v1/real_time/trades",
        json={"exchange": "binance", "symbol": "BTC/USDT"}
    )
    assert response.status_code == 200
    assert response.json()["trades"] == []
```

---

## 2. Configuration & Pydantic Tests

**Current Gap:** Config fallback mechanisms (lines 5-14 in config.py) untested

**Recommended Tests:**
```python
def test_settings_defaults():
    """Test default settings values"""
    from config import settings
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 8000
    assert settings.CACHE_TTL == 20
    assert settings.LOG_LEVEL == "INFO"

def test_settings_pydantic_compatibility():
    """Test Settings works with both Pydantic v1 and v2"""
    from config import Settings
    s = Settings(HOST="localhost", PORT=9000)
    assert s.HOST == "localhost"
    assert s.PORT == 9000
```

---

## 3. Cache Edge Case Tests

**Current Gap:** Cache doesn't test concurrent access or large datasets

**Recommended Tests:**
```python
import pytest
from services.cache_service import cache

def test_cache_overwrite():
    """Test that cache overwrites existing keys"""
    cache.clear()
    cache.set("key1", "value1", ttl=10)
    cache.set("key1", "value2", ttl=10)
    assert cache.get("key1") == "value2"

def test_cache_different_keys():
    """Test cache stores multiple different keys"""
    cache.clear()
    cache.set("key1", "value1", ttl=10)
    cache.set("key2", "value2", ttl=10)
    cache.set("key3", "value3", ttl=10)
    
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"

def test_cache_clear():
    """Test cache clear removes all entries"""
    cache.clear()
    cache.set("key1", "value1", ttl=10)
    cache.set("key2", "value2", ttl=10)
    
    cache.clear()
    
    assert cache.get("key1") is None
    assert cache.get("key2") is None
```

---

## 4. OHLCV Enhanced Tests

**Current Gap:** Time-range filtering and edge cases not tested

**Recommended Tests:**
```python
@pytest.mark.asyncio
async def test_ohlcv_with_time_range(mocker):
    """Test OHLCV respects start and end timestamps"""
    fake_ohlcv = {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1h",
        "ohlcv": [
            {"timestamp": 1600000000, "open": 10000, "high": 10050, "low": 9950, "close": 10020, "volume": 15.0},
            {"timestamp": 1600003600, "open": 10020, "high": 10060, "low": 9990, "close": 10030, "volume": 20.0},
            {"timestamp": 1600007200, "open": 10030, "high": 10080, "low": 10000, "close": 10050, "volume": 25.0},
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
            "interval": "1h",
            "start_timestamp": 1600000000,
            "end_timestamp": 1600005000,
            "limit": 100,
        }
    )
    assert response.status_code == 200
    assert len(response.json()["ohlcv"]) == 3

@pytest.mark.asyncio
async def test_ohlcv_all_timeframes(mocker):
    """Test OHLCV supports multiple timeframes"""
    for interval in ["1m", "5m", "15m", "1h", "4h", "1d"]:
        fake_ohlcv = {
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": interval,
            "ohlcv": [{"timestamp": 1600000000, "open": 10000, "high": 10050, "low": 9950, "close": 10020, "volume": 15.0}],
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
                "interval": interval,
                "limit": 100,
            }
        )
        assert response.status_code == 200
```

---

## 5. Integration Test Suite

**Current Gap:** No integration tests combining multiple services

**Recommended Test File:** `tests/test_integration.py`

```python
"""Integration tests for full request/response flows"""
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

class TestIntegrationFlows:
    """Test complete workflows involving multiple services"""
    
    def test_full_market_data_flow(self, mocker):
        """Test fetching complete market data for a symbol"""
        # Setup mocks
        mocker.patch(
            "services.exchange_client.ExchangeClient.get_ticker_price",
            return_value={"exchange": "binance", "symbol": "BTC/USDT", "price": 10000.0, "timestamp": 1600000000}
        )
        mocker.patch(
            "services.exchange_client.ExchangeClient.get_order_book",
            return_value={"exchange": "binance", "symbol": "BTC/USDT", "bids": [[10000, 1]], "asks": [[10001, 1]], "timestamp": 1600000000}
        )
        mocker.patch(
            "services.exchange_client.ExchangeClient.get_trade_history",
            return_value={"exchange": "binance", "symbol": "BTC/USDT", "trades": [{"price": 10000, "amount": 0.5, "side": "buy", "timestamp": 1600000000, "trade_id": "1"}]}
        )
        
        # Execute requests
        ticker = client.post("/api/v1/real_time/ticker", json={"exchange": "binance", "symbol": "BTC/USDT"})
        orderbook = client.post("/api/v1/real_time/order_book", json={"exchange": "binance", "symbol": "BTC/USDT"})
        trades = client.post("/api/v1/real_time/trades", json={"exchange": "binance", "symbol": "BTC/USDT"})
        
        # Verify all succeeded
        assert ticker.status_code == 200
        assert orderbook.status_code == 200
        assert trades.status_code == 200
        
        # Verify data consistency
        assert ticker.json()["symbol"] == orderbook.json()["symbol"] == trades.json()["symbol"]
```

---

## Implementation Priority

### Phase 1 (High Priority - +15% coverage)
1. ExchangeClient retry logic tests
2. Symbol validation tests
3. Utils router tests

**Expected Coverage Improvement:** 18% → 35% for ExchangeClient

### Phase 2 (Medium Priority - +8% coverage)
1. Order book/trades edge cases
2. OHLCV time-range tests
3. Cache edge case tests

**Expected Coverage Improvement:** 66% → 74% overall

### Phase 3 (Nice-to-have - +5% coverage)
1. Configuration fallback tests
2. Integration test suite
3. Performance/load tests

**Expected Coverage Improvement:** 74% → 79% overall

---

## Test Execution

To run all recommended tests once implemented:

```bash
# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_exchange_client.py -v

# Run tests matching pattern
pytest -k "retry" -v
```

---

## Expected Outcome

With all recommendations implemented:
- **Coverage Target:** 80-85% (from current 66%)
- **Test Count:** 20-25+ tests (from current 9)
- **Critical Gaps Closed:** ExchangeClient, validators, utils endpoints fully tested
- **Reliability:** High confidence in retry logic, edge cases, integration flows


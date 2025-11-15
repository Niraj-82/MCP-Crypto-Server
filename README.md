# MCP Crypto Server

Production-Grade Python MCP Server for Real-Time & Historical Cryptocurrency Market Data

---

## 🚀 Overview
A high-performance, non-blocking server for retrieving real-time and historical cryptocurrency market data, supporting multi-exchange operation via CCXT.

### Features
- Real-time price, order book, and trade history
- Historical OHLCV data (any interval)
- Utility endpoints: supported exchanges, symbols, status
- FastAPI-driven API, async throughout
- In-memory caching for low-latency/multi-client performance
- Robust error handling & schema validation via Pydantic
- Logging and retries for resiliency
- Full test coverage using pytest (mocks CCXT APIs)

---

## 📦 Project Structure

MCP Crypto Server — README
📌 Overview

The MCP Crypto Server is a fully asynchronous, production-ready backend service designed to retrieve and analyze cryptocurrency market data from 70+ exchanges using CCXT.
It supports:

Real-time market data

Historical OHLCV data

Technical indicators

Portfolio analytics

Streaming prototype

Caching, validation, retry logic, and rate limiting

Designed for AI agents, trading bots, analytics dashboards, and financial research tools.

🧠 Approach

This project was built using a modular, scalable, and production-inspired architecture:

✔ 1. Layered Architecture

Routers → Handle API endpoints

Services → Business logic (data fetching, caching, validation)

Models → Request/response schemas

Analytics → Indicators + portfolio logic

Streaming → Real-time data prototype

Config → Environment control

This separation ensures maintainability and easy extensibility.

✔ 2. Asynchronous Design

All API functions use async/await, ensuring:

High throughput

Non-blocking execution

Efficient handling of multiple clients

CCXT’s async_support module is used for all exchange operations.

✔ 3. Reliability First

Market APIs fail often, so the server includes:

Retry logic (3 attempts, exponential backoff)

Global error handlers

Validation for exchange/symbol correctness

Structured logging for debugging

✔ 4. Performance Optimizations

To avoid API rate-limit issues and reduce latency:

TTL-based in-memory caching

Rate limiter

Reuse of CCXT exchange instances

Lighter responses and faster execution

✔ 5. Expandability

The project is designed so new indicators, analytics modules, or streaming features can be added with minimal changes.

🛠 Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/Niraj-82/MCP-Crypto-Server.git
cd MCP-Crypto-Server

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the server
uvicorn server:app --reload

4️⃣ Open API documentation

Visit:
👉 http://localhost:8000/docs

📂 Project Structure
📦 MCP-Crypto-Server
│
├── server.py                       # Main FastAPI app
│
├── routers/
│     ├── real_time.py              # Ticker, orderbook, trades
│     ├── historical.py             # OHLCV
│     └── utils.py                  # Exchanges, symbols, validation
│
├── services/
│     ├── exchange_client.py        # CCXT integration
│     ├── cache_service.py          # Enhanced caching
│     ├── validation_service.py     # Validation logic
│     └── rate_limit.py             # Rate limiting (NEW)
│
├── analytics/
│     ├── indicators.py             # SMA/EMA (NEW)
│     └── portfolio.py              # Portfolio engine (NEW)
│
├── realtime/
│     └── websocket_handler.py      # Streaming prototype (NEW)
│
├── models/
│     ├── request_models.py
│     └── response_models.py
│
└── tests/                          # Test suite

🌐 API Endpoints Summary
🔵 Real-Time
Method	Endpoint	Description
POST	/api/v1/real_time/ticker	Current price
POST	/api/v1/real_time/order_book	Bids/asks
POST	/api/v1/real_time/trades	Recent trades
🟣 Historical
Method	Endpoint	Description
POST	/api/v1/historical/ohlcv	Candlestick data
🟢 Utilities
Method	Endpoint	Description
GET	/api/v1/utils/exchanges	Exchange list
GET	/api/v1/utils/symbols/{ex}	Tradable symbols
POST	/api/v1/utils/validate	Validate pair
GET	/api/v1/utils/status	Server health
📊 New Features Added (Enhancements)
📌 Technical Indicators

SMA

EMA

Expandable indicator framework

📌 Portfolio Analytics

Total value

Per-asset valuation

Real-time price integration

📌 WebSocket Streaming

Prototype live ticker feed

📌 Extended Caching

Faster performance

Lower API usage

📌 Rate Limiting

Prevents over-calling exchanges

🎯 Assumptions

This project assumes:

User will make reasonable request frequencies
(Cache and rate limiter handle common cases, but high-frequency bots need CCXT Pro.)

Internet connection is required
since data comes from external crypto exchanges.

Exchange APIs may fail, so retry logic handles temporary outages.

The server is non-persistent, meaning:

No database

No user accounts

No long-term storage
(Can be added later.)

Client-side visualization/usage is external to this project.

🧪 Run Tests
pytest -v

🐳 Docker Deployment

Build:

docker build -t mcp-crypto-server .


Run:

docker run -p 8000:8000 mcp-crypto-server

📄 License

MIT License © 2025

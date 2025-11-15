Advanced MCP Crypto Server
Real-Time | Historical | Indicators | Portfolio | Streaming | CCXT | FastAPI

📌 Overview

The Advanced MCP Crypto Server is a fully asynchronous, production-ready API platform designed to retrieve, process, and analyze cryptocurrency market data using CCXT and FastAPI.

This enhanced version includes:

🔥 Real-time & historical crypto data

📊 Technical indicators (SMA, EMA)

💼 Portfolio analytics engine

🔌 WebSocket streaming prototype

⚡ Extended caching + rate limiting

🛡 Retry logic, validations & error handling

Ideal for trading bots, AI agents, analytics dashboards, market research tools, and real-time financial systems.

✨ Key Features
🔰 Core Features

Real-time ticker, order book & trade history

Historical OHLCV with timeframe support

Exchange & symbol validation

In-memory TTL caching

FastAPI async architecture

CCXT integration with 70+ exchanges

Retry logic (3 attempts, exponential backoff)

🆕 New Enhancements
📊 Technical Indicators

SMA (Simple Moving Average)

EMA (Exponential Moving Average)

Easily extendable (RSI, MACD, Bollinger Bands, etc.)

💼 Portfolio Analytics

Real-time portfolio valuation

Multi-token support

Integrates with live market prices

📡 WebSocket Streaming

Simulated real-time feed

Ready for CCXT Pro upgrade

Useful for dashboards & monitoring tools

⚡ Performance Upgrades

Multi-layer caching

Rate limiting utility

Faster repeated requests

Lower exchange API load

📡 API Endpoints
🟦 Real-Time Endpoints
Method	Endpoint	Description
POST	/api/v1/real_time/ticker	Live price data
POST	/api/v1/real_time/order_book	Bid/ask levels
POST	/api/v1/real_time/trades	Recent trades
🟪 Historical Endpoint
Method	Endpoint	Description
POST	/api/v1/historical/ohlcv	OHLCV candlesticks
🟩 Utility Endpoints
Method	Endpoint	Purpose
GET	/api/v1/utils/exchanges	List all exchanges
GET	/api/v1/utils/symbols/{exchange}	List symbols
POST	/api/v1/utils/validate	Validate exchange/symbol pair
GET	/api/v1/utils/status	Health check
⚙️ Installation
git clone <your-repo-url>
cd mcp-crypto-server
pip install -r requirements.txt

🚀 Running the Server
uvicorn server:app --reload


Visit API docs:
👉 http://localhost:8000/docs

🧪 Running Tests
pytest -v

📦 Docker Deployment

Build the Docker image:

docker build -t mcp-crypto-server .


Run the container:

docker run -p 8000:8000 mcp-crypto-server

🔮 Future Enhancements

WebSocket integration using CCXT Pro

Full TA indicators (RSI, MACD, Bollinger Bands, ATR)

AI prediction endpoint

GraphQL interface

Redis caching layer

User authentication + portfolio storage


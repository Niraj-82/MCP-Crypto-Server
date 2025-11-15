
import uvicorn
import logging
import time
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from routers.real_time import router as real_time_router
from routers.historical import router as historical_router
from routers.utils import router as utils_router
from config import settings
from services import metrics as metrics_service
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from services.rate_limit_service import RateLimiter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_crypto_server")

app = FastAPI(title="MCP Crypto Market Data Server", version="0.1.0")

# Initialize rate limiter
rate_limiter = RateLimiter(interval=settings.RATE_LIMIT_INTERVAL)

# include routers
app.include_router(real_time_router, prefix="/api/v1/real_time")
app.include_router(historical_router, prefix="/api/v1/historical")
app.include_router(utils_router, prefix="/api/v1/utils")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    rate_limiter.wait()
    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s")
    try:
        # Use path as endpoint label; keep it simple
        metrics_service.observe_request(request.method, request.url.path, response.status_code, duration)
    except Exception:
        pass
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc} for {request.url.path}")
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

@app.exception_handler(Exception)
async def mcp_exception_handler(request: Request, exc: Exception):
    logger.error(f"Exception: {exc} for {request.url.path}")
    msg = str(exc)
    if isinstance(exc, ValueError) or 'not supported' in msg.lower():
        return JSONResponse(status_code=400, content={"detail": msg})
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error": "Internal Server Error"},
    )

if __name__ == "__main__":
    uvicorn.run("server.server:app", host=settings.HOST, port=settings.PORT, reload=True)


# Expose Prometheus metrics
@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics for scraping."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

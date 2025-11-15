from prometheus_client import Counter, Histogram

# Labels: method, endpoint, status_code
REQUEST_COUNT = Counter(
    "mcp_requests_total",
    "Total HTTP requests received by MCP server",
    ["method", "endpoint", "status_code"],
)

# Labels: method, endpoint
REQUEST_LATENCY = Histogram(
    "mcp_request_latency_seconds",
    "Histogram of request latency for MCP server",
    ["method", "endpoint"],
)


def observe_request(method: str, endpoint: str, status_code: int, duration: float) -> None:
    """Record a single request's metrics.

    Args:
        method: HTTP method string (GET/POST/etc.).
        endpoint: API path or route identifier.
        status_code: HTTP response status code.
        duration: Request processing time in seconds.
    """
    try:
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
    except Exception:
        # Metrics should never raise to avoid affecting request handling
        pass

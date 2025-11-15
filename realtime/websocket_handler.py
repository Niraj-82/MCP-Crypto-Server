
# placeholder websocket structure
async def stream_prices(callback):
    # pseudo-stream
    import asyncio, random
    while True:
        await asyncio.sleep(1)
        await callback({"BTC":random.random()*100000})

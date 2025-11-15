
import pandas as pd

def sma(data, period=14):
    return data['close'].rolling(period).mean()

def ema(data, period=14):
    return data['close'].ewm(span=period, adjust=False).mean()

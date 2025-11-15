
from analytics.portfolio import calculate_portfolio_value

def test_value():
    prices={'BTC':100}
    holdings={'BTC':2}
    assert calculate_portfolio_value(prices, holdings)==200

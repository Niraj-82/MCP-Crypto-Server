
def calculate_portfolio_value(prices, holdings):
    value=0
    for coin, amount in holdings.items():
        if coin in prices:
            value += prices[coin]*amount
    return value

import pandas as pd

def calculate_moving_averages(data, periods):
    """
    計算多個移動平均線
    """
    for period in periods:
        data[f'MA_{period}'] = data['close'].rolling(window=period).mean()
    return data
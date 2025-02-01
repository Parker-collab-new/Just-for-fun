import pandas as pd

def calculate_moving_averages(data, ma_periods):
    """
    計算多個移動平均線
    """
    for ma_period in ma_periods:
        data[f'MA_{ma_period}'] = data['close'].rolling(window=ma_period).mean()
    return data
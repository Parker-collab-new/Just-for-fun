import pandas as pd

def calculate_kd(data, k_period=14, d_period=3):
    """
    計算 KD 指標（隨機指標）
    :param data: 需要包含 'close', 'high', 'low' 欄位的 pandas DataFrame
    :param n: K 線計算的周期，默認為 14
    :param m: D 線的平滑周期，默認為 3
    :return: 包含 KD 指標的 pandas DataFrame
    """
    # 計算最高價和最低價
    high_n = data['high'].rolling(window=k_period).max()
    low_n = data['low'].rolling(window=k_period).min()

    # 計算 %K
    data['K'] = ((data['close'] - low_n) / (high_n - low_n)) * 100

    # 計算 %D (平滑 %K)
    data['D'] = data['K'].rolling(window=d_period).mean()

    return data
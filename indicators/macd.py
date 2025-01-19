import pandas as pd

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    計算 MACD 指標
    :param data: 需要包含 'close' 欄位的 pandas DataFrame
    :param fast_period: 快速 EMA 的周期，通常為 12
    :param slow_period: 慢速 EMA 的周期，通常為 26
    :param signal_period: 信號線的周期，通常為 9
    :return: 包含 MACD 指標的 pandas DataFrame
    """
    # 計算 12 日 EMA 和 26 日 EMA
    data['EMA_fast'] = data['close'].ewm(span=fast_period, adjust=False).mean()
    data['EMA_slow'] = data['close'].ewm(span=slow_period, adjust=False).mean()

    # 計算 MACD 線
    data['MACD'] = data['EMA_fast'] - data['EMA_slow']

    # 計算信號線 (9 日 EMA)
    data['Signal'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()

    # 計算直方圖
    data['Histogram'] = data['MACD'] - data['Signal']

    return data
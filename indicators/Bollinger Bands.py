import pandas as pd

def calculate_bollinger_bands(data, boolinger_period, num_std_dev=2):
    """
    計算布林通道
    :param data: 需要包含 'close' 欄位的 pandas DataFrame
    :param period: 計算 SMA 和標準差的周期 (默認 20)
    :param num_std_dev: 用來計算上軌和下軌的標準差倍數 (默認 2)
    :return: 包含布林通道的 pandas DataFrame
    """
    # 計算 20 日簡單移動平均線 (SMA)
    data['SMA'] = data['close'].rolling(window=boolinger_period, min_periods=1).mean()

    # 計算標準差
    data['STD'] = data['close'].rolling(window=boolinger_period, min_periods=1).std()

    # 計算上軌和下軌
    data['Upper Band'] = data['SMA'] + (data['STD'] * num_std_dev)
    data['Lower Band'] = data['SMA'] - (data['STD'] * num_std_dev)

    return data

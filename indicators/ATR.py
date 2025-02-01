import pandas as pd

def calculate_atr(data, atr_period):
    """
    計算 ATR 指標（平均真實區間）
    :param data: 需要包含 'high', 'low', 'close' 欄位的 pandas DataFrame
    :param n: ATR 計算的周期，默認為 14
    :return: 包含 ATR 指標的 pandas DataFrame
    """
    # 計算當前周期的 TR
    data['previous_close'] = data['close'].shift(1)
    data['tr1'] = data['high'] - data['low']
    data['tr2'] = abs(data['high'] - data['previous_close'])
    data['tr3'] = abs(data['low'] - data['previous_close'])

    # 取 TR 的最大值
    data['TR'] = data[['tr1', 'tr2', 'tr3']].max(axis=1)

    # 計算 ATR，使用移動平均
    data['ATR'] = data['TR'].rolling(window=atr_period).mean()

    # 刪除輔助欄位
    data.drop(['previous_close', 'tr1', 'tr2', 'tr3'], axis=1, inplace=True)

    return data
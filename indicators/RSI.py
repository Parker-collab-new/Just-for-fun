import pandas as pd

def calculate_rsi(data, rsi_period=14):
    """
    計算 RSI 指標
    :param data: 需要包含 'close' 欄位的 pandas DataFrame
    :param period: 計算 RSI 的周期 (默認 14)
    :return: 包含 RSI 指標的 pandas DataFrame
    """
    # 計算價格變化
    delta = data['close'].diff()

    # 計算漲幅和跌幅
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 計算平均漲幅和平均跌幅
    avg_gain = gain.rolling(window=rsi_period, min_periods=1).mean()
    avg_loss = loss.rolling(window=rsi_period, min_periods=1).mean()

    # 計算相對強弱 (RS)
    rs = avg_gain / avg_loss

    # 計算 RSI
    rsi = 100 - (100 / (1 + rs))

    # 返回原始 DataFrame 並加入 RSI 欄位
    data['RSI'] = rsi
    return data
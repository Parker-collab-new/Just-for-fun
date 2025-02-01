def should_enter_position(data, i, trend_line=None, bb_upper=None, bb_lower=None, 
                          rsi=None, macd=None, signal=None, volume=None, 
                          conditions=None):
    """
    判斷是否符合進場條件：
    - 條件由 `conditions` 提供，用戶可動態設置。

    參數:
        data (DataFrame): 包含價格和成交量的數據。
        i (int): 當前行索引。
        trend_line (float): 當前趨勢線（可選）。
        bb_upper (float): 布林通道上軌（可選）。
        bb_lower (float): 布林通道下軌（可選）。
        rsi (Series): RSI 值序列（可選）。
        macd (Series): MACD 值序列（可選）。
        signal (Series): MACD 信號線序列（可選）。
        volume (Series): 成交量序列（可選）。
        conditions (dict): 用戶設置的條件，包含以下鍵：
            - 'bb_break_upper' (bool): 是否判斷價格突破布林上軌。
            - 'rsi_condition' (tuple): RSI 條件，例如 ('>', 70)。
            - 'volume_threshold' (float): 成交量閾值倍數，例如 1.5 表示暴增 1.5 倍。
            - 'macd_cross' (bool): 是否判斷 MACD 黃金交叉。
            - 'breakout' (bool): 是否判斷價格突破回調高點。

    返回:
        bool: 是否符合進場條件。
    """
    if conditions is None:
        conditions = {}

    # 1. 價格突破布林通道上軌
    if conditions.get('bb_break_upper', False):
        if bb_upper is not None and data['close'].iloc[i] > bb_upper:
            return True

    # 2. RSI 條件
    rsi_condition = conditions.get('rsi_condition')
    if rsi_condition and rsi is not None:
        operator, threshold = rsi_condition
        if operator == '>' and rsi.iloc[i] > threshold:
            return True
        elif operator == '<' and rsi.iloc[i] < threshold:
            return True

    # 3. 成交量暴增
    volume_threshold = conditions.get('volume_threshold', None)
    if volume_threshold is not None and volume is not None:
        if i >= 10:  # 確保有足夠的數據計算平均成交量
            avg_volume = data['volume'].iloc[i-10:i].mean()
            if volume.iloc[i] > avg_volume * volume_threshold:
                return True

    # 4. MACD 黃金交叉
    if conditions.get('macd_cross', False) and macd is not None and signal is not None:
        if i > 0 and macd.iloc[i] > signal.iloc[i] and macd.iloc[i-1] <= signal.iloc[i-1]:
            return True

    # 5. 價格突破回調高點
    if conditions.get('breakout', False) and i >= 5:
        if data['close'].iloc[i] > max(data['close'].iloc[i-5:i-1]):
            return True

    return False  # 如果沒有符合任何條件，返回 False
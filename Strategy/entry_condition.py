from indicators.MA import calculate_moving_averages

def entry_condition(data, i, prev_macd, prev_signal, current_macd, current_signal, rsi, slippage, 
                    bb_upper, bb_lower, macd_threshold=0, rsi_lower_threshold=30, rsi_upper_threshold=70, 
                    volume_threshold=1.5, min_transaction_value=10000, condition_rules=None):
    """
    判斷是否進場的條件：
    - RSI < 30 或 RSI > 70
    - MACD 趨勢變化 (MACD 線和信號線交叉)
    - 價格突破布林通道的上軌或下軌
    - 成交量暴增
    - 成交金額至少達到指定門檻

    condition_rules 是一個字典，根據用戶設定的條件進行靈活判斷。
    """
    if condition_rules is None:
        condition_rules = {}

    # 1. 布林通道判斷（根據用戶自定義的條件）
    if condition_rules.get('bb_break', False):  # 'bb_break' 可能會是用戶設置的條件
        if data['close'].iloc[i] < bb_lower:
            return True  # 跌破布林下軌進場

    # 2. RSI 判斷：是否 RSI < 30 或 RSI > 70
    if condition_rules.get('rsi_condition', 'both') == 'lower' and rsi[i] < rsi_lower_threshold:
        return True  # RSI < 30 進場
    elif condition_rules.get('rsi_condition', 'both') == 'upper' and rsi[i] > rsi_upper_threshold:
        return True  # RSI > 70 進場
    elif condition_rules.get('rsi_condition', 'both') == 'both' and (rsi[i] < rsi_lower_threshold or rsi[i] > rsi_upper_threshold):
        return True  # RSI 超賣或超買進場

    # 3. MACD 變化：當前 MACD 線是否大於信號線
    if condition_rules.get('macd_cross', False):  # macd_cross: 用戶是否希望判斷 MACD 交叉
        if current_macd > current_signal and prev_macd <= prev_signal:
            return True  # MACD 線向上突破信號線，進場

    # 4. 成交量暴增：當前成交量大於過去 N 日的平均成交量 * volume_threshold
    avg_volume = data['volume'].iloc[i-10:i].mean()  # 假設過去 10 日的平均成交量
    if condition_rules.get('volume_boost', False):  # 'volume_boost' 控制是否啟用成交量暴增條件
        if data['volume'].iloc[i] > avg_volume * volume_threshold:
            return True  # 當前成交量暴增

    # 5. 成交金額至少達到指定門檻
    if condition_rules.get('min_transaction_value', False):  # 'min_transaction_value' 控制是否啟用成交金額條件
        transaction_value = data['close'].iloc[i] * data['volume'].iloc[i]  # 成交金額 = 收盤價 * 成交量
        if transaction_value >= min_transaction_value:
            return True  # 成交金額達到門檻

    # 如果沒有觸發任何條件，返回 False
    return False
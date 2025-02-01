def reduce_position(data, i, entry_price, trend_line, bb_upper, bb_lower, 
                    profit_threshold=0.05, trend_distance_threshold=0.02, 
                    condition_rules=None):
    """
    判斷是否減倉的條件：
    - 漲幅超過一定百分比
    - 離趨勢線過遠
    - 碰到布林通道

    profit_threshold: 設定漲幅達到多少百分比後進行減倉
    trend_distance_threshold: 設定離趨勢線過遠的距離閾值
    """
    if condition_rules is None:
        condition_rules = {}

    # 1. 漲幅達到一定百分比（如 5%）
    if condition_rules.get('profit_threshold', False):
        current_price = data['close'].iloc[i]
        price_change_percentage = (current_price - entry_price) / entry_price
        if price_change_percentage >= profit_threshold:
            return True  # 漲幅達到門檻，觸發減倉條件

    # 2. 與趨勢線的距離過遠（如 2%）
    if condition_rules.get('trend_distance', False):
        price_distance_from_trend = abs(data['close'].iloc[i] - trend_line) / trend_line
        if price_distance_from_trend >= trend_distance_threshold:
            return True  # 距離趨勢線過遠，觸發減倉條件

    # 3. 碰到布林通道的上軌或下軌
    if condition_rules.get('bb_touch', False):
        if data['close'].iloc[i] >= bb_upper or data['close'].iloc[i] <= bb_lower:
            return True  # 碰到布林通道的上下軌，觸發減倉條件

    # 如果沒有觸發任何減倉條件，返回 False
    return False

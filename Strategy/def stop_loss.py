def stop_loss(data, i, entry_price, slippage, stop_loss_percentage=0.05, 
              atr_factor=2, bb_lower=None, atr=None, rsi=None, 
              condition_rules=None):
    """
    判斷是否需要停損的條件：
    - 固定百分比停損（如 5%）
    - ATR 設定的停損區間
    - 價格突破布林通道下軌
    - RSI 顯示市場過賣區域

    condition_rules 是用戶設置的動態條件
    """
    if condition_rules is None:
        condition_rules = {}

    # 1. 固定百分比停損
    if condition_rules.get('percentage_stop_loss', False):
        price_change_percentage = (data['close'].iloc[i] - entry_price) / entry_price
        if price_change_percentage <= -stop_loss_percentage:
            return True  # 價格下跌超過設定百分比，觸發停損

    # 2. 使用 ATR 設定的停損區間
    if condition_rules.get('atr_stop_loss', False):
        stop_loss_price = entry_price - atr_factor * atr[i]  # 基於 ATR 計算的停損區間
        if data['close'].iloc[i] <= stop_loss_price:
            return True  # 價格跌破基於 ATR 計算的停損區間，觸發停損

    # 3. 碰到布林通道下軌
    if condition_rules.get('bb_stop_loss', False) and bb_lower is not None:
        if data['close'].iloc[i] <= bb_lower[i]:
            return True  # 價格觸及布林通道下軌，觸發停損

    # 4. RSI 顯示超賣區域
    if condition_rules.get('rsi_stop_loss', False) and rsi is not None:
        if rsi[i] < 30:  # RSI < 30 表示過賣
            return True  # RSI 顯示過賣區域，觸發停損

    # 如果沒有觸發任何停損條件，返回 False
    return False

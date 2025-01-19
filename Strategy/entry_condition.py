from indicators.MA import calculate_moving_averages

def entry_condition(data, i, position_value, prev_ma7, prev_ma99, current_ma7, current_ma99, slippage):
    """
    判斷是否進場的條件
    """
    if prev_ma7 < prev_ma99 and current_ma7 > current_ma99 and position_value == 0:
        entry_price = data['close'].iloc[i] * (1 + slippage)
        stop_loss_price = data['close'].iloc[i] * (1 - 0.1)  # 假設 stop_loss_offset 是 0.1
        position_value = 50 * 10  # 假設 leverage 是 10，initial_margin 是 50
        position_quantity = position_value / entry_price
        return entry_price, stop_loss_price, position_value, position_quantity
    return None, None, position_value, 0
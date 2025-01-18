import pandas as pd
import logging

def calculate_moving_averages(data, periods):
    """
    計算多個移動平均線
    """
    for period in periods:
        data[f'MA_{period}'] = data['close'].rolling(window=period).mean()
    return data

def backtest_long_strategy(data, leverage=10, initial_margin=50, 
                           increase_threshold=0.1, reduce_fraction=0.5, 
                           fee_rate=0.001, slippage=0.0005, 
                           stop_loss_offset=0.1, max_loss_threshold=0.20,
                           take_profit_threshold=0.10, price_drop_threshold=0.03):

    """
    單個交易對回測做多策略，增加停利和特定條件的加倉，且支持多次累計加倉。
    """
    position_value = 0
    entry_price = None
    stop_loss_price = None
    initial_balance = 1000
    cash = initial_balance
    position_quantity = 0
    balance = cash + position_quantity
    trade_log = []
    max_loss_limit = initial_balance * (1 - max_loss_threshold)
    total_fees = 0
    reduce_profit = 0  # 累計減倉獲得的利潤
    reduce_count = 0  # 累計減倉次數

    start_time = data.index[0]
    end_time = data.index[-1]

    # 回測主循環
    for i in range(1, len(data)):
        current_close = data['close'].iloc[i]
        prev_ma7 = data['MA_7'].iloc[i - 1]
        prev_ma99 = data['MA_99'].iloc[i - 1]
        current_ma7 = data['MA_7'].iloc[i]
        current_ma99 = data['MA_99'].iloc[i]
        current_ma25 = data['MA_25'].iloc[i]

        # 動態更新持倉價值
        if position_value > 0:
            position_value = position_quantity * current_close

        # 進場條件
        if prev_ma7 < prev_ma99 and current_ma7 > current_ma99 and position_value == 0:
            entry_price = current_close * (1 + slippage)
            stop_loss_price = current_close * (1 - stop_loss_offset)
            position_value = initial_margin * leverage
            position_quantity = position_value / entry_price
            fee = position_value * fee_rate
            cash = cash - fee - position_value
            balance = cash + position_value
            total_fees += fee
            reduce_profit = 0  # 重置減倉利潤
            reduce_count = 0  # 重置減倉次數
            trade_log.append({
                'Type': 'Entry',
                'Price': entry_price,
                'Position_Value': position_value,
                'Balance': balance,
                'Stop_Loss': stop_loss_price,
                'Timestamp': data.index[i],
                'Cash': cash 
            })

        # 其他邏輯略...

    final_balance = balance
    total_trades = len(trade_log)
    total_pnl = final_balance - initial_balance
    total_pnl_percent = (total_pnl / initial_balance) * 100
    return pd.DataFrame(trade_log), final_balance, total_trades, total_pnl, total_pnl_percent, total_fees, start_time, end_time
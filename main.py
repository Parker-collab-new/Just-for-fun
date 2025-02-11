import os
import logging
import sys
import pandas as pd
from binance.client import Client
from indicators.MA import calculate_moving_averages 
from indicators.ATR import calculate_atr
from symbol_setting import TradingSettingsApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from Strategy.codition_setting import TradingConditionApp
# 初始化日志
logging.basicConfig(
    filename="回測_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# 環境變量 API 密鑰
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
if not API_KEY or not API_SECRET:
    raise ValueError("請設置環境變量 BINANCE_API_KEY 和 BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

def fetch_klines(symbol, interval, limit=1000):
    """
    獲取 Binance K 線數據，返回 DataFrame
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[ 
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_volume', 
        'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['close', 'volume']].astype(float)
    return df

def backtest_multiple_symbols(symbols, interval, periods):
    results = {}
    for symbol in symbols:
        logging.info(f"開始回測交易對: {symbol}")
        try:
            data = fetch_klines(symbol, interval)
            data = calculate_moving_averages(data, periods)
            trade_log, final_balance, total_trades, total_pnl, total_pnl_percent, total_fees, start_time, end_time = backtest_long_strategy(
                data
            )
            results[symbol] = {
                'Trade_Log': trade_log,
                'Final_Balance': final_balance,
                'Total_Trades': total_trades,
                'Total_PnL': total_pnl,
                'Total_PnL_Percent': total_pnl_percent,
                'Total_Fees': total_fees,
                'Start_Time': start_time,
                'End_Time': end_time
            }
        except Exception as e:
            logging.error(f"回測 {symbol} 時出現錯誤: {e}")
    return results

# 主程式入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    settings_window = TradingSettingsApp()

    user_settings = None  # 先定義，確保變數存在

    if settings_window.exec_() == QDialog.Accepted:  # 用戶點了「確定」
        user_settings = settings_window.get_settings()  # 只在接受後獲取參數
        condition_window = TradingConditionApp(settings_window)  # 傳遞 settings_window
        condition_window.show()

    print("用戶設定的參數：", user_settings)

    # 提取用戶的設置參數
    symbols = [user_settings['symbol']]  # 這裡假設你只選擇了一個交易對
    interval = user_settings['interval']
    ma_periods = user_settings['periods']
    bollingerBands = user_settings['BollingerBands']
    atr = user_settings['ATR']
    macd = user_settings['MACD']
    rsi = user_settings['RSI']
   

    # 在這裡調用回測函數
    logging.info("回測開始...")
    results = backtest_multiple_symbols(symbols, interval, ma_periods)

    # 輸出結果
    for symbol, result in results.items():
        logging.info(f"\n交易對: {symbol}")
        logging.info(f"最終餘額: {result['Final_Balance']:.2f} USDT")
        logging.info(f"總交易次數: {result['Total_Trades']}")
        logging.info(f"總盈虧: {result['Total_PnL']:.2f} USDT ({result['Total_PnL_Percent']:.2f}%)")
        logging.info(f"總費用: {result['Total_Fees']:.2f} USDT")
    
    sys.exit(app.exec_())  # 確保退出 QApplication
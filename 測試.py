try:
    from strategy import calculate_moving_averages, backtest_long_strategy
    print("Successfully imported calculate_moving_averages and backtest_long_strategy!")
    
    # 验证函数是否可调用
    if callable(calculate_moving_averages):
        print("calculate_moving_averages is callable.")
    else:
        print("Error: calculate_moving_averages is not callable.")
        
    if callable(backtest_long_strategy):
        print("backtest_long_strategy is callable.")
    else:
        print("Error: backtest_long_strategy is not callable.")

except ImportError as e:
    print(f"ImportError occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

class TradingSettingsApp(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易參數設定")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("font-size: 14px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 交易對選擇
        self.symbol_label = QLabel("選擇交易對：")
        self.symbol_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(["ZENUSDT", "ETHUSDT", "BNBUSDT"])

        # 時間週期
        self.interval_label = QLabel("選擇時間週期：")
        self.interval_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])

        # 均線週期
        self.period_label = QLabel("設定均線週期：")
        self.period_label.setFont(QFont("Arial", 12, QFont.Bold))
        period_layout = QHBoxLayout()
        self.period1_input = QLineEdit("7")
        self.period1_input.setFixedWidth(50)
        self.period2_input = QLineEdit("25")
        self.period2_input.setFixedWidth(50)
        self.period3_input = QLineEdit("99")
        self.period3_input.setFixedWidth(50)
        period_layout.addWidget(self.period1_input)
        period_layout.addWidget(self.period2_input)
        period_layout.addWidget(self.period3_input)

        # ATR 參數
        self.atr_label = QLabel("ATR 週期：")
        self.atr_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.atr_input = QLineEdit("14")
        self.atr_input.setFixedWidth(50)

        # 布林通道參數
        self.boll_label = QLabel("布林通道（週期, 標準差）：")
        self.boll_label.setFont(QFont("Arial", 12, QFont.Bold))
        boll_layout = QHBoxLayout()
        self.boll_period_input = QLineEdit("20")
        self.boll_period_input.setFixedWidth(50)
        self.boll_std_input = QLineEdit("2")
        self.boll_std_input.setFixedWidth(50)
        boll_layout.addWidget(self.boll_period_input)
        boll_layout.addWidget(self.boll_std_input)

        # KD 指標
        self.kd_label = QLabel("KD 指標（K, D 週期）：")
        self.kd_label.setFont(QFont("Arial", 12, QFont.Bold))
        kd_layout = QHBoxLayout()
        self.kd_k_input = QLineEdit("9")
        self.kd_k_input.setFixedWidth(50)
        self.kd_d_input = QLineEdit("3")
        self.kd_d_input.setFixedWidth(50)
        kd_layout.addWidget(self.kd_k_input)
        kd_layout.addWidget(self.kd_d_input)

        # MACD 指標
        self.macd_label = QLabel("MACD（快, 慢, 訊號）：")
        self.macd_label.setFont(QFont("Arial", 12, QFont.Bold))
        macd_layout = QHBoxLayout()
        self.macd_fast_input = QLineEdit("12")
        self.macd_fast_input.setFixedWidth(50)
        self.macd_slow_input = QLineEdit("26")
        self.macd_slow_input.setFixedWidth(50)
        self.macd_signal_input = QLineEdit("9")
        self.macd_signal_input.setFixedWidth(50)
        macd_layout.addWidget(self.macd_fast_input)
        macd_layout.addWidget(self.macd_slow_input)
        macd_layout.addWidget(self.macd_signal_input)

        # RSI 參數
        self.rsi_label = QLabel("RSI 週期：")
        self.rsi_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.rsi_input = QLineEdit("14")
        self.rsi_input.setFixedWidth(50)

        # 設置按鈕
        self.set_button = QPushButton("確定設置")
        self.set_button.setFont(QFont("Arial", 14))
        self.set_button.clicked.connect(self.apply_settings)

        # 加入佈局
        layout.addWidget(self.symbol_label)
        layout.addWidget(self.symbol_combo)
        layout.addWidget(self.interval_label)
        layout.addWidget(self.interval_combo)
        layout.addWidget(self.period_label)
        layout.addLayout(period_layout)
        layout.addWidget(self.atr_label)
        layout.addWidget(self.atr_input)
        layout.addWidget(self.boll_label)
        layout.addLayout(boll_layout)
        layout.addWidget(self.kd_label)
        layout.addLayout(kd_layout)
        layout.addWidget(self.macd_label)
        layout.addLayout(macd_layout)
        layout.addWidget(self.rsi_label)
        layout.addWidget(self.rsi_input)
        layout.addWidget(self.set_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def apply_settings(self):
        """取得用戶設置的參數"""
        self.settings = {
            "symbol": self.symbol_combo.currentText(),
            "interval": self.interval_combo.currentText(),
            "periods": [
                int(self.period1_input.text()), 
                int(self.period2_input.text()), 
                int(self.period3_input.text())
            ],
            "ATR": int(self.atr_input.text()),
            "BollingerBands": {
                "period": int(self.boll_period_input.text()),
                "std_dev": float(self.boll_std_input.text())
            },
            "KD": {
                "K": int(self.kd_k_input.text()),
                "D": int(self.kd_d_input.text())
            },
            "MACD": {
                "fast": int(self.macd_fast_input.text()),
                "slow": int(self.macd_slow_input.text()),
                "signal": int(self.macd_signal_input.text())
            },
            "RSI": int(self.rsi_input.text())
        }
        self.accept()  # 關閉窗口
    
    def get_settings(self):
        """返回當前用戶設置"""
        return self.settings


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingSettingsApp()
    window.show()
    sys.exit(app.exec_())


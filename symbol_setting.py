import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TradingSettingsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易參數設定")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("font-size: 14px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 設置交易對選擇
        self.symbol_label = QLabel("選擇交易對：")
        self.symbol_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(["ZENUSDT", "ETHUSDT", "BNBUSDT"])

        # 設置時間週期選擇
        self.interval_label = QLabel("選擇時間週期：")
        self.interval_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])

        # 設置均線週期
        self.period_label = QLabel("設定均線週期：")
        self.period_label.setFont(QFont("Arial", 12, QFont.Bold))

        period_layout = QHBoxLayout()
        self.period1_input = QLineEdit()
        self.period1_input.setPlaceholderText("7")
        self.period1_input.setFixedWidth(50)

        self.period2_input = QLineEdit()
        self.period2_input.setPlaceholderText("25")
        self.period2_input.setFixedWidth(50)

        self.period3_input = QLineEdit()
        self.period3_input.setPlaceholderText("99")
        self.period3_input.setFixedWidth(50)

        period_layout.addWidget(self.period1_input)
        period_layout.addWidget(self.period2_input)
        period_layout.addWidget(self.period3_input)

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
        layout.addWidget(self.set_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def apply_settings(self):
        """取得用戶設置的參數"""
        symbol = self.symbol_combo.currentText()
        interval = self.interval_combo.currentText()
        period1 = self.period1_input.text() if self.period1_input.text() else "7"
        period2 = self.period2_input.text() if self.period2_input.text() else "25"
        period3 = self.period3_input.text() if self.period3_input.text() else "99"

        settings = {
            "symbol": symbol,
            "interval": interval,
            "periods": [int(period1), int(period2), int(period3)]
        }

        print("當前設置:", settings)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingSettingsApp()
    window.show()
    print("symbol")
    sys.exit(app.exec_())


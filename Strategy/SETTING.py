import json
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TradingConditionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易條件設置")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("font-size: 14px;")

        main_layout = QVBoxLayout()

        # === 買進條件 ===
        buy_layout = QVBoxLayout()
        buy_layout.setContentsMargins(10, 10, 10, 10)
        buy_layout.setSpacing(10)

        buy_label = QLabel("📈 買進條件設定")
        buy_label.setFont(QFont("Arial", 16, QFont.Bold))
        buy_layout.addWidget(buy_label)

        self.buy_amount_checkbox = QCheckBox("成交金額 至少")
        self.amount_value_input = QLineEdit()
        self.amount_value_input.setPlaceholderText("輸入成交金額")

        self.buy_volume_checkbox = QCheckBox("成交量 至少")
        self.volume_value_input = QLineEdit()
        self.volume_value_input.setPlaceholderText("輸入成交量閾值")

        self.rsi_checkbox = QCheckBox("RSI")
        self.rsi_condition_input = QComboBox()
        self.rsi_condition_input.addItems([">", "<"])
        self.rsi_value_input = QLineEdit()
        self.rsi_value_input.setPlaceholderText("輸入 RSI 值")

        self.macd_checkbox = QCheckBox("MACD")
        self.macd_condition_input = QComboBox()
        self.macd_condition_input.addItems(["黃金交叉", "死亡交叉", "漸增", "漸減"])

        self.bollinger_checkbox = QCheckBox("布林通道")
        self.bollinger_condition_input = QComboBox()
        self.bollinger_condition_input.addItems(["> 上軌", "< 下軌"])
        self.bollinger_std_input = QLineEdit()
        self.bollinger_std_input.setPlaceholderText("標準差 (如 2.0)")

        for widget in [
            (self.buy_amount_checkbox, self.amount_value_input),
            (self.buy_volume_checkbox, self.volume_value_input),
            (self.rsi_checkbox, self.rsi_condition_input, self.rsi_value_input),
            (self.macd_checkbox, self.macd_condition_input),
            (self.bollinger_checkbox, self.bollinger_condition_input, self.bollinger_std_input),
        ]:
            row = QHBoxLayout()
            for w in widget:
                row.addWidget(w)
            row.addStretch(1)
            buy_layout.addLayout(row)

        # === 停損條件 ===
        stop_loss_layout = QVBoxLayout()
        stop_loss_layout.setContentsMargins(10, 10, 10, 10)
        stop_loss_layout.setSpacing(10)

        stop_loss_label = QLabel("📉 停損條件設定")
        stop_loss_label.setFont(QFont("Arial", 16, QFont.Bold))
        stop_loss_layout.addWidget(stop_loss_label)

        self.atr_checkbox = QCheckBox("ATR 停損")
        self.atr_value_input = QLineEdit()
        self.atr_value_input.setPlaceholderText("輸入 ATR 乘數")

        self.rsi_stop_checkbox = QCheckBox("RSI 停損")
        self.rsi_stop_condition = QComboBox()
        self.rsi_stop_condition.addItems([">", "<"])
        self.rsi_stop_value = QLineEdit()
        self.rsi_stop_value.setPlaceholderText("輸入 RSI 值")

        self.macd_stop_checkbox = QCheckBox("MACD 停損")
        self.macd_stop_condition = QComboBox()
        self.macd_stop_condition.addItems(["黃金交叉", "死亡交叉"])

        self.kd_stop_checkbox = QCheckBox("KD 停損")
        self.kd_stop_condition = QComboBox()
        self.kd_stop_condition.addItems(["> K", "< K", "> D", "< D"])
        self.kd_stop_value = QLineEdit()
        self.kd_stop_value.setPlaceholderText("輸入 KD 值")

        self.ma_stop_checkbox = QCheckBox("MA 停損")
        self.ma_stop_condition = QComboBox()
        self.ma_stop_condition.addItems(["跌破 MA", "突破 MA"])
        self.ma_stop_value = QLineEdit()
        self.ma_stop_value.setPlaceholderText("輸入 MA 週期")

        self.bollinger_stop_checkbox = QCheckBox("布林通道 停損")
        self.bollinger_stop_condition = QComboBox()
        self.bollinger_stop_condition.addItems(["跌破下軌", "突破上軌"])

        for widget in [
            (self.atr_checkbox, self.atr_value_input),
            (self.rsi_stop_checkbox, self.rsi_stop_condition, self.rsi_stop_value),
            (self.macd_stop_checkbox, self.macd_stop_condition),
            (self.kd_stop_checkbox, self.kd_stop_condition, self.kd_stop_value),
            (self.ma_stop_checkbox, self.ma_stop_condition, self.ma_stop_value),
            (self.bollinger_stop_checkbox, self.bollinger_stop_condition),
        ]:
            row = QHBoxLayout()
            for w in widget:
                row.addWidget(w)
            row.addStretch(1)
            stop_loss_layout.addLayout(row)

        # === 設置條件按鈕 ===
        self.set_conditions_btn = QPushButton("設置條件")
        self.set_conditions_btn.setFont(QFont("Arial", 14))
        self.set_conditions_btn.clicked.connect(self.set_conditions)

        main_layout.addLayout(buy_layout)
        main_layout.addLayout(stop_loss_layout)
        main_layout.addWidget(self.set_conditions_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def set_conditions(self):
        """保存交易與停損條件"""
        conditions = {
            "buy_conditions": {
                "trade_amount": self.amount_value_input.text() if self.buy_amount_checkbox.isChecked() else None,
                "volume": self.volume_value_input.text() if self.buy_volume_checkbox.isChecked() else None,
                "rsi": {"condition": self.rsi_condition_input.currentText(), "value": self.rsi_value_input.text()} if self.rsi_checkbox.isChecked() else None,
                "macd": self.macd_condition_input.currentText() if self.macd_checkbox.isChecked() else None,
                "bollinger": {"condition": self.bollinger_condition_input.currentText(), "std": self.bollinger_std_input.text()} if self.bollinger_checkbox.isChecked() else None,
            },
            "stop_loss_conditions": {
                "atr": self.atr_value_input.text() if self.atr_checkbox.isChecked() else None,
                "rsi": {"condition": self.rsi_stop_condition.currentText(), "value": self.rsi_stop_value.text()} if self.rsi_stop_checkbox.isChecked() else None,
                "macd": self.macd_stop_condition.currentText() if self.macd_stop_checkbox.isChecked() else None,
                "kd": {"condition": self.kd_stop_condition.currentText(), "value": self.kd_stop_value.text()} if self.kd_stop_checkbox.isChecked() else None,
                "ma": {"condition": self.ma_stop_condition.currentText(), "period": self.ma_stop_value.text()} if self.ma_stop_checkbox.isChecked() else None,
                "bollinger": self.bollinger_stop_condition.currentText() if self.bollinger_stop_checkbox.isChecked() else None,
            }
        }

        with open("trade_conditions.json", "w", encoding="utf-8") as f:
            json.dump(conditions, f, indent=4, ensure_ascii=False)

        print("條件已儲存至 trade_conditions.json")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingConditionApp()
    window.show()
    sys.exit(app.exec_())

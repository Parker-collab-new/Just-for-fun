import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtCore import Qt

class TradingConditionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易條件設置")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("font-size: 14px;")

        # 主布局
        main_layout = QHBoxLayout()

        # 左側：交易條件設置
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(20)

        # 買進條件設置
        buy_condition_layout = QVBoxLayout()
        self.buy_condition_label = QLabel("買進條件：")
        self.buy_condition_label.setFont(QFont("Arial", 16, QFont.Bold))

        # 成交量條件
        self.buy_volume_layout = QHBoxLayout()
        self.buy_volume_checkbox = QCheckBox("成交量至少")
        self.volume_value_input = QLineEdit(self)
        self.volume_value_input.setPlaceholderText("輸入成交量閾值")
        self.volume_value_input.setFixedWidth(80)
        self.volume_value_input.setVisible(False)

        self.buy_volume_checkbox.stateChanged.connect(
            lambda: self.volume_value_input.setVisible(self.buy_volume_checkbox.isChecked())
        )

        self.buy_volume_layout.addWidget(self.buy_volume_checkbox)
        self.buy_volume_layout.addWidget(self.volume_value_input)
        self.buy_volume_layout.addStretch(1)

        # 成交量增加條件（倍數）
        self.volume_increase_layout = QHBoxLayout()
        self.volume_increase_checkbox = QCheckBox("成交量增加")
        self.volume_multiplier_input = QLineEdit(self)
        self.volume_multiplier_input.setPlaceholderText("倍數 (如 1.5)")
        self.volume_multiplier_input.setFixedWidth(80)
        self.volume_multiplier_input.setVisible(False)

        self.volume_increase_checkbox.stateChanged.connect(
            lambda: self.volume_multiplier_input.setVisible(self.volume_increase_checkbox.isChecked())
        )

        self.volume_increase_layout.addWidget(self.volume_increase_checkbox)
        self.volume_increase_layout.addWidget(self.volume_multiplier_input)
        self.volume_increase_layout.addStretch(1)

        # RSI 條件
        self.rsi_checkbox_layout = QHBoxLayout()
        self.rsi_checkbox = QCheckBox("RSI")
        self.rsi_condition_input = QComboBox()
        self.rsi_condition_input.addItems([">", "<"])
        self.rsi_value_input = QLineEdit(self)
        self.rsi_value_input.setPlaceholderText("輸入 RSI 值")
        self.rsi_value_input.setFixedWidth(80)

        self.rsi_checkbox_layout.addWidget(self.rsi_checkbox)
        self.rsi_checkbox_layout.addWidget(self.rsi_condition_input)
        self.rsi_checkbox_layout.addWidget(self.rsi_value_input)
        self.rsi_checkbox_layout.addStretch(1)

        # MACD 條件（黃金交叉 或 死亡交叉）
        self.macd_checkbox_layout = QHBoxLayout()
        self.macd_checkbox = QCheckBox("MACD")
        self.macd_condition_input = QComboBox()
        self.macd_condition_input.addItems(["黃金交叉", "死亡交叉"])
        self.macd_condition_input.setVisible(False)

        self.macd_checkbox.stateChanged.connect(
            lambda: self.macd_condition_input.setVisible(self.macd_checkbox.isChecked())
        )

        self.macd_checkbox_layout.addWidget(self.macd_checkbox)
        self.macd_checkbox_layout.addWidget(self.macd_condition_input)
        self.macd_checkbox_layout.addStretch(1)

        # 布林通道條件
        self.bollinger_checkbox_layout = QHBoxLayout()
        self.bollinger_checkbox = QCheckBox("布林通道")
        self.bollinger_condition_input = QComboBox()
        self.bollinger_condition_input.addItems(["> 上軌", "< 下軌"])
        self.bollinger_std_input = QLineEdit(self)
        self.bollinger_std_input.setPlaceholderText("標準差 (如 2.0)")
        self.bollinger_std_input.setFixedWidth(80)
        self.bollinger_std_input.setVisible(False)

        self.bollinger_checkbox.stateChanged.connect(
            lambda: self.bollinger_std_input.setVisible(self.bollinger_checkbox.isChecked())
        )

        self.bollinger_checkbox_layout.addWidget(self.bollinger_checkbox)
        self.bollinger_checkbox_layout.addWidget(self.bollinger_condition_input)
        self.bollinger_checkbox_layout.addWidget(self.bollinger_std_input)
        self.bollinger_checkbox_layout.addStretch(1)

        buy_condition_layout.addWidget(self.buy_condition_label)
        buy_condition_layout.addLayout(self.buy_volume_layout)
        buy_condition_layout.addLayout(self.volume_increase_layout)
        buy_condition_layout.addLayout(self.rsi_checkbox_layout)
        buy_condition_layout.addLayout(self.macd_checkbox_layout)
        buy_condition_layout.addLayout(self.bollinger_checkbox_layout)

        left_layout.addLayout(buy_condition_layout)

        # 右側：資金管理
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(20)

        self.right_frame = QFrame()
        self.right_frame.setFrameShape(QFrame.Box)
        self.right_frame.setStyleSheet("border: 2px solid #5A5A5A; border-radius: 10px;")
        right_frame_layout = QVBoxLayout(self.right_frame)
        right_frame_layout.setContentsMargins(10, 10, 10, 10)

        self.amount_label = QLabel("進場下單金額：")
        self.amount_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("輸入金額")

        self.leverage_label = QLabel("槓桿倍數：")
        self.leverage_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.leverage_input = QLineEdit()
        self.leverage_input.setPlaceholderText("輸入槓桿倍數")

        right_frame_layout.addWidget(self.amount_label)
        right_frame_layout.addWidget(self.amount_input)
        right_frame_layout.addWidget(self.leverage_label)
        right_frame_layout.addWidget(self.leverage_input)

        right_layout.addWidget(self.right_frame)

        # 設置條件按鈕
        self.set_conditions_btn = QPushButton("設置條件")
        self.set_conditions_btn.setFont(QFont("Arial", 14))
        self.set_conditions_btn.clicked.connect(self.set_conditions)

        # 主布局
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)
        main_layout.addWidget(self.set_conditions_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def set_conditions(self):
        """處理用戶設置的條件"""
        buy_conditions = {
            "volume_surge": self.buy_volume_checkbox.isChecked(),
            "volume_value": self.volume_value_input.text() if self.buy_volume_checkbox.isChecked() else None,
            "volume_increase": self.volume_increase_checkbox.isChecked(),
            "volume_multiplier": self.volume_multiplier_input.text() if self.volume_increase_checkbox.isChecked() else None,
            "rsi": self.rsi_checkbox.isChecked(),
            "rsi_condition": self.rsi_condition_input.currentText() if self.rsi_checkbox.isChecked() else None,
            "rsi_value": self.rsi_value_input.text() if self.rsi_checkbox.isChecked() else None,
            "macd": self.macd_checkbox.isChecked(),
            "macd_condition": self.macd_condition_input.currentText() if self.macd_checkbox.isChecked() else None,
            "bollinger_band": self.bollinger_checkbox.isChecked(),
            "bollinger_condition": self.bollinger_condition_input.currentText() if self.bollinger_checkbox.isChecked() else None,
            "bollinger_std": self.bollinger_std_input.text() if self.bollinger_checkbox.isChecked() else None,
        }

        print("買進條件:", buy_conditions)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingConditionApp()
    window.show()
    sys.exit(app.exec_())

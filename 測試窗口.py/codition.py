import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

class TradingConditionApp(QDialog):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易條件設置")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 進場條件
        self.entry_condition_label = QLabel("進場條件：")
        left_layout.addWidget(self.entry_condition_label)

        self.entry_conditions = {
            "成交量暴增": QCheckBox("成交量暴增"),
            "RSI": (QCheckBox("RSI"), QLineEdit()),
            "KD": (QCheckBox("KD"), QLineEdit()),
            "MA": (QCheckBox("MA"), QLineEdit()),
            "MACD": (QCheckBox("MACD"), QLineEdit()),
            "ATR": (QCheckBox("ATR"), QLineEdit()),
        }

        for key, value in self.entry_conditions.items():
            layout = QHBoxLayout()
            layout.addWidget(value[0])
            if isinstance(value, tuple):
                value[1].setPlaceholderText("輸入閾值")
                value[1].setVisible(False)
                layout.addWidget(value[1])
                value[0].toggled.connect(lambda checked, v=value[1]: v.setVisible(checked))
            left_layout.addLayout(layout)

        # 加倉、減倉、停損條件
        self.add_position_label = QLabel("加倉條件：")
        self.add_position_input = QComboBox()
        self.add_position_input.addItems(["價格突破上軌", "RSI>70", "MACD黃金交叉"])
        left_layout.addWidget(self.add_position_label)
        left_layout.addWidget(self.add_position_input)

        self.reduce_position_label = QLabel("減倉條件：")
        self.reduce_position_input = QComboBox()
        self.reduce_position_input.addItems(["價格跌破下軌", "RSI<30", "MACD死叉"])
        left_layout.addWidget(self.reduce_position_label)
        left_layout.addWidget(self.reduce_position_input)

        self.stop_loss_label = QLabel("停損條件：")
        self.stop_loss_input = QComboBox()
        self.stop_loss_input.addItems(["固定百分比停損", "ATR停損", "布林通道停損"])
        left_layout.addWidget(self.stop_loss_label)
        left_layout.addWidget(self.stop_loss_input)

        # 交易參數設置
        self.entry_amount_label = QLabel("進場金額：")
        self.entry_amount_input = QLineEdit()
        self.entry_amount_input.setPlaceholderText("輸入金額")

        self.leverage_label = QLabel("倍數：")
        self.leverage_input = QLineEdit()
        self.leverage_input.setPlaceholderText("輸入倍數")

        self.reduce_position_percentage_label = QLabel("減倉比例：")
        self.reduce_position_percentage_input = QLineEdit()
        self.reduce_position_percentage_input.setPlaceholderText("輸入減倉比例")

        self.add_position_percentage_label = QLabel("加倉比例：")
        self.add_position_percentage_input = QLineEdit()
        self.add_position_percentage_input.setPlaceholderText("輸入加倉比例")

        right_layout.addWidget(self.entry_amount_label)
        right_layout.addWidget(self.entry_amount_input)
        right_layout.addWidget(self.leverage_label)
        right_layout.addWidget(self.leverage_input)
        right_layout.addWidget(self.reduce_position_percentage_label)
        right_layout.addWidget(self.reduce_position_percentage_input)
        right_layout.addWidget(self.add_position_percentage_label)
        right_layout.addWidget(self.add_position_percentage_input)

        # 設置條件按鈕
        self.set_conditions_btn = QPushButton("設置條件")
        self.set_conditions_btn.clicked.connect(self.set_conditions)
        right_layout.addWidget(self.set_conditions_btn)

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

    def set_conditions(self):
        entry_conditions = {}
        for key, value in self.entry_conditions.items():
            if isinstance(value, tuple):
                if value[0].isChecked():
                    entry_conditions[key] = value[1].text() or "默認"
            else:
                if value.isChecked():
                    entry_conditions[key] = "選中"

        conditions = {
            "entry_conditions": entry_conditions,
            "add_condition": self.add_position_input.currentText(),
            "reduce_condition": self.reduce_position_input.currentText(),
            "stop_loss_condition": self.stop_loss_input.currentText(),
            "entry_amount": self.entry_amount_input.text() or "未設定",
            "leverage": self.leverage_input.text() or "未設定",
            "reduce_position_percentage": self.reduce_position_percentage_input.text() or "未設定",
            "add_position_percentage": self.add_position_percentage_input.text() or "未設定",
        }
        print(conditions)
        self.settings = conditions

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TradingConditionApp()
    ex.show()
    sys.exit(app.exec_())

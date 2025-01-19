import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class TradingConditionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("交易條件設置")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
                font-size: 18px;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-weight: bold;
                color: #333333;
                font-size: 18px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 30px;
                font-size: 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 18px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QComboBox {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 18px;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
            QCheckBox {
                font-size: 18px;
            }
            QVBoxLayout, QHBoxLayout {
                spacing: 20px;
            }
            .leftLayout {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            }
            .rightLayout {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            }
        """)

        main_layout = QHBoxLayout()  # 主布局，左右兩側

        # 左側：交易條件設置
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(20)

        # 買進條件設置 (多選框)
        buy_condition_layout = QVBoxLayout()
        self.buy_condition_label = QLabel("買進條件：")
        self.buy_volume_checkbox = QCheckBox("成交量暴增")
        self.rsi_checkbox_layout = QHBoxLayout()  # 使用水平布局放置勾選框和輸入框
        self.rsi_checkbox = QCheckBox("RSI<30")
        self.buy_condition_value_input = QLineEdit(self)
        self.buy_condition_value_input.setPlaceholderText("設置閾值")
        self.buy_condition_value_input.setVisible(False)  # 默認隱藏

        # 當勾選RSI條件時，顯示閾值輸入框
        self.rsi_checkbox.toggled.connect(self.toggle_rsi_input)

        # 將勾選框和輸入框放在同一行
        self.rsi_checkbox_layout.addWidget(self.rsi_checkbox)
        self.rsi_checkbox_layout.addWidget(self.buy_condition_value_input)

        buy_condition_layout.addWidget(self.buy_condition_label)
        buy_condition_layout.addWidget(self.buy_volume_checkbox)
        buy_condition_layout.addLayout(self.rsi_checkbox_layout)

        # 加倉條件設置
        add_position_layout = QHBoxLayout()
        self.add_position_label = QLabel("加倉條件：")
        self.add_position_input = QComboBox()
        self.add_position_input.addItems(["價格突破上軌", "RSI>70", "MACD黃金交叉"])
        add_position_layout.addWidget(self.add_position_label)
        add_position_layout.addWidget(self.add_position_input)

        # 減倉條件設置
        reduce_position_layout = QHBoxLayout()
        self.reduce_position_label = QLabel("減倉條件：")
        self.reduce_position_input = QComboBox()
        self.reduce_position_input.addItems(["價格跌破下軌", "RSI<30", "MACD死叉"])
        reduce_position_layout.addWidget(self.reduce_position_label)
        reduce_position_layout.addWidget(self.reduce_position_input)

        # 停損條件設置
        stop_loss_layout = QHBoxLayout()
        self.stop_loss_label = QLabel("停損條件：")
        self.stop_loss_input = QComboBox()
        self.stop_loss_input.addItems(["固定百分比停損", "ATR停損", "布林通道停損"])
        stop_loss_layout.addWidget(self.stop_loss_label)
        stop_loss_layout.addWidget(self.stop_loss_input)

        left_layout.addLayout(buy_condition_layout)
        left_layout.addLayout(add_position_layout)
        left_layout.addLayout(reduce_position_layout)
        left_layout.addLayout(stop_loss_layout)

        # 右側：進場與倉位設置
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(20)

        # 進場金額設置
        self.entry_amount_label = QLabel("進場金額：")
        self.entry_amount_input = QLineEdit(self)
        self.entry_amount_input.setPlaceholderText("輸入金額")
        
        # 倍數設置
        self.leverage_label = QLabel("倍數：")
        self.leverage_input = QLineEdit(self)
        self.leverage_input.setPlaceholderText("輸入倍數")

        # 減倉比例設置
        self.reduce_position_percentage_label = QLabel("減倉比例：")
        self.reduce_position_percentage_input = QLineEdit(self)
        self.reduce_position_percentage_input.setPlaceholderText("輸入減倉比例")

        # 加倉比例設置
        self.add_position_percentage_label = QLabel("加倉比例：")
        self.add_position_percentage_input = QLineEdit(self)
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
        self.set_conditions_btn = QPushButton("設置條件", self)
        self.set_conditions_btn.clicked.connect(self.set_conditions)

        # 添加按鈕到右側布局
        right_layout.addWidget(self.set_conditions_btn)

        # 把左右布局加入主布局
        main_layout.addLayout(left_layout, 3)  # 左側占3/4
        main_layout.addLayout(right_layout, 1)  # 右側占1/4

        self.setLayout(main_layout)

    def toggle_rsi_input(self):
        # 根據是否勾選RSI條件顯示/隱藏閾值輸入框
        if self.rsi_checkbox.isChecked():
            self.buy_condition_value_input.setVisible(True)
        else:
            self.buy_condition_value_input.setVisible(False)

    def set_conditions(self):
        # 獲取用戶選擇的買進條件
        buy_conditions = []
        if self.buy_volume_checkbox.isChecked():
            buy_conditions.append("成交量暴增")
        if self.rsi_checkbox.isChecked():
            buy_conditions.append("RSI<30")
            rsi_value = self.buy_condition_value_input.text()  # 用戶輸入的RSI閾值
        else:
            rsi_value = None
        if self.macd_checkbox.isChecked():
            buy_conditions.append("MACD黃金交叉")

        # 獲取用戶輸入的RSI閾值，若有
        if rsi_value:
            print(f"RSI條件閾值: {rsi_value}")
        else:
            rsi_value = "無"

        # 其他條件設置
        add_condition = self.add_position_input.currentText()
        reduce_condition = self.reduce_position_input.currentText()
        stop_loss_condition = self.stop_loss_input.currentText()

        # 獲取右側設置的金額和比例
        entry_amount = self.entry_amount_input.text()
        leverage = self.leverage_input.text()
        reduce_position_percentage = self.reduce_position_percentage_input.text()
        add_position_percentage = self.add_position_percentage_input.text()

        # 顯示選擇的條件
        print(f"買進條件: {', '.join(buy_conditions)} (RSI閾值: {rsi_value})")
        print(f"加倉條件: {add_condition}")
        print(f"減倉條件: {reduce_condition}")
        print(f"停損條件: {stop_loss_condition}")
        print(f"進場金額: {entry_amount}")
        print(f"倍數: {leverage}")
        print(f"減倉比例: {reduce_position_percentage}")
        print(f"加倉比例: {add_position_percentage}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TradingConditionApp()
    ex.show()
    sys.exit(app.exec_())

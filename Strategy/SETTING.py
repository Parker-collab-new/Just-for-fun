import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
)
from PyQt5.QtGui import QFont
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

        # 買進條件設置 (多選框)
        buy_condition_layout = QVBoxLayout()
        self.buy_condition_label = QLabel("買進條件：")
        self.buy_condition_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.buy_volume_checkbox = QCheckBox("成交量暴增")
        
        self.rsi_checkbox_layout = QHBoxLayout()  # 水平布局放置勾選框和輸入框
        self.rsi_checkbox = QCheckBox("RSI<")
        self.buy_condition_value_input = QLineEdit(self)
        self.buy_condition_value_input.setPlaceholderText("設置閾值")
        self.buy_condition_value_input.setFixedWidth(60)
        self.buy_condition_value_input.setVisible(False)
        self.rsi_checkbox.stateChanged.connect(self.toggle_rsi_input)

        self.rsi_checkbox_layout.addWidget(self.rsi_checkbox)
        self.rsi_checkbox_layout.addWidget(self.buy_condition_value_input)

        self.macd_checkbox = QCheckBox("MACD黃金交叉")
        
        buy_condition_layout.addWidget(self.buy_condition_label)
        buy_condition_layout.addWidget(self.buy_volume_checkbox)
        buy_condition_layout.addLayout(self.rsi_checkbox_layout)
        buy_condition_layout.addWidget(self.macd_checkbox)

        left_layout.addLayout(buy_condition_layout)

        # 加倉條件設置
        add_position_layout = QVBoxLayout()
        self.add_position_label = QLabel("加倉條件：")
        self.add_position_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.add_condition_input = QComboBox()
        self.add_condition_input.addItems(["價格突破上軌", "RSI>70", "MACD黃金交叉"])

        add_position_layout.addWidget(self.add_position_label)
        add_position_layout.addWidget(self.add_condition_input)

        left_layout.addLayout(add_position_layout)

        # 減倉條件設置
        reduce_position_layout = QVBoxLayout()
        self.reduce_position_label = QLabel("減倉條件：")
        self.reduce_position_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.reduce_condition_input = QComboBox()
        self.reduce_condition_input.addItems(["價格跌破下軌", "RSI<30", "MACD死叉"])

        reduce_position_layout.addWidget(self.reduce_position_label)
        reduce_position_layout.addWidget(self.reduce_condition_input)

        left_layout.addLayout(reduce_position_layout)

        # 停損條件設置
        stop_loss_layout = QVBoxLayout()
        self.stop_loss_label = QLabel("停損條件：")
        self.stop_loss_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.stop_loss_input = QComboBox()
        self.stop_loss_input.addItems(["固定百分比停損", "ATR停損", "布林通道停損"])

        stop_loss_layout.addWidget(self.stop_loss_label)
        stop_loss_layout.addWidget(self.stop_loss_input)

        left_layout.addLayout(stop_loss_layout)

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

        self.reduce_ratio_label = QLabel("減倉比例：")
        self.reduce_ratio_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.reduce_ratio_input = QLineEdit()
        self.reduce_ratio_input.setPlaceholderText("輸入減倉比例")

        self.add_ratio_label = QLabel("加倉比例：")
        self.add_ratio_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.add_ratio_input = QLineEdit()
        self.add_ratio_input.setPlaceholderText("輸入加倉比例")

        right_frame_layout.addWidget(self.amount_label)
        right_frame_layout.addWidget(self.amount_input)
        right_frame_layout.addWidget(self.leverage_label)
        right_frame_layout.addWidget(self.leverage_input)
        right_frame_layout.addWidget(self.reduce_ratio_label)
        right_frame_layout.addWidget(self.reduce_ratio_input)
        right_frame_layout.addWidget(self.add_ratio_label)
        right_frame_layout.addWidget(self.add_ratio_input)

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

    def toggle_rsi_input(self):
        """切換 RSI 條件的輸入框顯示"""
        self.buy_condition_value_input.setVisible(self.rsi_checkbox.isChecked())

    def set_conditions(self):
        """處理用戶設置的條件"""
        buy_conditions = {
            "volume_surge": self.buy_volume_checkbox.isChecked(),
            "rsi": self.rsi_checkbox.isChecked(),
            "rsi_value": self.buy_condition_value_input.text() if self.buy_condition_value_input.text() else None,
            "macd_cross": self.macd_checkbox.isChecked()
        }
        add_condition = self.add_condition_input.currentText()
        reduce_condition = self.reduce_condition_input.currentText()
        stop_loss_condition = self.stop_loss_input.currentText()

        # 資金管理參數
        amount = self.amount_input.text()
        leverage = self.leverage_input.text()
        reduce_ratio = self.reduce_ratio_input.text()
        add_ratio = self.add_ratio_input.text()

        # Debug 輸出
        print("買進條件:", buy_conditions)
        print("加倉條件:", add_condition)
        print("減倉條件:", reduce_condition)
        print("停損條件:", stop_loss_condition)
        print("資金管理:", {
            "amount": amount,
            "leverage": leverage,
            "reduce_ratio": reduce_ratio,
            "add_ratio": add_ratio
        })

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingConditionApp()
    window.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LabelExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QLabel 範例")
        self.setGeometry(100, 100, 400, 200)

        # 創建標籤
        label1 = QLabel("這是一個普通文字標籤", self)
        label1.setFont(QFont("Arial", 14))

        label2 = QLabel("<b>這是一個加粗的富文本標籤</b>", self)  # 支援 HTML 標籤
        label2.setAlignment(Qt.AlignCenter)  # 文本居中

        label3 = QLabel("這是帶背景顏色的標籤", self)
        label3.setStyleSheet("background-color: yellow; color: blue; font-size: 16px;")

        # 將標籤添加到布局
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = LabelExample()
    window.show()
    app.exec_()

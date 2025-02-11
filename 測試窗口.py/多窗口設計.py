import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QLabel

class HomePage(QWidget):
    """主選單頁面，讓用戶選擇功能"""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        self.label = QLabel("請選擇功能：")
        self.btn_query = QPushButton("查詢系統")
        self.btn_backtest = QPushButton("回測系統")
        self.btn_settings = QPushButton("設置")

        layout.addWidget(self.label)
        layout.addWidget(self.btn_query)
        layout.addWidget(self.btn_backtest)
        layout.addWidget(self.btn_settings)
        self.setLayout(layout)

        # 設定按鈕功能
        self.btn_query.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_backtest.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

class QuerySystem(QWidget):
    """查詢系統頁面"""
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("這是查詢系統")
        self.btn_back = QPushButton("返回主選單")

        layout.addWidget(self.label)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.btn_back.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

class BacktestSystem(QWidget):
    """回測系統頁面"""
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("這是回測系統")
        self.btn_back = QPushButton("返回主選單")

        layout.addWidget(self.label)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.btn_back.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

class SettingsPage(QWidget):
    """設定頁面"""
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("這是設置頁面")
        self.btn_back = QPushButton("返回主選單")

        layout.addWidget(self.label)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.btn_back.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

class MainWindow(QWidget):
    """主窗口，管理 QStackedWidget"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多功能選單系統")

        self.stacked_widget = QStackedWidget()
        self.home_page = HomePage(self.stacked_widget)
        self.query_page = QuerySystem(self.stacked_widget)
        self.backtest_page = BacktestSystem(self.stacked_widget)
        self.settings_page = SettingsPage(self.stacked_widget)

        self.stacked_widget.addWidget(self.home_page)    # index 0
        self.stacked_widget.addWidget(self.query_page)   # index 1
        self.stacked_widget.addWidget(self.backtest_page) # index 2
        self.stacked_widget.addWidget(self.settings_page) # index 3

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

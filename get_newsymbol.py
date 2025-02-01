import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class BinanceUSDTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("USDT 本位交易排行")
        self.setGeometry(100, 100, 500, 700)

        layout = QVBoxLayout()

        # 標題
        self.title_label = QLabel("📊 USDT 本位交易排行", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # 交易金額排行
        self.volume_label = QLabel("🔥 交易金額排行 (USDT)", self)
        self.volume_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.volume_list = QListWidget(self)

        # 漲幅排行
        self.gain_label = QLabel("📈 漲幅排行 (%)", self)
        self.gain_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        self.gain_list = QListWidget(self)

        # 跌幅排行
        self.loss_label = QLabel("📉 跌幅排行 (%)", self)
        self.loss_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        self.loss_list = QListWidget(self)

        # 更新按鈕
        self.update_button = QPushButton("🔄 更新排行", self)
        self.update_button.clicked.connect(self.fetch_rankings)

        # 佈局
        layout.addWidget(self.title_label)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_list)
        layout.addWidget(self.gain_label)
        layout.addWidget(self.gain_list)
        layout.addWidget(self.loss_label)
        layout.addWidget(self.loss_list)
        layout.addWidget(self.update_button)

        self.setLayout(layout)
        self.fetch_rankings()  # 啟動時自動加載數據

    def fetch_rankings(self):
        """從幣安 API 獲取 USDT 交易對的交易量、漲幅和跌幅排行"""
        url = "https://api.binance.com/api/v3/ticker/24hr"

        try:
            response = requests.get(url)
            data = response.json()

            # 篩選 USDT 本位交易對
            usdt_pairs = [item for item in data if item['symbol'].endswith("USDT")]

            # 按 24h 交易量排序
            sorted_by_volume = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)[:10]

            # 按漲跌幅排序
            sorted_by_gain = sorted(usdt_pairs, key=lambda x: float(x['priceChangePercent']), reverse=True)[:10]
            sorted_by_loss = sorted(usdt_pairs, key=lambda x: float(x['priceChangePercent']))[:10]

            # 清空列表
            self.volume_list.clear()
            self.gain_list.clear()
            self.loss_list.clear()

            # 顯示交易量排行
            for item in sorted_by_volume:
                symbol = item['symbol']
                volume = float(item['quoteVolume'])
                self.volume_list.addItem(f"{symbol}: ${volume:,.2f}")

            # 顯示漲幅排行（綠色字體）
            for item in sorted_by_gain:
                symbol = item['symbol']
                change = float(item['priceChangePercent'])
                list_item = QListWidgetItem(f"{symbol}: +{change:.2f}%")
                list_item.setForeground(QColor("green"))  # 設定字體顏色為綠色
                self.gain_list.addItem(list_item)

            # 顯示跌幅排行（紅色字體）
            for item in sorted_by_loss:
                symbol = item['symbol']
                change = float(item['priceChangePercent'])
                list_item = QListWidgetItem(f"{symbol}: {change:.2f}%")
                list_item.setForeground(QColor("red"))  # 設定字體顏色為紅色
                self.loss_list.addItem(list_item)

        except Exception as e:
            self.volume_list.addItem(f"獲取數據失敗: {str(e)}")
            self.gain_list.addItem(f"獲取數據失敗: {str(e)}")
            self.loss_list.addItem(f"獲取數據失敗: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BinanceUSDTApp()
    window.show()
    sys.exit(app.exec_())

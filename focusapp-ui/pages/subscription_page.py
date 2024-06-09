from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class SubscriptionPage(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(0, 100, 0, 0)

        subscriptionLabel = QLabel(f"Ваш айди - {self.user_data['username']}", self)
        subscriptionLabel.setStyleSheet("color: white; font-size: 50px;")
        subscriptionInfoLabel = QLabel("Купить подписку можно\nв нашем телеграм-боте", self)
        subscriptionInfoLabel.setStyleSheet("color: white; font-size: 50px;")

        telegramButton = QPushButton("Перейти в телеграм-бот", self)
        telegramButton.setFixedSize(300, 50)
        telegramButton.setStyleSheet("""
            background-color: white;
            color: #282B3A;
            border-radius: 10px;
            font-size: 18px;
        """)
        telegramButton.clicked.connect(self.open_telegram_bot)

        layout.addWidget(subscriptionLabel)
        layout.addSpacing(20)
        layout.addWidget(subscriptionInfoLabel)
        layout.addSpacing(20)
        layout.addWidget(telegramButton)
        self.setLayout(layout)

    def open_telegram_bot(self):
        import webbrowser
        webbrowser.open("https://t.me/your_telegram_bot")

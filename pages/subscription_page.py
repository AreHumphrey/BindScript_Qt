from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class SubscriptionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel("Ваш айди - Artem#1\nКупить подписку можно в нашем телеграм-боте", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        telegramButton = QPushButton("Перейти в телеграм-бот", self)
        telegramButton.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        layout.addWidget(label)
        layout.addWidget(telegramButton)
        self.setLayout(layout)
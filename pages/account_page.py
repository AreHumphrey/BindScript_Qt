from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class AccountPage(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(200, 100, 0, 0)

        subscriptionLayout = QVBoxLayout()
        subscriptionLayout.setAlignment(Qt.AlignCenter)

        subscriptionLabel = QLabel("Подписка", self)
        subscriptionLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        subscriptionEndLabel = QLabel(f"Активна до {self.user_data['subscription_end']}", self)
        subscriptionEndLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        subscriptionBox = QWidget()
        subscriptionBox.setFixedWidth(400)
        subscriptionBox.setLayout(subscriptionLayout)
        subscriptionBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        subscriptionLayout.addWidget(subscriptionLabel)
        subscriptionLayout.addWidget(subscriptionEndLabel)

        registrationLayout = QVBoxLayout()
        registrationLayout.setAlignment(Qt.AlignCenter)

        registrationLabel = QLabel("Дата регистрации", self)
        registrationLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        registrationDateLabel = QLabel(self.user_data['registration_date'], self)
        registrationDateLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        registrationBox = QWidget()
        registrationBox.setFixedWidth(400)
        registrationBox.setLayout(registrationLayout)
        registrationBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        registrationLayout.addWidget(registrationLabel)
        registrationLayout.addWidget(registrationDateLabel)

        containerLayout = QVBoxLayout()
        containerLayout.setAlignment(Qt.AlignCenter)
        containerLayout.addWidget(subscriptionBox)
        containerLayout.addSpacing(20)
        containerLayout.addWidget(registrationBox)

        containerBox = QWidget()
        containerBox.setLayout(containerLayout)
        containerBox.setStyleSheet("border: none;")

        layout.addWidget(containerBox)
        self.setLayout(layout)

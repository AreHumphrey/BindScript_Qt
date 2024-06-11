
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
import requests

class AccountPage(QWidget):
    def __init__(self, user_data, switch_to_change_password):
        super().__init__()
        self.user_data = user_data
        self.switch_to_change_password = switch_to_change_password
        self.tokens = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.layout.setContentsMargins(200, 100, 0, 0)

        self.usernameLabel = QLabel(f"Имя пользователя: {self.user_data.get('username', '---')}", self)
        self.usernameLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")

        self.subscriptionLayout = QVBoxLayout()
        self.subscriptionLayout.setAlignment(Qt.AlignCenter)

        self.subscriptionLabel = QLabel("Подписка", self)
        self.subscriptionLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        self.subscriptionEndLabel = QLabel(f"Активна до {self.user_data.get('subscription_end', '---')}", self)
        self.subscriptionEndLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        self.subscriptionBox = QWidget()
        self.subscriptionBox.setFixedWidth(400)
        self.subscriptionBox.setLayout(self.subscriptionLayout)
        self.subscriptionBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        self.subscriptionLayout.addWidget(self.subscriptionLabel)
        self.subscriptionLayout.addWidget(self.subscriptionEndLabel)

        self.registrationLayout = QVBoxLayout()
        self.registrationLayout.setAlignment(Qt.AlignCenter)

        self.registrationLabel = QLabel("Дата регистрации", self)
        self.registrationLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        self.registrationDateLabel = QLabel(self.user_data.get('registration_date', '---'), self)
        self.registrationDateLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        self.registrationBox = QWidget()
        self.registrationBox.setFixedWidth(400)
        self.registrationBox.setLayout(self.registrationLayout)
        self.registrationBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        self.registrationLayout.addWidget(self.registrationLabel)
        self.registrationLayout.addWidget(self.registrationDateLabel)

        self.containerLayout = QVBoxLayout()
        self.containerLayout.setAlignment(Qt.AlignCenter)
        self.containerLayout.addWidget(self.usernameLabel)
        self.containerLayout.addWidget(self.subscriptionBox)
        self.containerLayout.addSpacing(20)
        self.containerLayout.addWidget(self.registrationBox)

        self.change_password_button = QPushButton("Изменить пароль")
        self.change_password_button.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)
        self.change_password_button.clicked.connect(self.switch_to_change_password)

        self.containerBox = QWidget()
        self.containerBox.setLayout(self.containerLayout)
        self.containerBox.setStyleSheet("border: none;")

        self.layout.addWidget(self.containerBox)
        self.layout.addWidget(self.change_password_button)
        self.setLayout(self.layout)

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.update_user_data()

    def update_user_data(self):
        if not self.tokens:
            return

        try:
            response = requests.get('http://127.0.0.1:8000/api/users/me/', headers={
                'Authorization': f'Bearer {self.tokens["access"]}'
            })

            if response.status_code == 200:
                user_data = response.json()
                self.usernameLabel.setText(f"Имя пользователя: {user_data.get('username', '---')}")
                self.subscriptionEndLabel.setText(f"Активна до {user_data.get('subscription_end', '---')}")
                self.registrationDateLabel.setText(user_data.get('registration_date', '---'))
                print(f"Fetched user data: {user_data}")
            else:
                print(f"Failed to fetch user data, status code: {response.status_code}")
        except Exception as e:
            print(f"Error while fetching user data: {e}")

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_user_data)
        self.timer.start(5000)


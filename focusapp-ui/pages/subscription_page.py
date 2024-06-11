from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import requests
import datetime
import webbrowser
import jwt

class SubscriptionPage(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.tokens = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(0, 100, 0, 0)

        self.usernameLabel = QLabel(f"Ваш айди - {self.user_data.get('username', '---')}", self)
        self.usernameLabel.setStyleSheet("color: white; font-size: 50px;")
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

        layout.addWidget(self.usernameLabel)
        layout.addSpacing(20)
        layout.addWidget(subscriptionInfoLabel)
        layout.addSpacing(20)
        layout.addWidget(telegramButton)
        self.setLayout(layout)

    def open_telegram_bot(self):
        webbrowser.open("https://t.me/Focusapp_bot")

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.update_user_data()

    def update_user_data(self):
        if not self.tokens:
            return

        if self.is_token_expired(self.tokens["access"]):
            if not self.refresh_token():
                print("Failed to refresh token")
                return

        try:
            response = requests.get('http://46.101.81.78/api/users/me/', headers={
                'Authorization': f'Bearer {self.tokens["access"]}'
            })

            if response.status_code == 200:
                user_data = response.json()
                self.user_data.update(user_data)
                self.usernameLabel.setText(f"Ваш айди - {self.user_data.get('username', '---')}")
            elif response.status_code == 401:
                if self.refresh_token():
                    response = requests.get('http://46.101.81.78/api/users/me/', headers={
                        'Authorization': f'Bearer {self.tokens["access"]}'
                    })
                    if response.status_code == 200:
                        user_data = response.json()
                        self.user_data.update(user_data)
                        self.usernameLabel.setText(f"Ваш айди - {self.user_data.get('username', '---')}")
                    else:
                        print(f"Failed to fetch user data after refresh, status code: {response.status_code}, response: {response.json()}")
                else:
                    print("Failed to refresh token after receiving 401")
            else:
                print(f"Failed to fetch user data, status code: {response.status_code}, response: {response.json()}")
        except Exception as e:
            print(f"Error while fetching user data: {e}")

    def is_token_expired(self, token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = datetime.datetime.fromtimestamp(payload['exp'])
            return exp < datetime.datetime.utcnow()
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True

    def refresh_token(self):
        try:
            response = requests.post('http://46.101.81.78/api/token/refresh/', data={
                'refresh': self.tokens["refresh"]
            })

            if response.status_code == 200:
                new_tokens = response.json()
                self.tokens.update(new_tokens)
                print("Token refreshed successfully")
                return True
            else:
                print(f"Failed to refresh token, status code: {response.status_code}, response: {response.json()}")
                return False
        except Exception as e:
            print(f"Error while refreshing token: {e}")
            return False

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
import requests
import datetime
import jwt

class AccountPage(QWidget):
    def __init__(self, user_data, switch_to_change_password):
        super().__init__()
        self.user_data = user_data
        self.switch_to_change_password = switch_to_change_password
        self.tokens = None
        self.initUI()
        self.start_timer()

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
        self.subscriptionEndLabel = QLabel(f"Активна до {self.format_date(self.user_data.get('subscription_end', '---'))}", self)
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
        self.registrationDateLabel = QLabel(self.format_date(self.user_data.get('registration_date', '---')), self)
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

    def format_date(self, date_str):
        try:
            date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return '---'

    def update_user_data(self):
        if not self.tokens:
            return

        if self.is_token_expired(self.tokens["access"]):
            if not self.refresh_token():
                print("Failed to refresh token")
                return

        try:
            response = requests.get('http://127.0.0.1:8000/api/users/me/', headers={
                'Authorization': f'Bearer {self.tokens["access"]}'
            })

            if response.status_code == 200:
                user_data = response.json()
                self.usernameLabel.setText(f"Имя пользователя: {user_data.get('username', '---')}")
                self.subscriptionEndLabel.setText(f"Активна до {self.format_date(user_data.get('subscription_end', '---') or '---')}")
                self.registrationDateLabel.setText(self.format_date(user_data.get('registration_date', '---')))
                print(f"Fetched user data: {user_data}")
            elif response.status_code == 401:
                if self.refresh_token():
                    response = requests.get('http://127.0.0.1:8000/api/users/me/', headers={
                        'Authorization': f'Bearer {self.tokens["access"]}'
                    })
                    if response.status_code == 200:
                        user_data = response.json()
                        self.usernameLabel.setText(f"Имя пользователя: {user_data.get('username', '---')}")
                        self.subscriptionEndLabel.setText(f"Активна до {self.format_date(user_data.get('subscription_end', '---') or '---')}")
                        self.registrationDateLabel.setText(self.format_date(user_data.get('registration_date', '---')))
                        print(f"Fetched user data: {user_data}")
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
            response = requests.post('http://127.0.0.1:8000/api/token/refresh/', data={
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

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_user_data)
        self.timer.start(10000)

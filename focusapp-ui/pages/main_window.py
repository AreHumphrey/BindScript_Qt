from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import requests
import datetime
import jwt

from .account_page import AccountPage
from .binds_page import BindsPage
from .subscription_page import SubscriptionPage
from .settings_page import SettingsPage
from .change_password_page import ChangePasswordPage


class MainWindow(QWidget):
    def __init__(self, switch_to_login, main_app):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.main_app = main_app
        self.tokens = None
        self.user_data = {
            "username": "---",
            "subscription_end": "---",
            "registration_date": "---"
        }
        self.initUI()
        self.start_timer()

    def initUI(self):
        self.setWindowTitle("FocusAPP")
        self.resize(1280, 720)

        # Основной макет
        mainLayout = QVBoxLayout(self)

        # Верхняя панель
        topLayout = QHBoxLayout()
        topLayout.setAlignment(Qt.AlignRight)
        self.userLabel = QLabel(self.user_data["username"])
        self.userLabel.setStyleSheet("color: white; font-size: 24px; ")
        logoutButton = QPushButton("выйти")
        logoutButton.setFixedSize(100, 40)
        logoutButton.setStyleSheet("color: white; background-color: #282B3A; border: none; font-size: 24px;")
        logoutButton.clicked.connect(self.logout)
        topLayout.addWidget(self.userLabel)
        topLayout.addWidget(logoutButton)

        leftLayout = QVBoxLayout()
        titleLabel = QLabel("FocusAPP")
        titleLabel.setFont(QFont("Arial", 30, QFont.Bold))
        titleLabel.setStyleSheet("color: white;")
        titleLabel.setAlignment(Qt.AlignLeft)
        leftLayout.addWidget(titleLabel)

        self.listWidget = QListWidget(self)
        self.listWidget.addItem("Аккаунт")
        self.listWidget.addItem("Бинды")
        self.listWidget.addItem("Подписка")
        self.listWidget.addItem("Настройки")
        self.listWidget.setFixedWidth(250)
        self.listWidget.setFixedHeight(400)
        self.listWidget.setStyleSheet("""
            QListWidget {
                color: white;
                background-color: #282B3A;
                font-size: 40px;
                border: none;
            }
            QListWidget::item {
                padding: 20px;
                border: none;
                background-color: #282B3A;
            }
            QListWidget::item:selected {
                color: #7B7FA2;
                background-color: #282B3A;
                border: none;
            }
        """)

        # Виджет с переключающимися страницами
        self.contentWidget = QStackedWidget(self)
        self.accountPage = AccountPage(self.user_data, self.switch_to_change_password)
        self.subscriptionPage = SubscriptionPage(self.user_data)
        self.contentWidget.addWidget(self.accountPage)
        self.contentWidget.addWidget(BindsPage())
        self.contentWidget.addWidget(self.subscriptionPage)
        self.contentWidget.addWidget(SettingsPage())
        self.changePasswordPage = ChangePasswordPage(self.switch_to_account, self.tokens)
        self.contentWidget.addWidget(self.changePasswordPage)

        self.listWidget.currentRowChanged.connect(self.handle_page_change)

        leftLayout.addWidget(self.listWidget)
        leftLayout.addStretch()

        contentLayout = QHBoxLayout()
        contentLayout.addLayout(leftLayout, 1)
        contentLayout.addWidget(self.contentWidget, 3)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(contentLayout)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setLayout(mainLayout)

    def handle_page_change(self, index):
        if index == 1:
            subscription_end = self.user_data.get('subscription_end', None)
            if subscription_end:
                try:
                    end_date = datetime.datetime.fromisoformat(subscription_end.replace('Z', '+00:00'))
                    if end_date < datetime.datetime.now():
                        self.listWidget.setCurrentRow(0)
                        QMessageBox.warning(self, "Доступ запрещен", "Ваша подписка истекла. Пожалуйста, обновите подписку.")
                        return
                except ValueError:
                    self.listWidget.setCurrentRow(0)
                    QMessageBox.warning(self, "Доступ запрещен", "Неправильная дата окончания подписки. Пожалуйста, свяжитесь с поддержкой.")
                    return
            else:
                self.listWidget.setCurrentRow(0)
                QMessageBox.warning(self, "Доступ запрещен", "Подписка не найдена. Пожалуйста, приобретите подписку.")
                return
        self.contentWidget.setCurrentIndex(index)

    def switch_to_change_password(self):
        self.changePasswordPage.tokens = self.tokens
        self.contentWidget.setCurrentWidget(self.changePasswordPage)

    def switch_to_account(self):
        self.contentWidget.setCurrentWidget(self.accountPage)

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.accountPage.set_tokens(tokens)
        self.subscriptionPage.set_tokens(tokens)
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
                print(f"User data: {user_data}")
                self.user_data.update(user_data)
                self.userLabel.setText(self.user_data["username"])
                self.accountPage.update_user_data(user_data)
                self.subscriptionPage.update_user_data(user_data)
            elif response.status_code == 401:
                if self.refresh_token():
                    response = requests.get('http://46.101.81.78/api/users/me/', headers={
                        'Authorization': f'Bearer {self.tokens["access"]}'
                    })
                    if response.status_code == 200:
                        user_data = response.json()
                        self.user_data.update(user_data)
                        self.userLabel.setText(self.user_data["username"])
                        self.accountPage.update_user_data(user_data)
                        self.subscriptionPage.update_user_data(user_data)
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

    def logout(self):
        self.tokens = None
        self.user_data = {
            "username": "---",
            "subscription_end": "---",
            "registration_date": "---"
        }
        self.switch_to_login()

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_user_data)
        self.timer.start(10000)

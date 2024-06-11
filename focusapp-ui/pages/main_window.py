from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import requests

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
        logoutButton.clicked.connect(self.switch_to_login)
        topLayout.addWidget(self.userLabel)
        topLayout.addWidget(logoutButton)

        # Левый боковой список
        leftLayout = QVBoxLayout()
        titleLabel = QLabel("FocusAPP")
        titleLabel.setFont(QFont("Arial", 30, QFont.Bold))
        titleLabel.setStyleSheet("color: white;")
        titleLabel.setAlignment(Qt.AlignLeft)
        leftLayout.addWidget(titleLabel)

        listWidget = QListWidget(self)
        listWidget.addItem("Аккаунт")
        listWidget.addItem("Бинды")
        listWidget.addItem("Подписка")
        listWidget.addItem("Настройки")
        listWidget.setFixedWidth(250)
        listWidget.setFixedHeight(400)
        listWidget.setStyleSheet("""
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
        self.contentWidget.addWidget(self.accountPage)
        self.contentWidget.addWidget(BindsPage())
        self.contentWidget.addWidget(SubscriptionPage(self.user_data))
        self.contentWidget.addWidget(SettingsPage())
        self.changePasswordPage = ChangePasswordPage(self.switch_to_account, self.tokens)
        self.contentWidget.addWidget(self.changePasswordPage)

        listWidget.currentRowChanged.connect(self.contentWidget.setCurrentIndex)

        leftLayout.addWidget(listWidget)
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

    def switch_to_change_password(self):
        self.changePasswordPage.tokens = self.tokens  # Ensure tokens are set before switching
        self.contentWidget.setCurrentWidget(self.changePasswordPage)

    def switch_to_account(self):
        self.contentWidget.setCurrentWidget(self.accountPage)

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.accountPage.set_tokens(tokens)
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
                print(f"User data: {user_data}")
                self.user_data.update(user_data)
                self.userLabel.setText(self.user_data["username"])
                self.accountPage.update_user_data(user_data)
            else:
                print(f"Failed to fetch user data, status code: {response.status_code}, response: {response.json()}")
        except Exception as e:
            print(f"Error while fetching user data: {e}")

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_user_data)
        self.timer.start(5000)

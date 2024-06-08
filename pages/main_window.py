from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from pages.account_page import AccountPage
from pages.binds_page import BindsPage
from pages.subscription_page import SubscriptionPage
from pages.settings_page import SettingsPage

class MainWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.user_data = {
            "username": "Artem#1",
            "subscription_end": "08.01.2023",
            "registration_date": "08.01.2032",
            "binds": {
                "Уборная": "-",
                "Полы": "-",
                "Бургеры": "-",
                "Мусор": "U"
            }
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FocusAPP")
        self.resize(1280, 720)

        # Основной макет
        mainLayout = QVBoxLayout(self)

        # Верхняя панель
        topLayout = QHBoxLayout()
        topLayout.setAlignment(Qt.AlignRight)  # Выровнять элементы по правому краю
        userLabel = QLabel(self.user_data["username"])
        userLabel.setStyleSheet("color: white; font-size: 24px;")
        logoutButton = QPushButton("выйти")
        logoutButton.setFixedSize(100, 40)
        logoutButton.setStyleSheet("color: white; background-color: #282B3A; border: none; font-size: 24px;")
        logoutButton.clicked.connect(self.switch_to_login)
        topLayout.addWidget(userLabel)
        topLayout.addWidget(logoutButton)

        # Левый боковой список
        leftLayout = QVBoxLayout()
        titleLabel = QLabel("FocusAPP")
        titleLabel.setFont(QFont("Arial", 24, QFont.Bold))
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
                font-size: 24px;
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
        contentWidget = QStackedWidget(self)
        contentWidget.setContentsMargins(0, 30, 0, 0)  # Добавить верхний отступ в 30 пикселей
        accountPage = AccountPage(self.user_data)
        contentWidget.addWidget(accountPage)
        bindsPage = BindsPage(self.user_data["binds"])  # Передача данных биндов
        contentWidget.addWidget(bindsPage)
        subscriptionPage = SubscriptionPage(self.user_data)  # Передача данных пользователя
        contentWidget.addWidget(subscriptionPage)
        settingsPage = SettingsPage()
        contentWidget.addWidget(settingsPage)

        listWidget.currentRowChanged.connect(contentWidget.setCurrentIndex)

        leftLayout.addWidget(listWidget)
        leftLayout.addStretch()

        # Создание горизонтального макета для контента
        contentLayout = QHBoxLayout()
        contentLayout.addLayout(leftLayout, 1)
        contentLayout.addWidget(contentWidget, 3)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(contentLayout)

        # Настройка фона
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setLayout(mainLayout)

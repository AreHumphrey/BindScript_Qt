from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FocusAPP")
        self.resize(1280, 720)

        # Основной макет
        mainLayout = QHBoxLayout(self)

        # Левый боковой список
        listWidget = QListWidget(self)
        listWidget.addItem("Аккаунт")
        listWidget.addItem("Бинды")
        listWidget.addItem("Подписка")
        listWidget.addItem("Настройки")
        listWidget.setFixedWidth(250)
        listWidget.setFixedHeight(400)  # Ensure all items are visible without scrolling
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

        # Страница "Аккаунт"
        accountPage = QWidget()
        accountLayout = QVBoxLayout(accountPage)
        accountLabel = QLabel("Ваш айди - Artem#1\nПодписка активна до 08.01.2023\nДата регистрации: 08.01.2032", self)
        accountLabel.setStyleSheet("color: white; font-size: 18px;")
        accountLayout.addWidget(accountLabel)
        contentWidget.addWidget(accountPage)

        # Страница "Бинды"
        bindsPage = QWidget()
        bindsLayout = QVBoxLayout(bindsPage)
        bindsLabel = QLabel("Управление биндами", self)
        bindsLabel.setStyleSheet("color: white; font-size: 18px;")
        bindsLayout.addWidget(bindsLabel)
        contentWidget.addWidget(bindsPage)

        # Страница "Подписка"
        subscriptionPage = QWidget()
        subscriptionLayout = QVBoxLayout(subscriptionPage)
        subscriptionLabel = QLabel("Ваш айди - Artem#1\nКупить подписку можно в нашем телеграм-боте", self)
        subscriptionLabel.setStyleSheet("color: white; font-size: 18px;")
        telegramButton = QPushButton("Перейти в телеграм-бот", self)
        telegramButton.setStyleSheet("background-color: white; color: black; border-radius: 10px;")
        subscriptionLayout.addWidget(subscriptionLabel)
        subscriptionLayout.addWidget(telegramButton)
        contentWidget.addWidget(subscriptionPage)

        # Страница "Настройки"
        settingsPage = QWidget()
        settingsLayout = QVBoxLayout(settingsPage)
        settingsLabel = QLabel("Внимание - скрипт работает только на разрешении экрана 1920x1080.\nВ дальнейшем мы добавим другие разрешения", self)
        settingsLabel.setStyleSheet("color: white; font-size: 18px;")
        settingsLayout.addWidget(settingsLabel)
        contentWidget.addWidget(settingsPage)

        listWidget.currentRowChanged.connect(contentWidget.setCurrentIndex)

        # Верхняя панель
        topLayout = QHBoxLayout()
        userLabel = QLabel("Artem#1")
        userLabel.setStyleSheet("color: white; font-size: 18px;")
        logoutButton = QPushButton("выйти")
        logoutButton.setStyleSheet("color: white; background-color: #282B3A; border: none;")
        logoutButton.clicked.connect(self.switch_to_login)
        topLayout.addWidget(userLabel)
        topLayout.addStretch()
        topLayout.addWidget(logoutButton)

        leftLayout = QVBoxLayout()
        titleLabel = QLabel("FocusAPP")
        titleLabel.setFont(QFont("Arial", 24, QFont.Bold))
        titleLabel.setStyleSheet("color: white;")
        titleLabel.setAlignment(Qt.AlignCenter)
        leftLayout.addWidget(titleLabel)
        leftLayout.addLayout(topLayout)
        leftLayout.addWidget(listWidget)
        leftLayout.addStretch()

        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addWidget(contentWidget, 3)

        # Настройка фона
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setLayout(mainLayout)

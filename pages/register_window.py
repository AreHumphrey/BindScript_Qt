from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class RegisterWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FocusAPP")
        self.resize(960, 540)

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter)

        headerLayout = QHBoxLayout()
        headerLayout.setAlignment(Qt.AlignLeft)
        titleLabel = QLabel("FocusAPP")
        titleLabel.setFont(QFont("Arial", 24, QFont.Bold))
        titleLabel.setStyleSheet("color: white; padding: 20px; font-weight: bold;")
        headerLayout.addWidget(titleLabel)
        mainLayout.addLayout(headerLayout)

        # Добавление заголовка "Регистрация"
        subtitleLabel = QLabel("Регистрация")
        subtitleLabel.setFont(QFont("Arial", 26))
        subtitleLabel.setAlignment(Qt.AlignCenter)
        subtitleLabel.setStyleSheet("color: white; font-weight: bold; ")
        mainLayout.addWidget(subtitleLabel)

        mainLayout.addStretch(1)

        inputLayout = QVBoxLayout()
        inputLayout.setAlignment(Qt.AlignCenter)

        usernameInput = QLineEdit()
        usernameInput.setPlaceholderText("Логин")
        usernameInput.setFixedHeight(60)
        usernameInput.setFixedWidth(self.width() // 2)
        usernameInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        passwordInput = QLineEdit()
        passwordInput.setPlaceholderText("Пароль")
        passwordInput.setFixedHeight(60)
        passwordInput.setFixedWidth(self.width() // 2)
        passwordInput.setEchoMode(QLineEdit.Password)
        passwordInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        confirmPasswordInput = QLineEdit()
        confirmPasswordInput.setPlaceholderText("Повторите пароль")
        confirmPasswordInput.setFixedHeight(60)
        confirmPasswordInput.setFixedWidth(self.width() // 2)
        confirmPasswordInput.setEchoMode(QLineEdit.Password)
        confirmPasswordInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        inputLayout.addWidget(usernameInput)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(passwordInput)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(confirmPasswordInput)
        inputLayout.addSpacing(40)

        # Кнопка регистрации
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        registerButton = QPushButton("Зарегистрироваться")
        registerButton.setFixedHeight(30)
        registerButton.setFixedWidth(self.width() // 3)
        registerButton.setStyleSheet("""
            background-color: white;
            color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
        """)
        buttonLayout.addWidget(registerButton)

        # Ссылка на вход
        loginLabel = QPushButton("Есть аккаунт? Войти")
        loginLabel.setFont(QFont("Arial", 10))
        loginLabel.setStyleSheet("color: #2D8CFF; background-color: transparent; border: none;")
        loginLabel.clicked.connect(self.switch_to_login)

        inputLayout.addLayout(buttonLayout)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(loginLabel)

        mainLayout.addLayout(inputLayout)
        mainLayout.addStretch(1)

        # Настройка фона
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

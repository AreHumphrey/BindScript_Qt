import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import re

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
        titleLabel.setFont(QFont("Arial", 30, QFont.Bold))
        titleLabel.setStyleSheet("color: white; padding: 20px; font-weight: bold;")
        headerLayout.addWidget(titleLabel)
        mainLayout.addLayout(headerLayout)

        spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mainLayout.addItem(spacer)

        subtitleLabel = QLabel("Регистрация")
        subtitleLabel.setFont(QFont("Arial", 30, QFont.Bold))
        subtitleLabel.setAlignment(Qt.AlignCenter)
        subtitleLabel.setStyleSheet("color: white; font-weight: bold; ")
        mainLayout.addWidget(subtitleLabel)

        mainLayout.addStretch(1)

        inputLayout = QVBoxLayout()
        inputLayout.setAlignment(Qt.AlignCenter)

        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Логин")
        self.usernameInput.setFixedHeight(60)
        self.usernameInput.setFixedWidth(self.width() // 2)
        self.usernameInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("Email")
        self.emailInput.setFixedHeight(60)
        self.emailInput.setFixedWidth(self.width() // 2)
        self.emailInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        self.passwordInput = QLineEdit()
        self.passwordInput.setPlaceholderText("Пароль")
        self.passwordInput.setFixedHeight(60)
        self.passwordInput.setFixedWidth(self.width() // 2)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setPlaceholderText("Повторите пароль")
        self.confirmPasswordInput.setFixedHeight(60)
        self.confirmPasswordInput.setFixedWidth(self.width() // 2)
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)
        self.confirmPasswordInput.setStyleSheet("""
            background-color: #282B3A;
            color: white;
            border: 2px solid white;
            border-radius: 30px;
            padding: 20px;
            font-size: 18px;
        """)

        inputLayout.addWidget(self.usernameInput)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(self.emailInput)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(self.passwordInput)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(self.confirmPasswordInput)
        inputLayout.addSpacing(40)

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
        registerButton.clicked.connect(self.handle_register)

        loginLabel = QPushButton("Есть аккаунт? Войти")
        loginLabel.setFont(QFont("Arial", 10))
        loginLabel.setStyleSheet("color: #2D8CFF; background-color: transparent; border: none;")
        loginLabel.clicked.connect(self.switch_to_login)

        inputLayout.addLayout(buttonLayout)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(loginLabel)

        mainLayout.addLayout(inputLayout)
        mainLayout.addStretch(1)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def handle_register(self):
        username = self.usernameInput.text()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        confirm_password = self.confirmPasswordInput.text()

        if not self.validate_username(username):
            self.show_error("Логин должен быть от 3 до 20 символов и может содержать только буквы, цифры и символы подчеркивания.")
            return

        if not self.validate_email(email):
            self.show_error("Введите действительный email.")
            return

        if not self.validate_password(password):
            self.show_error("Пароль должен быть от 8 до 20 символов, содержать заглавную букву, строчную букву, цифру и специальный символ.")
            return

        if password != confirm_password:
            self.show_error("Пароли не совпадают")
            return

        response = requests.post('http://pybyte.ru/api/users/register/', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        })

        if response.status_code == 201:
            self.switch_to_login()
        else:
            self.show_error("Ошибка регистрации")

    def validate_username(self, username):
        return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

    def validate_email(self, email):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

    def validate_password(self, password):
        return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password) is not None

    def show_error(self, message):
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red;")
        self.layout().addWidget(error_label)

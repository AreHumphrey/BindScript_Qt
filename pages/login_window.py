from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, switch_to_register, switch_to_main):
        super().__init__()
        self.switch_to_register = switch_to_register
        self.switch_to_main = switch_to_main
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

        subtitleLabel = QLabel("Войти")
        subtitleLabel.setFont(QFont("Arial", 30, QFont.Bold))
        subtitleLabel.setAlignment(Qt.AlignCenter)
        subtitleLabel.setStyleSheet("color: white;")
        mainLayout.addWidget(subtitleLabel)

        mainLayout.addStretch(1)

        inputLayout = QVBoxLayout()
        inputLayout.setAlignment(Qt.AlignCenter)

        loginInput = QLineEdit()
        loginInput.setPlaceholderText("Логин")
        loginInput.setFixedHeight(60)
        loginInput.setFixedWidth(self.width() // 2)
        loginInput.setStyleSheet("""
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

        inputLayout.addWidget(loginInput)
        inputLayout.addSpacing(40)
        inputLayout.addWidget(passwordInput)
        inputLayout.addSpacing(40)

        # Кнопка входа
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        loginButton = QPushButton("Войти")
        loginButton.setFixedHeight(40)
        loginButton.setFixedWidth(self.width() // 6)
        loginButton.setStyleSheet("""
            background-color: white;
            color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
        """)
        buttonLayout.addWidget(loginButton)
        loginButton.clicked.connect(self.switch_to_main)

        # Ссылка на регистрацию
        registerLabel = QPushButton("Нет аккаунта? Зарегистрироваться")
        registerLabel.setFont(QFont("Arial", 10))
        registerLabel.setStyleSheet("color: #2D8CFF; background-color: transparent; border: none;")
        registerLabel.clicked.connect(self.switch_to_register)

        inputLayout.addLayout(buttonLayout)
        inputLayout.addSpacing(20)
        inputLayout.addWidget(registerLabel)

        mainLayout.addLayout(inputLayout)
        mainLayout.addStretch(1)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#282B3A"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

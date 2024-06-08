from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class ChangePasswordPage(QWidget):
    def __init__(self, switch_to_account):
        super().__init__()
        self.switch_to_account = switch_to_account
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(200, 100, 200, 0)

        old_password_label = QLabel("Введите старый пароль", self)
        old_password_label.setStyleSheet("color: white; font-size: 18px;")
        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)

        new_password_label = QLabel("Введите новый пароль", self)
        new_password_label.setStyleSheet("color: white; font-size: 18px;")
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)

        confirm_password_label = QLabel("Повторите пароль", self)
        confirm_password_label.setStyleSheet("color: white; font-size: 18px;")
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)

        change_password_button = QPushButton("Изменить пароль")
        change_password_button.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)
        change_password_button.clicked.connect(self.change_password)

        layout.addWidget(old_password_label)
        layout.addWidget(self.old_password_input)
        layout.addSpacing(20)
        layout.addWidget(new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addSpacing(20)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(20)
        layout.addWidget(change_password_button)
        self.setLayout(layout)

    def change_password(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            print("Новые пароли не совпадают")
            return

        # Логика проверки старого пароля и смены на новый

        print("Пароль изменен")
        self.switch_to_account()

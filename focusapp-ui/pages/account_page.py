import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import Qt, QTimer


class AccountPage(QWidget):
    def __init__(self, user_data, switch_to_change_password):
        super().__init__()
        self.user_data = user_data
        self.switch_to_change_password = switch_to_change_password
        self.initUI()
        self.start_data_refresh()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.layout.setContentsMargins(200, 100, 0, 0)

        self.usernameLabel = QLabel(f"Username: {self.user_data['username']}", self)
        self.usernameLabel.setStyleSheet("color: white; font-size: 20px; font-weight: bold; border: none")
        self.layout.addWidget(self.usernameLabel)

        self.subscriptionLayout = QVBoxLayout()
        self.subscriptionLayout.setAlignment(Qt.AlignCenter)

        self.subscriptionLabel = QLabel("Подписка", self)
        self.subscriptionLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        self.subscriptionEndLabel = QLabel(self.get_subscription_text(), self)
        self.subscriptionEndLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        subscriptionBox = QWidget()
        subscriptionBox.setFixedWidth(400)
        subscriptionBox.setLayout(self.subscriptionLayout)
        subscriptionBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        self.subscriptionLayout.addWidget(self.subscriptionLabel)
        self.subscriptionLayout.addWidget(self.subscriptionEndLabel)

        self.registrationLayout = QVBoxLayout()
        self.registrationLayout.setAlignment(Qt.AlignCenter)

        self.registrationLabel = QLabel("Дата регистрации", self)
        self.registrationLabel.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none")
        self.registrationDateLabel = QLabel(self.user_data['registration_date'], self)
        self.registrationDateLabel.setStyleSheet("color: white; font-size: 20px; border: none")

        registrationBox = QWidget()
        registrationBox.setFixedWidth(400)
        registrationBox.setLayout(self.registrationLayout)
        registrationBox.setStyleSheet("border: 2px solid white; border-radius: 15px; padding: 10px;")

        self.registrationLayout.addWidget(self.registrationLabel)
        self.registrationLayout.addWidget(self.registrationDateLabel)

        containerLayout = QVBoxLayout()
        containerLayout.setAlignment(Qt.AlignCenter)
        containerLayout.addWidget(subscriptionBox)
        containerLayout.addSpacing(20)
        containerLayout.addWidget(registrationBox)

        change_password_button = QPushButton("Изменить пароль")
        change_password_button.setStyleSheet("""
            color: white;
            background-color: #282B3A;
            border: 2px solid white;
            border-radius: 10px;
            font-size: 18px;
            padding: 5px;
        """)
        change_password_button.clicked.connect(self.switch_to_change_password)

        containerBox = QWidget()
        containerBox.setLayout(containerLayout)
        containerBox.setStyleSheet("border: none;")

        self.layout.addWidget(containerBox)
        self.layout.addWidget(change_password_button)
        self.setLayout(self.layout)

    def get_subscription_text(self):
        subscription_end = self.user_data.get('subscription_end', None)
        if subscription_end:
            return f"Активна до {subscription_end}"
        return "Нет активной подписки"

    def start_data_refresh(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(5000)  # обновление каждые 5 секунд

    def refresh_data(self):
        response = requests.get(f'http://127.0.0.1:8000/api/users/{self.user_data["id"]}/')
        if response.status_code == 200:
            new_data = response.json()
            self.user_data = new_data
            self.update_ui()

    def update_ui(self):
        self.usernameLabel.setText(f"Username: {self.user_data['username']}")
        self.subscriptionEndLabel.setText(self.get_subscription_text())
        self.registrationDateLabel.setText(self.user_data['registration_date'])


# Пример использования (необходимо заменить switch_to_change_password реальной функцией)
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    user_data = {
        "id": 1,
        "username": "testuser",
        "registration_date": "2023-06-01",
        "subscription_end": "2023-12-31"
    }
    window = AccountPage(user_data, lambda: print("Change password"))
    window.show()
    sys.exit(app.exec_())

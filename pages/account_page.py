from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AccountPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel("Ваш айди - Artem#1\nПодписка активна до 08.01.2023\nДата регистрации: 08.01.2032", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        self.setLayout(layout)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(0, 100, 0, 0)

        label = QLabel("Внимание - скрипт работает только на\nразрешении экрана 1920x1080.\nВ дальнейшем мы добавим другие разрешения", self)
        label.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(label)
        self.setLayout(layout)
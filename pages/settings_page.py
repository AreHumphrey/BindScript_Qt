from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel("Внимание - скрипт работает только на разрешении экрана 1920x1080.\nВ дальнейшем мы добавим другие разрешения", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        self.setLayout(layout)
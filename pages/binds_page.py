from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class BindsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel("Управление биндами", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        self.setLayout(layout)

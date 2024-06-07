from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class BindsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        label = QLabel("Управление биндами", self)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        self.setLayout(layout)

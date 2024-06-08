from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QInputDialog
from PyQt5.QtCore import Qt
from functools import partial

class BindsPage(QWidget):
    def __init__(self, binds_data):
        super().__init__()
        self.binds_data = binds_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)  # Выровнять по верхнему краю и по центру

        for bind_name, bind_key in self.binds_data.items():
            bindLayout = QHBoxLayout()
            bindLayout.setAlignment(Qt.AlignCenter)

            bindLabel = QLabel(bind_name, self)
            bindLabel.setStyleSheet("color: white; font-size: 18px;")
            bindLayout.addWidget(bindLabel)

            bindKey = QLabel(bind_key, self)
            bindKey.setStyleSheet("color: white; font-size: 18px;")
            bindLayout.addWidget(bindKey)

            editButton = QPushButton("-", self)
            editButton.setStyleSheet("""
                color: white;
                background-color: #282B3A;
                border: 2px solid white;
                border-radius: 10px;
                font-size: 18px;
                padding: 5px 15px;
            """)
            editButton.clicked.connect(partial(self.edit_bind, bind_name))
            bindLayout.addWidget(editButton)

            layout.addLayout(bindLayout)
            layout.addSpacing(10)

        self.setLayout(layout)

    def edit_bind(self, bind_name):
        new_key, ok = QInputDialog.getText(self, "Изменить бинд", f"Введите новый бинд для {bind_name}:")
        if ok:
            self.binds_data[bind_name] = new_key
            self.updateUI()

    def updateUI(self):
        for i in reversed(range(self.layout().count())):
            widgetToRemove = self.layout().itemAt(i).widget()
            self.layout().removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        self.initUI()

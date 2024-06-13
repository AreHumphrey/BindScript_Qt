from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import subprocess
import keyboard


class BindsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setContentsMargins(40, 100, 40, 0)

        self.binds = [
            {"name": "Уборная", "script": "./tolchki.py", "key": "", "process": None},
            {"name": "Полы", "script": "./poli.py", "key": "", "process": None},
            {"name": "Бургеры", "script": "./burger.py", "key": "", "process": None},
            {"name": "Мусор", "script": "./musorka.py", "key": "", "process": None}
        ]

        for bind in self.binds:
            bindLayout = QHBoxLayout()
            bindLayout.setAlignment(Qt.AlignCenter)

            bindLabel = QLabel(bind["name"])
            bindLabel.setStyleSheet("color: white; font-size: 24px; padding: 10px; border: none")
            bindInput = QLineEdit(bind["key"])
            bindInput.setFixedSize(120, 70)
            bindInput.setMaxLength(1)  # Ограничить ввод одним символом
            bindInput.setStyleSheet("""
                color: white;
                background-color: #282B3A;
                border: 2px solid white;
                border-radius: 10px;
                font-size: 18px;
                margin-left: 10px;
                text-align: center;
            """)
            bindInput.textChanged.connect(lambda text, b=bind: self.update_bind_key(b, text))

            container = QWidget()
            containerLayout = QHBoxLayout(container)
            containerLayout.addWidget(bindLabel)
            containerLayout.addStretch()
            containerLayout.addWidget(bindInput)
            container.setStyleSheet("border: 2px solid white; border-radius: 15px; margin-bottom: 20px;")

            layout.addWidget(container)

        self.setLayout(layout)
        self.setup_global_hotkeys()

    def update_bind_key(self, bind, key):
        bind["key"] = key
        self.setup_global_hotkeys()

    def setup_global_hotkeys(self):
        keyboard.unhook_all()  # Удалить все ранее установленные горячие клавиши
        for bind in self.binds:
            if bind["key"]:
                keyboard.add_hotkey(bind["key"], lambda b=bind: self.toggle_script(b))

    def toggle_script(self, bind):
        if bind["process"] is None or bind["process"].poll() is not None:
            try:
                bind["process"] = subprocess.Popen(["python", bind["script"]])
            except Exception as e:
                print(f"Error running script {bind['script']}: {e}")
        else:
            try:
                bind["process"].terminate()
                bind["process"] = None
            except Exception as e:
                print(f"Error stopping script {bind['script']}: {e}")

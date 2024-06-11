import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from pages.login_window import LoginWindow
from pages.register_window import RegisterWindow
from pages.main_window import MainWindow
from pages.change_password_page import ChangePasswordPage

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.loginWindow = LoginWindow(self.switch_to_register, self.switch_to_main)
        self.registerWindow = RegisterWindow(self.switch_to_login)
        self.mainWindow = MainWindow(self.switch_to_login, self)

        self.addWidget(self.loginWindow)
        self.addWidget(self.registerWindow)
        self.addWidget(self.mainWindow)

        self.setWindowTitle("FocusAPP")
        self.setFixedSize(1280, 720)
        self.setCurrentIndex(0)

    def switch_to_register(self):
        self.setCurrentIndex(1)

    def switch_to_login(self):
        self.setCurrentIndex(0)

    def switch_to_main(self, tokens):
        self.mainWindow.set_tokens(tokens)
        self.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())

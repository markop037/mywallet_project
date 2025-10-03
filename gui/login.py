from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from gui.register import Register
from gui.home import Home
from services.auth_service import AuthService


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.setStyleSheet("background-color: navy; color: white;")
        self.resize(320, 410)
        self.username_entry = None
        self.password_entry = None
        self.login_button = None
        self.error_label = None
        self.signUp_button = None
        self.reg_window = None
        self.home_window = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(QLabel("Welcome to MyWallet", alignment=Qt.AlignmentFlag.AlignVCenter))
        layout.addSpacing(20)

        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_entry)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.check_user)
        layout.addWidget(self.login_button)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")
        layout.addWidget(self.error_label)

        self.signUp_button = QPushButton("Don't have an account? Sign Up")
        self.signUp_button.clicked.connect(self.show_registration_form)
        layout.addWidget(self.signUp_button)

        self.setLayout(layout)

    def check_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if AuthService.check_user_password(username, password):
            self.hide()
            self.home_window = Home(username)
            self.home_window.show()
        else:
            self.error_label.setText("Incorrect username or password.")

    def show_registration_form(self):
        self.reg_window = Register(self)
        self.reg_window.show()

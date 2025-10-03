from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from services.auth_service import AuthService


class Register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setStyleSheet("background-color: navy; color: white;")
        self.resize(320, 540)
        self.firstName_entry = None
        self.lastName_entry = None
        self.username_entry = None
        self.password_entry = None
        self.confirm_password_entry = None
        self.email_entry = None
        self.signUp_button = None
        self.error_label = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("MyWallet"), alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addSpacing(20)

        self.firstName_entry = QLineEdit()
        self.lastName_entry = QLineEdit()
        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.email_entry = QLineEdit()

        fields = [
            ("First Name", self.firstName_entry),
            ("Last Name", self.lastName_entry),
            ("Username*", self.username_entry),
            ("Password*", self.password_entry),
            ("Confirm Password*", self.confirm_password_entry),
            ("Email", self.email_entry),
        ]

        for label, widget in fields:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)

        self.signUp_button = QPushButton("Sign Up")
        self.signUp_button.clicked.connect(self.register_user)
        layout.addWidget(self.signUp_button)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def register_user(self):
        first_name = self.firstName_entry.text()
        last_name = self.lastName_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        email = self.email_entry.text()

        if not username or not password or not confirm_password:
            self.error_label.setText("Fill in all fields marked with *.")
            return

        if password != confirm_password:
            self.error_label.setText("Passwords do not match.")
            return

        success, message = AuthService.register_user(first_name, last_name, username, password, email)

        if success:
            self.error_label.setStyleSheet("color: green;")
            self.error_label.setText(message)

        else:
            self.error_label.setStyleSheet("color: red;")
            self.error_label.setText(message)

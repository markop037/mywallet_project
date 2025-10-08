from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from gui.register import Register
from gui.home import Home
from services.auth_service import AuthService
from models.database import Database
from config import DB_SERVER, DB_NAME


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.resize(360, 280)

        # stylesheet for consistent dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #F5F5F5;
                font-size: 14px;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#signup {
                background: transparent;
                color: #03A9F4;
                text-decoration: none;
                border: none;
            }
            QPushButton#signup:hover {
                color: #29B6F6;              /* svetlija plava */
                text-decoration: underline;  /* underline kad hover */
                cursor: pointer;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#error {
                color: #FF5252;
                font-weight: bold;
            }
        """)

        # Input fields and buttons
        self.username_entry = None
        self.password_entry = None
        self.login_button = None
        self.error_label = None
        self.signUp_button = None
        self.reg_window = None
        self.home_window = None

        # Initialize database and auth service
        self.database = Database(DB_SERVER, DB_NAME)
        self.session = self.database.get_session()
        self.auth_service = AuthService(self.session)

        # Setup UI
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()  # Main vertical layout
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        # Title label
        title_label = QLabel("Welcome to MyWallet", alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("title")
        layout.addWidget(title_label)

        # Username input
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter username")

        # Password input
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setPlaceholderText("Enter password")

        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_entry)

        # Login button
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.check_user)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.login_button)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        layout.addWidget(self.error_label)

        # Sign up button
        self.signUp_button = QPushButton("Don't have an account? Sign Up")
        self.signUp_button.setObjectName("signup")
        self.signUp_button.clicked.connect(self.show_registration_form)
        self.signUp_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.signUp_button)

        # Set layout
        self.setLayout(layout)

        # Check credentials and open home if valid

    def check_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if self.auth_service.check_user_password(username, password):
            self.hide()
            self.home_window = Home(username)
            self.home_window.show()
        else:
            self.error_label.setText("Incorrect username or password.")

        # Open registration window

    def show_registration_form(self):
        self.reg_window = Register()
        self.reg_window.show()
        self.hide()

        # Show a message under input fields

    def show_message(self, msg: str, color="green"):
        self.error_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.error_label.setText(msg)

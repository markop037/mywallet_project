import re

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from services.auth_service import AuthService
from models.database import Database
from config import DB_SERVER, DB_NAME


class Register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")  # Set window title
        self.resize(380, 400)  # Set window size

        # Set stylesheet for the widget
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
            QPushButton#login {
                background: transparent;
                color: #03A9F4;
                text-decoration: none;
                border: none;
            }
            QPushButton#login:hover {
                color: #29B6F6;
                text-decoration: underline;
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

        # Initialize input fields and buttons
        self.firstName_entry = None
        self.lastName_entry = None
        self.username_entry = None
        self.password_entry = None
        self.confirm_password_entry = None
        self.email_entry = None
        self.signUp_button = None
        self.error_label = None
        self.login_window = None
        self.login_button = None

        # Initialize database and authentication service
        self.database = Database(DB_SERVER, DB_NAME)  # Connect to database
        self.session = self.database.get_session()  # Get session
        self.auth_service = AuthService(self.session)  # Auth service instance

        # Setup the UI elements
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()  # Create vertical layout
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align items to top
        layout.setSpacing(12)  # Set spacing between widgets

        # Title label
        title_label = QLabel("Create your account", alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("title")
        layout.addWidget(title_label)

        # Input fields
        self.firstName_entry = QLineEdit()
        self.firstName_entry.setPlaceholderText("First Name")

        self.lastName_entry = QLineEdit()
        self.lastName_entry.setPlaceholderText("Last Name")

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Username*")

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input
        self.password_entry.setPlaceholderText("Password*")

        self.confirm_password_entry = QLineEdit()
        self.confirm_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_entry.setPlaceholderText("Confirm Password*")

        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")

        fields = [
            self.firstName_entry,
            self.lastName_entry,
            self.username_entry,
            self.password_entry,
            self.confirm_password_entry,
            self.email_entry,
        ]

        # Add input fields to layout
        for widget in fields:
            layout.addWidget(widget)

        # Sign Up button
        self.signUp_button = QPushButton("Sign Up")
        self.signUp_button.clicked.connect(self.register_user)  # Connect to registration method
        self.signUp_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.signUp_button)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        layout.addWidget(self.error_label)

        # Button to go to login form
        self.login_button = QPushButton("Already have an account? Log In")
        self.login_button.setObjectName("login")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.show_login_form)
        layout.addWidget(self.login_button)

        # Set the layout for the widget
        self.setLayout(layout)

    def register_user(self):
        # Get values from input fields
        first_name = self.firstName_entry.text()
        last_name = self.lastName_entry.text()
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        email = self.email_entry.text()

        # Check if all fields are filled
        if not all([first_name, last_name, username, password, confirm_password, email]):
            self.error_label.setText("Please fill in all fields.")
            return

        # Validate password strength
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if not re.match(password_pattern, password):
            self.error_label.setText(
                "Password must be at least 8 characters long\n"
                "Include a number\n"
                "Include an uppercase letter\n"
                "Include a special character"
            )
            return

        # Validate email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            self.error_label.setText("Please enter a valid email address")
            return

        # Check if passwords match
        if password != confirm_password:
            self.error_label.setText("Passwords do not match.")
            return

        # Register user using AuthService
        success, message = self.auth_service.register_user(first_name, last_name, username, password, email)

        if success:
            # Show success message in green
            self.error_label.setStyleSheet("color: green; font-weight: bold;")
            self.error_label.setText(message)

            # Open login window
            from gui.login import Login
            self.login_window = Login()
            self.login_window.show_message("Registration successful! Please log in.", "green")
            self.login_window.show()
            self.close()
        else:
            # Show error message in red
            self.error_label.setStyleSheet("color: red; font-weight: bold;")
            self.error_label.setText(message)

    def show_login_form(self):
        # Open the login window
        from gui.login import Login
        self.login_window = Login()
        self.login_window.show()
        self.close()

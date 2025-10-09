from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTextEdit, QListWidget)
from services.auth_service import AuthService
from services.finance_service import FinanceService
from models.finance import IncomeCategory, ExpenseCategory
from PySide6.QtCore import Qt
from models.database import Database
from config import DB_SERVER, DB_NAME
from gui.chart import ChartDialog


class Home(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("My Wallet")
        self.resize(480, 500)

        # stylesheet for consistent dark theme
        self.setStyleSheet("""
                    QWidget {
                        background-color: #2E2E2E;
                        color: #F5F5F5;
                        font-size: 14px;
                        font-family: Segoe UI, Arial, sans-serif;
                    }
                    QLineEdit, QTextEdit, QListWidget {
                        background-color: #3C3C3C;
                        border: 1px solid #555;
                        border-radius: 6px;
                        padding: 6px;
                        color: white;
                    }
                    QLineEdit:focus, QTextEdit:focus, QListWidget:focus {
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
                    QLabel#title {
                        font-size: 18px;
                        font-weight: bold;
                        color: #ffffff;
                    }
                    QLabel#subtitle {
                        font-size: 14px;
                        color: #B0BEC5;
                    }
                    QLabel#error {
                        color: #FF5252;
                        font-weight: bold;
                    }
                    QLabel#balance {
                        font-size: 16px;
                        font-weight: bold;
                        color: #03DAC6;
                    }
                """)

        # Initialize database and services
        self.database = Database(DB_SERVER, DB_NAME)
        self.session = self.database.get_session()
        self.auth_service = AuthService(self.session)
        self.finance_service = FinanceService(self.session)

        # Get user info
        self.user = self.auth_service.check_user(username)

        # Define UI elements (initialized later)
        self.balance_amount_label = None
        self.incomes_button = None
        self.expenses_button = None
        self.amount_entry = None
        self.description_text = None
        self.add_income_button = None
        self.add_expense_button = None
        self.error_label = None
        self.income_list = None
        self.expense_list = None

        # Build the interface
        self.init_ui()

    def init_ui(self):
        # Initialize all UI components and layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        # Title and welcome section
        title_label = QLabel(f"Welcome, {self.user.FirstName}")
        title_label.setObjectName("title")
        layout.addWidget(title_label)

        subtitle_label = QLabel("Current account balance")
        subtitle_label.setObjectName("subtitle")
        layout.addWidget(subtitle_label)

        # Display current balance
        self.balance_amount_label = QLabel(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
        self.balance_amount_label.setObjectName("balance")
        layout.addWidget(self.balance_amount_label)

        # Buttons for income and expense summaries
        h_layout = QHBoxLayout()
        self.incomes_button = QPushButton("See incomes")
        self.incomes_button.clicked.connect(self.get_incomes_summary)
        self.incomes_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.expenses_button = QPushButton("See expenses")
        self.expenses_button.clicked.connect(self.get_expenses_summary)
        self.expenses_button.setCursor(Qt.CursorShape.PointingHandCursor)

        h_layout.addWidget(self.incomes_button)
        h_layout.addWidget(self.expenses_button)
        layout.addLayout(h_layout)

        # Input fields for adding transactions
        self.amount_entry = QLineEdit()
        self.amount_entry.setPlaceholderText("Amount*")

        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Description")

        layout.addWidget(self.amount_entry)
        layout.addWidget(self.description_text)

        # Category lists for income and expenses
        h_cat_layout = QHBoxLayout()
        self.income_list = QListWidget()
        self.expense_list = QListWidget()

        self.load_categories()  # Load categories from database

        self.income_list.itemSelectionChanged.connect(self.on_income_selection_changed)
        self.expense_list.itemSelectionChanged.connect(self.on_expense_selection_changed)

        h_cat_layout.addWidget(self.income_list)
        h_cat_layout.addWidget(self.expense_list)
        layout.addLayout(h_cat_layout)

        # Buttons for adding income and expense
        self.add_income_button = QPushButton("Add income")
        self.add_income_button.clicked.connect(self.add_income)
        self.add_income_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_expense_button = QPushButton("Add expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.add_expense_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.add_income_button)
        layout.addWidget(self.add_expense_button)

        # Error message label
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def load_categories(self):
        # Load income and expense categories from the database
        income_categories = self.session.query(IncomeCategory).all()
        expense_categories = self.session.query(ExpenseCategory).all()

        self.income_list.clear()
        self.expense_list.clear()

        for cat in income_categories:
            self.income_list.addItem(f"{cat.CategoryID}: {cat.CategoryName}")

        for cat in expense_categories:
            self.expense_list.addItem(f"{cat.CategoryID}: {cat.CategoryName}")

    def get_incomes_summary(self):
        # Display a pie chart with income distribution
        summary = self.finance_service.get_income_summary(user_id=self.user.UserID)

        # Each item: (category, amount)
        categories = [item[1] for item in summary]
        amounts = [item[0] for item in summary]
        total_amount = sum(amounts)

        dialog = ChartDialog(categories, amounts, "Incomes Summary", total_amount)
        dialog.exec()

    def get_expenses_summary(self):
        # Display a pie chart with expense distribution
        summary = self.finance_service.get_expense_summary(user_id=self.user.UserID)
        categories = [item[1] for item in summary]
        amounts = [item[0] for item in summary]
        total_amount = sum(amounts)

        dialog = ChartDialog(categories, amounts, "Expenses Summary", total_amount)
        dialog.exec()

    def add_income(self):
        # Add a new income entry for the selected category
        if self.expense_list.selectedItems():
            self.error_label.setText("Cannot add income while an expense category is selected.")
            return

        selected_items = self.income_list.selectedItems()
        if selected_items and self.amount_entry.text():
            try:
                amount = float(self.amount_entry.text())
            except ValueError:
                self.error_label.setText("Amount must be a number.")
                return
            if amount <= 0:
                self.error_label.setText("Amount must be greater than 0.")
                return

            # Extract category ID from the selected item
            selected_text = selected_items[0].text()
            category_id = int(selected_text.split(":")[0])

            # Save income to database
            self.finance_service.add_income(
                self.user.UserID,
                category_id,
                float(self.amount_entry.text()),
                self.description_text.toPlainText()
            )

            # Update balance label
            self.balance_amount_label.setText(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
            self.error_label.setStyleSheet("color: green; font-weight: bold;")
            self.error_label.setText("Income added successfully!")

            # Reset inputs for new entry
            self.amount_entry.clear()
            self.description_text.clear()
            self.income_list.clearSelection()
        else:
            self.error_label.setStyleSheet("color: red; font-weight: bold;")
            self.error_label.setText("Fill in all fields marked with *.")

    def add_expense(self):
        # Add a new expense entry for the selected category
        if self.income_list.selectedItems():
            self.error_label.setText("Cannot add expense while an income category is selected.")
            return

        selected_items = self.expense_list.selectedItems()
        if selected_items and self.amount_entry.text():
            try:
                amount = float(self.amount_entry.text())
            except ValueError:
                self.error_label.setText("Amount must be a number.")
                return
            if amount <= 0:
                self.error_label.setText("Amount must be greater than 0.")
                return

            # Prevent spending more than available balance
            current_balance = self.finance_service.calculate_net_balance(self.user.UserID)
            if current_balance < amount:
                self.error_label.setText("Cannot add expense. Balance cannot go below $0.")
                return

            # Extract category ID from the selected item
            selected_text = selected_items[0].text()
            category_id = int(selected_text.split(":")[0])

            # Save expense to database
            self.finance_service.add_expense(
                self.user.UserID,
                category_id,
                float(self.amount_entry.text()),
                self.description_text.toPlainText()
            )

            # Update balance label
            self.balance_amount_label.setText(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
            self.error_label.setStyleSheet("color: green; font-weight: bold;")
            self.error_label.setText("Expense added successfully!")

            # Reset inputs for new entry
            self.amount_entry.clear()
            self.description_text.clear()
            self.expense_list.clearSelection()
        else:
            self.error_label.setStyleSheet("color: red; font-weight: bold;")
            self.error_label.setText("Fill in all fields marked with *.")

    def on_income_selection_changed(self):
        # Unselect expense category when income is selected
        if self.income_list.selectedItems():
            self.expense_list.clearSelection()
            self.error_label.setText("")

    def on_expense_selection_changed(self):
        # Unselect income category when expense is selected
        if self.expense_list.selectedItems():
            self.income_list.clearSelection()
            self.error_label.setText("")

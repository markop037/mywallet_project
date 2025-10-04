from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QTextEdit, QListWidget, QMessageBox)
from services.auth_service import AuthService
from services.finance_service import FinanceService
from models.finance import Income, Expense
from PySide6.QtCore import Qt
from models.database import Database
from config import DB_SERVER, DB_NAME


class Home(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("My Wallet")
        self.resize(480, 500)

        # Modern tamni stil (isti kao Login/Register)
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

        self.database = Database(DB_SERVER, DB_NAME)
        self.session = self.database.get_session()
        self.auth_service = AuthService(self.session)
        self.finance_service = FinanceService(self.session)

        self.user = self.auth_service.check_user(username)

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
        self.categories_income_dic = {}
        self.categories_expense_dic = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)

        # Naslov i dobrodošlica
        title_label = QLabel(f"Welcome, {self.user.FirstName}")
        title_label.setObjectName("title")
        layout.addWidget(title_label)

        subtitle_label = QLabel("Current account balance")
        subtitle_label.setObjectName("subtitle")
        layout.addWidget(subtitle_label)

        self.balance_amount_label = QLabel(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
        self.balance_amount_label.setObjectName("balance")
        layout.addWidget(self.balance_amount_label)

        # Dugmići za pregled prihoda i troškova
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

        # Polja za unos
        self.amount_entry = QLineEdit()
        self.amount_entry.setPlaceholderText("Amount*")

        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Description")

        layout.addWidget(self.amount_entry)
        layout.addWidget(self.description_text)

        # Kategorije
        self.categories_income_dic = {1: "Salary", 2: "Passive income", 3: "Other income"}
        self.categories_expense_dic = {
            4: "Rent", 5: "Transport", 6: "Food and drink",
            7: "Health", 8: "Clothes", 9: "Other expenses"
        }

        h_cat_layout = QHBoxLayout()
        self.income_list = QListWidget()
        self.income_list.addItems(list(map(str, self.categories_income_dic.values())))

        self.expense_list = QListWidget()
        self.expense_list.addItems(list(map(str, self.categories_expense_dic.values())))

        h_cat_layout.addWidget(self.income_list)
        h_cat_layout.addWidget(self.expense_list)
        layout.addLayout(h_cat_layout)

        # Dugmići za dodavanje prihoda i rashoda
        self.add_income_button = QPushButton("Add income")
        self.add_income_button.clicked.connect(self.add_income)
        self.add_income_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_expense_button = QPushButton("Add expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.add_expense_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.add_income_button)
        layout.addWidget(self.add_expense_button)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def get_incomes_summary(self):
        summary = self.finance_service.get_summary(model=Income, user_id=self.user.UserID)
        QMessageBox.information(self, "Incomes Summary", str(summary))

    def get_expenses_summary(self):
        summary = self.finance_service.get_summary(model=Expense, user_id=self.user.UserID)
        QMessageBox.information(self, "Expenses Summary", str(summary))

    def add_income(self):
        selected_items = self.income_list.selectedItems()
        if selected_items and self.amount_entry.text():
            category_name = selected_items[0].text()
            category_id = next((k for k, v in self.categories_income_dic.items() if v == category_name), None)
            FinanceService.add_income(self.user.UserID, category_id, float(self.amount_entry.text()),
                                      self.description_text.toPlainText())
            self.balance_amount_label.setText(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
            self.error_label.setText("")
        else:
            self.error_label.setText("Fill in all fields marked with *.")

    def add_expense(self):
        selected_items = self.expense_list.selectedItems()
        if selected_items and self.amount_entry.text():
            category_name = selected_items[0].text()
            category_id = next((k for k, v in self.categories_expense_dic.items() if v == category_name), None)
            FinanceService.add_expense(self.user.UserID, category_id,
                                       float(self.amount_entry.text()), self.description_text.toPlainText())
            self.balance_amount_label.setText(f"$ {self.finance_service.calculate_net_balance(self.user.UserID)}")
            self.error_label.setText("")
        else:
            self.error_label.setText("Fill in all fields marked with *.")

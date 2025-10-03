from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QTextEdit, QListWidget, QMessageBox)
from services.auth_service import AuthService
from services.finance_service import FinanceService
from models.finance import Income, Expense
from PySide6.QtCore import Qt


class Home(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("My Wallet")
        self.setStyleSheet("background-color: navy; color: white;")
        self.resize(400, 860)

        self.user = AuthService.check_user(username)

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
        layout.addWidget(QLabel(f"Welcome {self.user.FirstName}", alignment=Qt.AlignmentFlag.AlignVCenter))
        layout.addSpacing(10)

        layout.addWidget(QLabel("Current account balance"))
        self.balance_amount_label = QLabel(f"${FinanceService.calculate_net_balance(self.user.UserID)}")
        layout.addWidget(self.balance_amount_label)

        h_layout = QHBoxLayout()
        self.incomes_button = QPushButton("See incomes")
        self.incomes_button.clicked.connect(self.get_incomes_summary)
        self.expenses_button = QPushButton("See expenses")
        self.expenses_button.clicked.connect(self.get_expenses_summary)
        h_layout.addWidget(self.incomes_button)
        h_layout.addWidget(self.expenses_button)
        layout.addLayout(h_layout)

        self.amount_entry = QLineEdit()
        self.description_text = QTextEdit()
        layout.addWidget(QLabel("Amount*"))
        layout.addWidget(self.amount_entry)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description_text)

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

        self.add_income_button = QPushButton("Add income")
        self.add_income_button.clicked.connect(self.add_income)
        self.add_expense_button = QPushButton("Add expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        layout.addWidget(self.add_income_button)
        layout.addWidget(self.add_expense_button)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def get_incomes_summary(self):
        summary = FinanceService.get_summary(model=Income, user_id=self.user.UserID)
        QMessageBox.information(self, "Incomes Summary", str(summary))

    def get_expenses_summary(self):
        summary = FinanceService.get_summary(model=Expense, user_id=self.user.UserID)
        QMessageBox.information(self, "Expenses Summary", str(summary))

    def add_income(self):
        selected_items = self.income_list.selectedItems()
        if selected_items and self.amount_entry.text():
            category_name = selected_items[0].text()
            category_id = next((k for k, v in self.categories_income_dic.items() if v == category_name), None)
            FinanceService.add_income(self.user.UserID, category_id, float(self.amount_entry.text()),
                                      self.description_text.toPlainText())
            self.balance_amount_label.setText(f"{FinanceService.calculate_net_balance(self.user.UserID)}")
            self.error_label.setText("")
        else:
            self.error_label.setText("Fill in all fields marked with *.")

    def add_expense(self):
        selected_items = self.expense_list.selectedItems()
        if selected_items and self.amount_entry.text():
            category_name = selected_items[0].text()
            category_id = next((k for k, v in self.categories_expense_dic.items() if v == category_name), None)
            FinanceService.add_expense(self.user.UserID, category_id, float(self.amount_entry.text()),
                                        self.description_text.toPlainText())
            self.balance_amount_label.setText(f"$ {FinanceService.calculate_net_balance(self.user.UserID)}")
            self.error_label.setText("")
        else:
            self.error_label.setText("Fill in all fields marked with *.")

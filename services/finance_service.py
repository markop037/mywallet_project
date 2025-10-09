from models.finance import Income, Expense, IncomeCategory, ExpenseCategory
from sqlalchemy import func


class FinanceService:
    def __init__(self, db_session):
        self.session = db_session

    def calculate_net_balance(self, user_id):
        # Sum all income amounts for the given user; return 0 if no records exist
        total_income = (
            self.session.query(func.sum(Income.Amount))
            .filter(Income.UserID == user_id)
            .scalar()
            or 0
        )

        # Sum all expense amounts for the given user; return 0 if no records exist
        total_expense = (
            self.session.query(func.sum(Expense.Amount))
            .filter(Expense.UserID == user_id)
            .scalar()
            or 0
        )

        balance = round(total_income - total_expense, 3)

        # Return the net balance
        return balance

    # Get total income per category for a specific user
    def get_income_summary(self, user_id):
        return (
            self.session.query(
                func.sum(Income.Amount).label("TotalIncome"),
                IncomeCategory.CategoryName
            )
            .join(IncomeCategory, Income.CategoryID == IncomeCategory.CategoryID)
            .filter(Income.UserID == user_id)
            .group_by(IncomeCategory.CategoryID, IncomeCategory.CategoryName)
            .all()  # Return all results
        )

    # Get total expenses per category for a specific user
    def get_expense_summary(self, user_id):
        return (
            self.session.query(
                func.sum(Expense.Amount).label("TotalExpense"),
                ExpenseCategory.CategoryName
            )
            .join(ExpenseCategory, Expense.CategoryID == ExpenseCategory.CategoryID)
            .filter(Expense.UserID == user_id)
            .group_by(ExpenseCategory.CategoryID, ExpenseCategory.CategoryName)
            .all()  # Return all results
        )

    # Add a new income record for a user
    def add_income(self, user_id, category_id, amount, description=""):
        new_income = Income(
            Amount=amount,
            UserID=user_id,
            CategoryID=category_id,
            Description=description
        )
        self.session.add(new_income)
        self.session.commit()

    # Add a new expense record for a user
    def add_expense(self, user_id, category_id, amount, description=""):
        new_expense = Expense(
            Amount=amount,
            UserID=user_id,
            CategoryID=category_id,
            Description=description
        )
        self.session.add(new_expense)
        self.session.commit()

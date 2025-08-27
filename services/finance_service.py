from models.finance import Income, Expense
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
            self.session.query(func.sum(Expense.UserID))
            .filter(Expense.UserID == user_id)
            .scalar()
            or 0
        )

        # Return the net balance
        return total_income - total_expense

    def get_summary(self, model, user_id):
        # Get a summary of incomes or expenses grouped by category for a user
        return (
            self.session.query(func.sum(model.Amount), model.category.CategoryName)
            .join(model.category)
            .filter(model.UserID == user_id)
            .group_by(model.CategoryID, model.category.CategoryName)
            .all()
        )

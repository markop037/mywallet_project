from models.finance import Income, Expense, IncomeCategory, ExpenseCategory
from sqlalchemy import func


class FinanceService:
    def __init__(self, db_session):
        self.session = db_session

    def calculate_net_balance(self, user_id):
        total_income = (
            self.session.query(func.sum(Income.Amount))
            .filter(Income.UserID == user_id)
            .scalar()
            or 0
        )
        total_expense = (
            self.session.query(func.sum(Expense.Amount))
            .filter(Expense.UserID == user_id)
            .scalar()
            or 0
        )
        return round(total_income - total_expense, 3)

    def get_income_summary(self, user_id):
        return (
            self.session.query(
                func.sum(Income.Amount).label("TotalIncome"),
                IncomeCategory.CategoryName,
            )
            .join(IncomeCategory, Income.CategoryID == IncomeCategory.CategoryID)
            .filter(Income.UserID == user_id)
            .group_by(IncomeCategory.CategoryID, IncomeCategory.CategoryName)
            .all()
        )

    def get_expense_summary(self, user_id):
        return (
            self.session.query(
                func.sum(Expense.Amount).label("TotalExpense"),
                ExpenseCategory.CategoryName,
            )
            .join(ExpenseCategory, Expense.CategoryID == ExpenseCategory.CategoryID)
            .filter(Expense.UserID == user_id)
            .group_by(ExpenseCategory.CategoryID, ExpenseCategory.CategoryName)
            .all()
        )

    def get_recent_transactions(self, user_id, limit=20):
        incomes = (
            self.session.query(Income, IncomeCategory.CategoryName)
            .outerjoin(IncomeCategory)
            .filter(Income.UserID == user_id)
            .order_by(Income.created_at.desc())
            .limit(limit)
            .all()
        )
        expenses = (
            self.session.query(Expense, ExpenseCategory.CategoryName)
            .outerjoin(ExpenseCategory)
            .filter(Expense.UserID == user_id)
            .order_by(Expense.created_at.desc())
            .limit(limit)
            .all()
        )
        rows = []
        for inc, cat_name in incomes:
            rows.append({
                "id": inc.IncomeID,
                "type": "Income",
                "category": cat_name,
                "amount": inc.Amount,
                "description": inc.Description or "",
                "created_at": inc.created_at,
            })
        for exp, cat_name in expenses:
            rows.append({
                "id": exp.ExpenseID,
                "type": "Expense",
                "category": cat_name,
                "amount": exp.Amount,
                "description": exp.Description or "",
                "created_at": exp.created_at,
            })
        rows.sort(key=lambda r: r["created_at"], reverse=True)
        return rows[:limit]

    def add_income(self, user_id, category_id, amount, description=""):
        new_income = Income(
            Amount=amount, UserID=user_id,
            CategoryID=category_id, Description=description,
        )
        self.session.add(new_income)
        self.session.commit()
        self.session.refresh(new_income)
        return new_income

    def add_expense(self, user_id, category_id, amount, description=""):
        new_expense = Expense(
            Amount=amount, UserID=user_id,
            CategoryID=category_id, Description=description,
        )
        self.session.add(new_expense)
        self.session.commit()
        self.session.refresh(new_expense)
        return new_expense

    def delete_transaction(self, tx_type: str, tx_id: int):
        if tx_type == "Income":
            record = self.session.get(Income, tx_id)
        else:
            record = self.session.get(Expense, tx_id)
        if record:
            self.session.delete(record)
            self.session.commit()

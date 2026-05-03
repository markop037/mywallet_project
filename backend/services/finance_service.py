from datetime import datetime, timedelta
from typing import Optional

from models.finance import Income, Expense, IncomeCategory, ExpenseCategory
from sqlalchemy import func


def _period_start(period: Optional[str]) -> Optional[datetime]:
    """Return the UTC start datetime for the given period label, or None for all-time."""
    now = datetime.utcnow()
    if period == "day":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "week":
        start = now - timedelta(days=now.weekday())
        return start.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "month":
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if period == "year":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return None


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

    def get_income_summary(self, user_id, period: Optional[str] = None):
        since = _period_start(period)
        q = (
            self.session.query(
                func.sum(Income.Amount).label("TotalIncome"),
                IncomeCategory.CategoryName,
            )
            .join(IncomeCategory, Income.CategoryID == IncomeCategory.CategoryID)
            .filter(Income.UserID == user_id)
        )
        if since:
            q = q.filter(Income.created_at >= since)
        return q.group_by(IncomeCategory.CategoryID, IncomeCategory.CategoryName).all()

    def get_expense_summary(self, user_id, period: Optional[str] = None):
        since = _period_start(period)
        q = (
            self.session.query(
                func.sum(Expense.Amount).label("TotalExpense"),
                ExpenseCategory.CategoryName,
            )
            .join(ExpenseCategory, Expense.CategoryID == ExpenseCategory.CategoryID)
            .filter(Expense.UserID == user_id)
        )
        if since:
            q = q.filter(Expense.created_at >= since)
        return q.group_by(ExpenseCategory.CategoryID, ExpenseCategory.CategoryName).all()

    def get_recent_transactions(self, user_id, limit=100, period: Optional[str] = None):
        since = _period_start(period)
        income_q = (
            self.session.query(Income, IncomeCategory.CategoryName)
            .outerjoin(IncomeCategory)
            .filter(Income.UserID == user_id)
        )
        expense_q = (
            self.session.query(Expense, ExpenseCategory.CategoryName)
            .outerjoin(ExpenseCategory)
            .filter(Expense.UserID == user_id)
        )
        if since:
            income_q = income_q.filter(Income.created_at >= since)
            expense_q = expense_q.filter(Expense.created_at >= since)
        incomes = income_q.order_by(Income.created_at.desc()).limit(limit).all()
        expenses = expense_q.order_by(Expense.created_at.desc()).limit(limit).all()
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

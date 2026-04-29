from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_current_user, get_db
from models.finance import ExpenseCategory, IncomeCategory
from models.user import User
from schemas.finance import (
    BalanceResponse,
    CategoryOut,
    ExpenseCreate,
    IncomeCreate,
    SummaryItem,
    TransactionOut,
)
from services.finance_service import FinanceService

router = APIRouter()


@router.get("/categories/incomes", response_model=List[CategoryOut])
def list_income_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cats = db.query(IncomeCategory).order_by(IncomeCategory.CategoryID).all()
    return [CategoryOut(id=c.CategoryID, name=c.CategoryName) for c in cats]


@router.get("/categories/expenses", response_model=List[CategoryOut])
def list_expense_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cats = db.query(ExpenseCategory).order_by(ExpenseCategory.CategoryID).all()
    return [CategoryOut(id=c.CategoryID, name=c.CategoryName) for c in cats]


@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    return BalanceResponse(balance=svc.calculate_net_balance(current_user.UserID))


@router.get("/transactions", response_model=List[TransactionOut])
def list_transactions(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    return svc.get_recent_transactions(current_user.UserID, limit=limit)


@router.post("/incomes", status_code=status.HTTP_201_CREATED)
def add_income(
    data: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    record = svc.add_income(
        user_id=current_user.UserID,
        category_id=data.category_id,
        amount=data.amount,
        description=data.description,
    )
    return {"message": "Income added", "id": record.IncomeID}


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    current_balance = svc.calculate_net_balance(current_user.UserID)
    if current_balance < data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Balance cannot go below $0.",
        )
    record = svc.add_expense(
        user_id=current_user.UserID,
        category_id=data.category_id,
        amount=data.amount,
        description=data.description,
    )
    return {"message": "Expense added", "id": record.ExpenseID}


@router.delete("/transactions/{tx_type}/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    tx_type: str,
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if tx_type not in ("Income", "Expense"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction type.")
    svc = FinanceService(db)
    svc.delete_transaction(tx_type, tx_id)


@router.get("/summary/incomes", response_model=List[SummaryItem])
def income_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    return [
        SummaryItem(category=cat, total=total)
        for total, cat in svc.get_income_summary(current_user.UserID)
    ]


@router.get("/summary/expenses", response_model=List[SummaryItem])
def expense_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = FinanceService(db)
    return [
        SummaryItem(category=cat, total=total)
        for total, cat in svc.get_expense_summary(current_user.UserID)
    ]

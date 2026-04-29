from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TransactionBase(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = ""


class IncomeCreate(TransactionBase):
    pass


class ExpenseCreate(TransactionBase):
    pass


class TransactionOut(BaseModel):
    id: int
    type: str
    category: Optional[str] = ""
    amount: float
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SummaryItem(BaseModel):
    category: str
    total: float


class BalanceResponse(BaseModel):
    balance: float


class CategoryOut(BaseModel):
    id: int
    name: str

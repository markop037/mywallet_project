from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class IncomeCategory(Base):
    __tablename__ = "IncomeCategories"
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), nullable=False)
    incomes = relationship("Income", back_populates="category")


class ExpenseCategory(Base):
    __tablename__ = "ExpenseCategories"
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), nullable=False)
    expenses = relationship("Expense", back_populates="category")


class Income(Base):
    __tablename__ = "Incomes"
    IncomeID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("IncomeCategories.CategoryID"))
    Description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    category = relationship("IncomeCategory", back_populates="incomes")


class Expense(Base):
    __tablename__ = "Expenses"
    ExpenseID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("ExpenseCategories.CategoryID"))
    Description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    category = relationship("ExpenseCategory", back_populates="expenses")

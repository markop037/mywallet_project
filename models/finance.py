from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base


# IncomeCategory Table ORM Model
class IncomeCategory(Base):
    __tablename__ = "IncomeCategories"
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), nullable=False)

    # One-to-Many:
    incomes = relationship("Income", back_populates="category")


# ExpenseCategory Table ORM Model
class ExpenseCategory(Base):
    __tablename__ = "ExpenseCategories"

    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), nullable=False)

    # One-to-Many: povezuje Expense -> ExpenseCategory
    expenses = relationship("Expense", back_populates="category")


# Income Table ORM Model
class Income(Base):
    __tablename__ = "Incomes"

    IncomeID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("IncomeCategories.CategoryID"))
    Description = Column(String(255), nullable=True)

    user = relationship("User")
    category = relationship("IncomeCategory", back_populates="incomes")


# Expense Table ORM Model
class Expense(Base):
    __tablename__ = "Expenses"

    ExpenseID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("ExpenseCategories.CategoryID"))
    Description = Column(String(255), nullable=True)

    user = relationship("User")
    category = relationship("ExpenseCategory", back_populates="expenses")

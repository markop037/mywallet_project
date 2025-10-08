from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base


# IncomeCategory Table ORM Model
class IncomeCategory(Base):
    __tablename__ = "IncomeCategories"  # Table name in the database
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    CategoryName = Column(String(50), nullable=False)  # Category name column

    # One-to-Many relationship: connects Income -> IncomeCategory
    incomes = relationship("Income", back_populates="category")


# ExpenseCategory Table ORM Model
class ExpenseCategory(Base):
    __tablename__ = "ExpenseCategories"  # Table name
    CategoryID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    CategoryName = Column(String(50), nullable=False)  # Category name column

    # One-to-Many relationship: connects Expense -> ExpenseCategory
    expenses = relationship("Expense", back_populates="category")


# Income Table ORM Model
class Income(Base):
    __tablename__ = "Incomes"  # Table name

    IncomeID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    Amount = Column(Float, nullable=False)  # Income amount
    UserID = Column(Integer, ForeignKey("Users.UserID"))  # Foreign key to User
    CategoryID = Column(Integer, ForeignKey("IncomeCategories.CategoryID"))  # Foreign key to IncomeCategory
    Description = Column(String(255), nullable=True)  # Optional description

    user = relationship("User")  # Relationship to User table
    category = relationship("IncomeCategory", back_populates="incomes")  # Relationship to category


# Expense Table ORM Model
class Expense(Base):
    __tablename__ = "Expenses"  # Table name

    ExpenseID = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    Amount = Column(Float, nullable=False)  # Expense amount
    UserID = Column(Integer, ForeignKey("Users.UserID"))  # Foreign key to User
    CategoryID = Column(Integer, ForeignKey("ExpenseCategories.CategoryID"))  # Foreign key to ExpenseCategory
    Description = Column(String(255), nullable=True)  # Optional description

    user = relationship("User")  # Relationship to User table
    category = relationship("ExpenseCategory", back_populates="expenses")  # Relationship to category

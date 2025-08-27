from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


# Category Table ORM Model
class Category(Base):
    __tablename__ = "Categories"

    CategoryID = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50), nullable=False)


# Income Table ORM Model
class Income(Base):
    __tablename__ = "Incomes"

    IncomeID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("Categories.CategoryID"))

    user = relationship("User")
    category = relationship("Category")


# Expense Table ORM Model
class Expense(Base):
    __tablename__ = "Expenses"

    ExpenseID = Column(Integer, primary_key=True, autoincrement=True)
    Amount = Column(Float, nullable=False)
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    CategoryID = Column(Integer, ForeignKey("Categories.CategoryID"))

    user = relationship("User")
    category = relationship("Category")

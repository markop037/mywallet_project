import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models.finance import Income, IncomeCategory, Expense, ExpenseCategory
from models.user import User
from models.database import Base


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_user(session):
    user = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko123",
        Password="marko00pera",
        Email="marko02@gmail.com",
    )
    session.add(user)
    session.commit()

    result = session.query(User).first()
    assert result is not None
    assert result.Username == "marko123"
    assert result.Email == "marko02@gmail.com"


def test_unique_username_and_email(session):
    user1 = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko_p",
        Password="StrongPass123",
        Email="marko.peric@gmail.com",
    )

    user2 = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko_p",
        Password="AnotherPass456",
        Email="marko.peric@gmail.com"
    )

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    assert session.query(User).count() == 1


def test_add_income_and_expense(session):
    user = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko123",
        Password="marko00pera",
        Email="marko02@gmail.com",
    )
    income_cat = IncomeCategory(CategoryName="Freelance")
    expense_cat = ExpenseCategory(CategoryName="Transport")

    session.add_all([user, income_cat, expense_cat])
    session.commit()

    income = Income(Amount=1500.0, UserID=user.UserID, CategoryID=income_cat.CategoryID, Description="Project")
    expense = Expense(Amount=100.0, UserID=user.UserID, CategoryID=expense_cat.CategoryID, Description="Bus Ticket")

    session.add_all([income, expense])
    session.commit()

    fetched_income = session.query(Income).first()
    fetched_expense = session.query(Expense).first()

    assert fetched_income.Amount == 1500.0
    assert fetched_expense.Amount == 100.0
    assert fetched_income.category.CategoryName == "Freelance"
    assert fetched_expense.category.CategoryName == "Transport"
    assert fetched_income.user.Username == "marko123"



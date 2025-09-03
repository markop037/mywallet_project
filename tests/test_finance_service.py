import pytest
from models.database import Database, Base
from models.user import User
from models.finance import Category, Income, Expense
from services.finance_service import FinanceService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def db_session():
    db = Database(server="", database="", driver="")
    db.engine = create_engine('sqlite:///:memory:')
    db.session = sessionmaker(bind=db.engine)

    Base.metadata.create_all(db.engine)

    session = db.get_session()
    yield session
    session.close()
    Base.metadata.drop_all(db.engine)


@pytest.fixture()
def test_user(db_session):
    user = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko123",
        Password="securepass",
        Email="marko@example.com"
    )

    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture()
def finance_service(db_session):
    return FinanceService(db_session)


@pytest.fixture()
def categories(db_session):
    income_cat = Category(CategoryName="Salary")
    expense_cat = Category(CategoryName="Food")
    db_session.add_all([income_cat, expense_cat])
    db_session.commit()
    return {"income": income_cat, "expense": expense_cat}


def test_calculate_net_balance(finance_service, db_session, test_user, categories):
    user = test_user
    income_cat = categories["income"]
    expense_cat = categories["expense"]

    # Add incomes
    income1 = Income(Amount=1000, user=user, category=income_cat)
    income2 = Income(Amount=500, user=user, category=income_cat)
    db_session.add_all([income1, income2])

    # Add expenses
    expense1 = Expense(Amount=200, user=user, category=expense_cat)
    expense2 = Expense(Amount=100, user=user, category=expense_cat)
    db_session.add_all([expense1, expense2])
    db_session.commit()

    net_balance = finance_service.calculate_net_balance(user.UserID)
    assert net_balance == (1000 + 500) - (200 + 100)


def test_calculate_net_balance_no_records(finance_service, test_user):
    net_balance = finance_service.calculate_net_balance(test_user.UserID)
    assert net_balance == 0


def test_get_summary_incomes(finance_service, db_session, test_user, categories):
    user = test_user
    income_cat = categories["income"]

    db_session.add_all([
        Income(Amount=1000, user=user, category=income_cat),
        Income(Amount=500, user=user, category=income_cat)
    ])
    db_session.commit()

    summary = finance_service.get_summary(Income, user.UserID)
    assert len(summary) == 1
    total_amount, category_name = summary[0]
    assert total_amount == 1500
    assert category_name == "Salary"


def test_get_summary_expenses(finance_service, db_session, test_user, categories):
    user = test_user
    expense_cat = categories["expense"]

    db_session.add_all([
        Expense(Amount=200, user=user, category=expense_cat),
        Expense(Amount=100, user=user, category=expense_cat)
    ])
    db_session.commit()

    summary = finance_service.get_summary(Expense, user.UserID)
    assert len(summary) == 1
    total_amount, category_name = summary[0]
    assert total_amount == 300
    assert category_name == "Food"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.finance import IncomeCategory, ExpenseCategory, Income, Expense
from services.finance_service import FinanceService
from models.database import Base
from models.user import User


@pytest.fixture
def session():
    # Create a temporary in-memory database session for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def finance_service(session):
    # Provide a FinanceService instance with pre-created categories
    income_cat = IncomeCategory(CategoryName="Freelance")
    expense_cat = ExpenseCategory(CategoryName="Transport")
    session.add_all([income_cat, expense_cat])
    session.commit()
    return FinanceService(session)


@pytest.fixture
def user(session):
    # Create a test user in the database
    user = User(
        FirstName="Marko",
        LastName="Peric",
        Username="marko123",
        Password="marko00pera",
        Email="marko02@gmail.com",
    )
    session.add(user)
    session.commit()


def test_add_income(finance_service, session, user):
    # Test that adding an income record works correctly
    finance_service.add_income(user_id=1, category_id=1, amount=500.0, description="Project A")

    income = session.query(Income).filter_by(UserID=1).first()

    assert income is not None
    assert income.Amount == 500.0
    assert income.Description == "Project A"


def test_add_expense(finance_service, session, user):
    # Test that adding an expense record works correctly
    finance_service.add_expense(user_id=1, category_id=1, amount=200.0, description="Taxi")

    expense = session.query(Expense).filter_by(UserID=1).first()
    assert expense is not None
    assert expense.Amount == 200.0
    assert expense.Description == "Taxi"


def test_calculate_net_balance(finance_service):
    # Test that net balance is calculated correctly (income - expense)
    finance_service.add_income(user_id=1, category_id=1, amount=1000)
    finance_service.add_expense(user_id=1, category_id=1, amount=300)

    balance = finance_service.calculate_net_balance(user_id=1)
    assert balance == 700  # 1000 - 300


def test_calculate_net_balance_empty(finance_service):
    # Test that net balance returns 0 when there are no records
    balance = finance_service.calculate_net_balance(user_id=1)
    assert balance == 0  # No records should return 0


def test_get_income_summary(finance_service):
    # Test that income summary returns correct totals per category
    finance_service.add_income(user_id=1, category_id=1, amount=100)
    finance_service.add_income(user_id=1, category_id=1, amount=150)

    summary = finance_service.get_income_summary(user_id=1)
    assert len(summary) == 1
    total_income, category_name = summary[0]
    assert total_income == 250
    assert category_name == "Freelance"


def test_get_expense_summary(finance_service):
    # Test that expense summary returns correct totals per category
    finance_service.add_expense(user_id=1, category_id=1, amount=60)
    finance_service.add_expense(user_id=1, category_id=1, amount=40)

    summary = finance_service.get_expense_summary(user_id=1)
    assert len(summary) == 1
    total_expense, category_name = summary[0]
    assert total_expense == 100
    assert category_name == "Transport"

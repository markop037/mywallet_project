import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.database import Database, Base
from models.user import User
from models.finance import Category, Income, Expense


class TestTable(Base):
    __tablename__ = "test_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


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


def test_database_connection_and_create_table(db_session):
    db_session.add(TestTable(id=1, name="Test"))
    db_session.commit()
    result = db_session.query(TestTable).filter_by(name="Test").first()
    assert result is not None
    assert result.name == "Test"


def test_user_model_insert(db_session, test_user):
    result = db_session.query(User).filter_by(Username="marko123").first()

    assert result is not None
    assert result.FirstName == "Marko"
    assert result.Email == "marko@example.com"


def test_income_insert(db_session, test_user):
    category = Category(CategoryName="Freelance")
    db_session.add(category)
    db_session.commit()

    income = Income(Amount=1500.0, user=test_user, category=category)
    db_session.add(income)
    db_session.commit()

    result = db_session.query(Income).first()
    assert result is not None
    assert result.user.Username == "marko123"
    assert result.category.CategoryName == "Freelance"
    assert result.Amount == 1500.0


def test_expense_insert(db_session, test_user):
    category = Category(CategoryName="Food")
    db_session.add(category)
    db_session.commit()

    expense = Expense(Amount=200, user=test_user, category=category)
    db_session.add(expense)
    db_session.commit()

    result = db_session.query(Expense).first()
    assert result.user.Username == "marko123"
    assert result.category.CategoryName == "Food"
    assert result.Amount == 200.0

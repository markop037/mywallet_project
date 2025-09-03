import pytest
from models.database import Database, Base
from models.user import User
from services.auth_service import AuthService
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
def auth_service(db_session):
    return AuthService(db_session)


def test_register_user_success(db_session, auth_service):
    success, msg = auth_service.register_user(
        first_name="Marko",
        last_name="Peric",
        username="marko123",
        password="securepass",
        email="marko@example.com"
    )

    assert success is True
    assert msg == "User successfully registered"

    user = db_session.query(User).filter_by(Username="marko123").first()
    assert user is not None
    assert user.FirstName == "Marko"
    assert user.Email == "marko@example.com"


def test_register_user_duplicate(auth_service):
    # Register first user
    auth_service.register_user(
        "Marko", "Peric", "marko123", "mypassword123", "marko@example.com"
    )

    # Try duplicate with same username
    success, msg = auth_service.register_user(
        "John", "Smith", "marko123", "newpassword", "john@example.com"
    )
    assert success is False
    assert msg == "Username or email already exists"

    # Try duplicate with same email
    success, msg = auth_service.register_user(
        "Emily", "Johnson", "emily123", "anotherpassword", "marko@example.com"
    )
    assert success is False
    assert msg == "Username or email already exists"


def test_check_user(auth_service):
    auth_service.register_user("Alice", "Brown", "alice", "mypassword", "alice@example.com")

    user = auth_service.check_user("alice")
    assert user is not None
    assert user.Username == "alice"

    missing_user = auth_service.check_user("bob")
    assert missing_user is None


def test_check_user_password(auth_service):
    auth_service.register_user("Bob", "Taylor", "bob", "letmein", "bob@example.com")

    # Correct password
    assert auth_service.check_user_password("bob", "letmein") is True

    # Wrong password
    assert auth_service.check_user_password("bob", "wrongpass") is False

    # User does not exist
    assert auth_service.check_user_password("nonexistent", "letmein") is False

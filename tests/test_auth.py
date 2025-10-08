import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from services.auth_service import AuthService
from models.user import User
from werkzeug.security import check_password_hash


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
def auth_service(session):
    # Provide an AuthService instance for testing
    return AuthService(session)


def test_register_user_success(auth_service, session):
    # Test that a user can be successfully registered
    success, message = auth_service.register_user(
        "Marko", "Peric", "marko_p",
        "StrongPass123", "marko.peric@gmail.com"
    )

    assert success is True
    assert message == "User successfully registered"

    user = session.query(User).filter_by(Username="marko_p").first()
    assert user is not None
    assert check_password_hash(user.Password, "StrongPass123")


def test_register_user_duplicate(auth_service, session):
    # Test that registering a user with existing username/email fails
    auth_service.register_user(
        "Marko", "Peric", "marko_p",
        "StrongPass123", "marko.peric@gmail.com"
    )

    success, message = auth_service.register_user(
        "Marko", "Peric", "marko_p",
        "StrongPass123", "marko.peric@gmail.com"
    )

    assert success is False
    assert message == "Username or email already exists"


def test_check_user_existing(auth_service, session):
    # Test that user exists
    auth_service.register_user(
        "Marko", "Peric", "marko_p",
        "StrongPass123", "marko.peric@gmail.com"
    )

    user = auth_service.check_user("marko_p")

    assert user is not None
    assert user.Username == "marko_p"


def test_check_user_password_correct(auth_service, session):
    # Test that password verification works correctly for a user
    auth_service.register_user(
        "Marko", "Peric", "marko_p",
        "StrongPass123", "marko.peric@gmail.com"
    )

    assert auth_service.check_user_password("marko_p", "StrongPass123") is True

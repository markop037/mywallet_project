import uuid

from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash


class AuthService:
    def __init__(self, db_session):
        self.session = db_session

    def get_or_create_oauth_user(self, email: str, full_name: str = "") -> User:
        user = self.session.query(User).filter_by(Email=email).first()
        if not user:
            parts = full_name.strip().split(" ", 1) if full_name.strip() else []
            first = parts[0] if parts else "Google"
            last = parts[1] if len(parts) > 1 else "User"
            username = f"user_{uuid.uuid4().hex[:8]}"
            user = User(
                FirstName=first,
                LastName=last,
                Username=username,
                Password=generate_password_hash(uuid.uuid4().hex),
                Email=email,
            )
            self.session.add(user)
            self.session.commit()
        return user

    def register_user(self, first_name, last_name, username, password, email):
        existing_user = self.session.query(User).filter(
            (User.Username == username) | (User.Email == email)
        ).first()

        if existing_user:
            return False, "Username or email already exists"

        hashed_password = generate_password_hash(password)
        user = User(
            FirstName=first_name,
            LastName=last_name,
            Username=username,
            Password=hashed_password,
            Email=email,
        )
        self.session.add(user)
        self.session.commit()
        return True, "User successfully registered"

    def check_user(self, username):
        return self.session.query(User).filter_by(Username=username).first()

    def check_user_password(self, username, password):
        user = self.check_user(username)
        if user and check_password_hash(user.Password, password):
            return True
        return False

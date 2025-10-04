from models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:
    def __init__(self, db_session):
        self.session = db_session

    def register_user(self, first_name, last_name, username, password, email):
        # Check if username or email already exists
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
            Email=email
        )
        self.session.add(user)
        self.session.commit()
        return True, "User successfully registered"

    def check_user(self, username):
        return self.session.query(User).filter_by(Username=username).first()

    def check_user_password(self, username, password):
        # Check if the user exists and if the password is correct
        user = self.check_user(username)
        if user and check_password_hash(user.Password, password):
            return True
        return False
    
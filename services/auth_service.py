from models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:
    def __init__(self, db_session):
        self.session = db_session

    def register_user(self, first_name, last_name, username, password, email):
        # Hash the plain-text password before saving it to the database
        hashed_password = generate_password_hash(password)

        # Create a new User object
        user = User(
            FirstName=first_name,
            LastName=last_name,
            Username=username,
            Password=hashed_password,
            Email=email
        )
        try:
            # Add the user to the session and commit to save it in the DB
            self.session.add(user)
            self.session.commit()
            return True, "User successfully registered"
        except IntegrityError:
            # Roll back the session if there is a uniqueness violation
            self.session.rollback()
            return False, "Username already exists"

    def check_user(self, username):
        # Query the database for a user with the given username
        return self.session.query(User).filter_by(Username=username).first()

    def check_user_password(self, username, password):
        # Check if the user exists and if the password is correct
        user = self.check_user(username)
        if user and check_password_hash(user.Password, password):
            return True
        return False
    
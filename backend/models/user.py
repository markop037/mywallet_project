from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Username = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(username={self.Username}, email={self.Email})>"

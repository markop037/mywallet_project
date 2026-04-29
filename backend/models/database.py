import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./mywallet_dev.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables. Called once at application startup."""
    import models.user  # noqa: F401
    import models.finance  # noqa: F401
    Base.metadata.create_all(engine)

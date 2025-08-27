from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a base class for declarative ORM models
Base = declarative_base()


class Database:
    def __init__(self, server, database, driver="ODBC Driver 17 for SQL Server"):
        # Build the connection string for SQL Server using pyodbc
        conn_str = (
            f"mssql+pyodbc://@{server}/{database}"
            f"?driver={driver.replace(' ', '+')}"
            "&trusted_connection=yes"
        )

        self.engine = create_engine(conn_str, echo=False)
        self.session = sessionmaker(bind=self.engine)

    def create_table(self):
        # Create all tables defined in ORM models
        Base.metadata.create_all(self.engine)

    def get_session(self):
        # Return a new session instance for performing DB operations
        return self.session()

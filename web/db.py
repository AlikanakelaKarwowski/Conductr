# Import SQLAlchemy's create_engine function
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

connection_url = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(
    connection_url, 
    echo=True,
    pool_size=5,          # Number of connections to keep open
    max_overflow=10,      # Extra connections when pool is full
    pool_pre_ping=True    # Test connections before using
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        if session.dirty or session.new or session.deleted:
            session.commit()
    except Exception as e:
        session.rollback()
        raise  
    finally:
        session.close()

# Test the connection
if __name__ == "__main__":
    try:
        connection = engine.connect()
        print("Connected to PostgreSQL database successfully!")
        connection.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
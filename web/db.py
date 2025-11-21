# Import SQLAlchemy's create_engine function
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

connection_url = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)


# Create a connection string
engine = create_engine(connection_url)

# Test the connection
try:
    connection = engine.connect()
    print("Connected to PostgreSQL database successfully!")
    connection.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
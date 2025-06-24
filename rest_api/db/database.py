from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import POSTGRES_CONN

DATABASE_URL = (
    f"postgresql://{POSTGRES_CONN['user']}:{POSTGRES_CONN['password']}"
    f"@{POSTGRES_CONN['host']}:{POSTGRES_CONN['port']}/{POSTGRES_CONN['dbname']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from typing import Optional
from sqlmodel import SQLModel, Session, create_engine
from os import getenv
from dotenv import load_dotenv

class DatabaseConnection:
    """Database connection manager using SQLModel"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_engine'):
            load_dotenv()
            
            # Get database connection parameters from environment variables
            DB_USER = getenv("DB_USER", "default_user")
            DB_PASSWORD = getenv("DB_PASSWORD", "default_password")
            DB_HOST = getenv("DB_HOST", "localhost")
            DB_PORT = getenv("DB_PORT", "5432")
            DB_NAME = getenv("DB_NAME", "default_db")
            
            # Create database URL
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            
            # Create engine with connection pool
            self._engine = create_engine(
                DATABASE_URL,
                echo=False,
                pool_size=5,
                max_overflow=10
            )
    
    def create_db_and_tables(self):
        """Create all tables defined in SQLModel classes"""
        SQLModel.metadata.create_all(self._engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return Session(self._engine)
    
    def get_engine(self):
        """Get the database engine"""
        return self._engine

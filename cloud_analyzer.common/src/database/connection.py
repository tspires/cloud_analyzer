"""Database connection management."""

from typing import Optional, Dict, Any
from contextlib import contextmanager
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

from .models import Base

logger = logging.getLogger(__name__)


def get_database_url(config: Dict[str, Any]) -> str:
    """Construct database URL from configuration."""
    from urllib.parse import quote_plus
    
    db_config = config.get('database', {})
    
    host = db_config.get('host', 'localhost')
    port = db_config.get('port', 5432)
    database = db_config.get('database', 'azure_metrics')
    username = db_config.get('username', 'postgres')
    password = db_config.get('password', '')
    
    # URL encode the password to handle special characters
    encoded_password = quote_plus(str(password)) if password else ''
    encoded_username = quote_plus(str(username))
    
    if encoded_password:
        return f"postgresql://{encoded_username}:{encoded_password}@{host}:{port}/{database}"
    else:
        return f"postgresql://{encoded_username}@{host}:{port}/{database}"


class DatabaseConnection:
    """Database connection manager with connection pooling."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize database connection."""
        self.config = config
        self.database_url = get_database_url(config)
        self.engine = None
        self.session_factory = None
        self._initialized = False
    
    def initialize(self):
        """Initialize database connection and session factory."""
        if self._initialized:
            return
        
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=self.config.get('database', {}).get('echo', False)
            )
            
            # Create session factory
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False
            )
            
            self._initialized = True
            logger.info("Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise
    
    def create_tables(self):
        """Create database tables."""
        if not self._initialized:
            self.initialize()
        
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test database connection."""
        if not self._initialized:
            try:
                self.initialize()
            except Exception:
                return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup."""
        if not self._initialized:
            self.initialize()
        
        session = self.session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_sync_session(self) -> Session:
        """Get synchronous database session."""
        if not self._initialized:
            self.initialize()
        
        return self.session_factory()
    
    def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Any:
        """Execute a raw SQL query."""
        with self.get_session() as session:
            try:
                result = session.execute(text(query), params or {})
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Query execution failed: {e}")
                raise
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./math_solver.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ProblemHistory(Base):
    """Database model for storing solved problem history"""
    __tablename__ = "problem_history"

    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String, nullable=False)
    problem_type = Column(String, nullable=False)
    final_answer = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)  # JSON string of steps
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

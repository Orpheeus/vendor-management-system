from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta hacia la DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./ironclad_database.db"

# Motor
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
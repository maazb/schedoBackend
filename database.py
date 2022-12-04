from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://aeraihnyukhoes:8e0fec45d02c6ba3657cce762f246831f63a4b973a5f4aae1f7fabc5953e8bf8@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d4vuq2n6tktj7g"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

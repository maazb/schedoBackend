from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://ujqgbicrpujvjb:6b728f654913b4d1f87cfdd69f3dfd651f5115f5e8eac48dd35f683047443186@ec2-54-147-36-107.compute-1.amazonaws.com:5432/dda25ri2qi0kt6"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

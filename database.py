from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://fthrqpxtobqyvs:a86b813357cc38683e6c0e5b749dc4fb8073d007e4c2a898d470a285ae0acc48@ec2-44-206-197-71.compute-1.amazonaws.com:5432/d71g440ad85thb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

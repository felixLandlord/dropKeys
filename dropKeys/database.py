from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dropKeys.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Import models to ensure they are registered with Base
from . import models

# Create tables
Base.metadata.create_all(bind=engine)



def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
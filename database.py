from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    #Base.metadata.create_all(bind=engine)
    try:
        yield Base.metadata.create_all(bind=engine)
    finally:
        Base.metadata.create_all(bind=engine).close()

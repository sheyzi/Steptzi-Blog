from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config.settings import settings

engine = create_engine(settings.DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal(bind=engine, autocommit=False, autoflush=False) as session:
        try:
            yield session
        finally:
            session.close()


Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)

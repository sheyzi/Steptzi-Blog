from sqlmodel import create_engine, Session
from sqlmodel import SQLModel


from config.settings import settings

engine = create_engine(settings.DB_URI)


def get_db():
    with Session(bind=engine, autocommit=False, autoflush=False) as session:
        try:
            yield session
        finally:
            session.close()


def init_db():

    SQLModel.metadata.create_all(engine)

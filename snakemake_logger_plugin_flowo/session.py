from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

try:
    engine = create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_pre_ping=True,
        echo=settings.SQL_ECHO,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception:
    SessionLocal = None


def get_db():
    db = None
    try:
        if SessionLocal is None:
            raise Exception("SessionLocal is not initialized.")
        db = SessionLocal()
        yield db
    except Exception:
        return
    finally:
        if db is not None:
            db.close()

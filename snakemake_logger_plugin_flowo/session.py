from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
import sys

try:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        echo=settings.SQL_ECHO,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except:
    print(
        "\033[91m[ERROR] Flowo failed to connect to PostgreSQL.\033[0m", file=sys.stderr
    )
    print(
        "\033[93mPlease check your configuration (e.g., host, port, user, password).\033[0m",
        file=sys.stderr,
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

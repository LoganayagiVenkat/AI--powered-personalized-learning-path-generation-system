import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learning_path.db")

# Load environment configuration
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "learning_path_db")

# Construct MySQL URI
MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
SQLITE_URL = "sqlite:///backend/database/learning_path.db"

engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    global engine, SessionLocal
    if engine is not None and SessionLocal is not None:
        return engine

    mysql_connected = False
    if os.getenv("FORCE_SQLITE", "false").lower() != "true":
        try:
            logger.info(f"Attempting connection to MySQL at {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}...")
            test_engine = create_engine(
                MYSQL_URL,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 2}
            )
            with test_engine.connect() as conn:
                logger.info("Successfully connected to MySQL server!")
            engine = test_engine
            mysql_connected = True
        except Exception as e:
            logger.warning(f"MySQL connection unavailable ({e}). Automatically using SQLite database fallback for instant operation.")

    if not mysql_connected:
        db_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(db_dir, exist_ok=True)
        sqlite_path = os.path.join(db_dir, "learning_path.db")
        engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
        logger.info(f"Connected to local SQLite database at {sqlite_path}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

def get_engine():
    global engine
    if engine is None:
        init_db()
    return engine

def get_db():
    global SessionLocal
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


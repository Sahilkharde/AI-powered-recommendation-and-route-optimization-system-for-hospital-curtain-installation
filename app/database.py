from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import DATABASE_URL, IS_SNOWFLAKE

connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    if IS_SNOWFLAKE:
        return
    Base.metadata.create_all(bind=engine)


def get_snowflake_session():
    """Return a Snowpark Session for Cortex AI calls.

    Only works when connected to Snowflake. Returns None otherwise.
    """
    if not IS_SNOWFLAKE:
        return None
    try:
        from snowflake.snowpark import Session as SnowparkSession

        from app.config import (
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_DATABASE,
            SNOWFLAKE_PASSWORD,
            SNOWFLAKE_ROLE,
            SNOWFLAKE_SCHEMA,
            SNOWFLAKE_USER,
            SNOWFLAKE_WAREHOUSE,
        )

        return SnowparkSession.builder.configs({
            "account": SNOWFLAKE_ACCOUNT,
            "user": SNOWFLAKE_USER,
            "password": SNOWFLAKE_PASSWORD,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "role": SNOWFLAKE_ROLE,
        }).create()
    except Exception:
        return None

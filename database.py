from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://stringhusniddin:ReBQigD0L4sM@ep-holy-feather-14762857.eu-central-1.aws.neon.tech/neondb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getdb():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
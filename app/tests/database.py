from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import engine, SessionLocal, get_db
from app.main import app
from app import schemas , models
from app.config import settings
import pytest
from alembic import command

#SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi'

SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()       
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
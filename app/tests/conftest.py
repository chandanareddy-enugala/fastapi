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
from app.ouath2 import create_access_token


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
    
@pytest.fixture()
def test_user2(client):
    user_data = {"email":"abc2345@gmail.com",
                 "password":"password123"}
    res = client.post("/users/create", json = user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    print('in test_user',new_user)
    return new_user
    
    
@pytest.fixture()
def test_user(client):
    user_data = {"email":"abc@gmail.com",
                 "password":"password123"}
    res = client.post("/users/create", json = user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    print('in test_user',new_user)
    return new_user
 
@pytest.fixture
def token(test_user):
    token = create_access_token({"user_id": test_user['id']})
    return token

@pytest.fixture
def authorized_client(client, token):
    client.headers={
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
         {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(postdata):
        return models.Post(**postdata)
    
    post_map = map(create_post_model,posts_data)
    print('before list',post_map)
    posts = list(post_map)
   
    print('after converting to list',posts)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    print('posts..............',posts)
    return posts
    
    


import pytest
from app import schemas
from app.config import settings
from jose import jwt


   
def test_root(client, session):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200
    

def test_create_user(client,session):
    res = client.post('/users/create',json = {'email':'monika2@gmail.com','password':'password12345'})
    print("response_json",res.json())
    new_user = schemas.GetResponse(**res.json())
    print("new_user",new_user)
    assert res.json().get('email') == 'monika2@gmail.com'
    assert res.status_code == 201
    
    
def test_login_user(client,test_user):
    res = client.post('/login',data = {'username':test_user['email'],'password':test_user['password']})
    print('in login',res.json())
    login_res = schemas.Token(**res.json())
    print('au....................',login_res)
    payload = jwt.decode(login_res.access_token, settings.secret_key , algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
    
    

    
def test_create_post(client, test_user):
    # Step 1: Log in the test user
    login_res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    assert login_res.status_code == 200  # Or whatever your successful login status code is
    login_res_data = login_res.json()
    print('Login response:', login_res_data)
    # Extract the token from the login response. This assumes your login response includes a token.
    # Adjust the key based on your actual response structure (e.g., 'access_token', 'token', etc.)
    token = login_res_data['access_token']
    # Step 2: Use the token to authenticate the create post request
    # Include the token in the request headers. The exact header name and format depend on your auth setup,
    # but it's often something like 'Authorization': 'Bearer <token>'
    headers = {"Authorization": f"Bearer {token}"}
    print('headers',headers)
    post_data = {'title': "chandu", 'content': 'hello'}
    create_post_res = client.post('/posts/', json=post_data, headers=headers)
    assert create_post_res.status_code == 201  # Assuming 201 is the status code for successful post creation
    print("Create post response:", create_post_res.json())
    # Step 3: Verify the response
    # Assuming your response model includes the 'title' field
    assert create_post_res.json().get('title') == 'chandu'

    # Optionally, you can deserialize the response to your PostResponse schema
    # This step is useful if you want to work with the response data as a Python object
    # and also serves as a validation that the response matches your schema
    new_post = schemas.PostResponse(**create_post_res.json())
    print("Deserialized new post:", new_post)
    assert new_post.title == 'chandu'  # Example of asserting with the deserialized object

# def test_incorrect_username(test_user, client):
#     res = client.post('/login', data = {"username": 'abc1@gmail.com' ,"password": test_user["password"]})
#     assert res.status_code == 403
#     print('res',res.json())
#     assert res.json().get('detail') == 'invalid credentials'
    

# def test_incorrect_password(test_user, client):
#     res = client.post('/login', data = {"username": test_user['email'] ,"password": "password123456"})
#     assert res.status_code == 403
#     print('res',res.json())
#     assert res.json().get('detail') == 'invaild and not found'

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422),
    ('abc@gmail.com', 'password123',200)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    print('res',res.json())

    assert res.status_code == status_code
    
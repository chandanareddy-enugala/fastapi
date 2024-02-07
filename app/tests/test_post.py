from typing import List
from app import schemas

# def test_get_all_posts(authorized_client,test_posts):
#     res = authorized_client.get('/posts/')
#     assert len(res.json()) == len(test_posts)
#     print(res.json())
#     assert res.status_code == 200

from pydantic import ValidationError

# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get('/posts/')
#     assert res.status_code == 200
#     response_posts = res.json()
#     print('r................',response_posts)
#     assert len(response_posts) == len(test_posts)
#     # Iterate over each post response and validate with PostOut schema
#     for post_data in response_posts:
#         try:
#             # This will raise a ValidationError if the data is not valid for PostOut schema
#             post_out = schemas.PostOut(**post_data)
#             print('po======================',post_out)
#         except ValidationError as e:
#             # If there is a validation error, print the error and fail the test
#             print(e.json())
#             assert False, f"Post data does not match PostOut schema: {e.json()}"
            
# def test_unathorized_user_get_all_posts(client, test_posts):
#     res = client.get('/posts/')
#     assert res.status_code == 401

# def test_unathorized_user_get_one_posts(client, test_posts):
#     res = client.get(f'/posts/{test_posts[1].id}')
#     assert res.status_code == 401 
    
# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f'/posts/{test_posts[1].id}')
#     print(res.json())
#     post = schemas.PostOut(**res.json())
#     print(post)
#     assert post.Post.id == test_posts[1].id
#     assert post.Post.content == test_posts[1].content

# def test_unauthorized_user_delete_post(client,test_user,test_posts):
#     res = client.delete(f'/posts/delete/posts/{test_posts[0].id}')
#     assert res.status_code == 401

# def test_unauthorized_user_delete_post(client,test_posts):
#     res = client.delete(f'/posts/delete/posts/{test_posts[0].id}')
#     assert res.status_code == 401

# def test_authorized_user_delete_post(authorized_client,test_posts):
#     res = authorized_client.delete(f'/posts/delete/posts/{test_posts[0].id}')
#     assert res.status_code == 204
    
# def test_delete_post_non_exist(authorized_client,test_posts):
#     res = authorized_client.delete(f'/posts/delete/posts/647')
#     assert res.status_code == 404
    
# def test_delete_other_user_post(authorized_client,test_user,test_posts):
#     res = authorized_client.delete(f'/posts/delete/posts/{test_posts[3].id}')
#     assert res.status_code == 403
    
def test_update_post(authorized_client,test_user,test_posts):
    data = {
        "title":"updated title",
        "content":"vbvhfb",
        "id":test_posts[2].id
    }
    res = authorized_client.put(f'/posts/update/{test_posts[2].id}', json = data)
    print('res==============',res,type(res))
    print('\n\n')
    print('restext==============',res.text,type(res.text))
    update_post = schemas.PostResponse(**res.json())
    
    print('update_post==============',update_post,type(update_post),'res.json()=============',res.json())
    assert res.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']
    
"""def test_unauthorized_client_update(client,test_user,test_posts):
    res = client.put(f'/posts/update/{test_posts[2].id}')
    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client,test_posts):
    data = {
        "title":"updated title",
        "content":"vbvhfb",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f'posts/update/5677',json = data)
    assert res.status_code == 404
    """
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class GetResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode =True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating :Optional[int] = None
    

class PostCreate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: GetResponse
    
    class Config:
      orm_mode = True
      

class UserCreate(BaseModel):
     email: EmailStr
     password: str
   
    
     class Config:
        orm_mode =True
           
    
class UserLogin(BaseModel):
    email : EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id:Optional[int]=None
    email: Optional[EmailStr] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    
    
    
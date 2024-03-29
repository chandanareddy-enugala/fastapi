
from fastapi import FastAPI
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, get_db
from . import utils
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import Settings



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"message":" hi Hello World"}

"""if __name__ == '__main__':
    uvicorn.run(app, reload = True)"""
    
    
    
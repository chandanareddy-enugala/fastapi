
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional,List
from app import ouath2
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user_id: int = Depends(ouath2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) 
    #                values (%s,%s,%s) returning *""",
    #                (post.title,post.content,post.published))
    # #print(post.title_,type(post.title_))
    # new_post = cursor.fetchone()
    # conn.commit()
    #print(**post.dict())
    #new_post=models.Post(title=post.title, content = post.content, published = post.published)
    print("1...............",get_current_user_id.id)
    print("2............",get_current_user_id.email)
    new_post =models.Post(owner_id = get_current_user_id.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/",response_model=List[schemas.PostOut]) #response_model=List[schemas.PostResponse]
#@router.get("/")
def get_posts(db: Session = Depends(get_db),get_current_user_id: int = Depends(ouath2.get_current_user),limit: int = 5, skip: int =0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #filter(models.Post.owner_id == get_current_user_id.id)
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    print(results)
    #cursor.execute("select * from posts")
    #posts = cursor.fetchall()
    #print(posts)
    return results



@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),get_current_user_id: int = Depends(ouath2.get_current_user)):
    # cursor.execute("""select * from posts where id = %s """, (str(id)))
    # post_one = cursor.fetchone()
    #post_one = db.query(models.Post).filter(models.Post.id==id).first()
    post_one = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id )
    post = post_one.first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # if post_one.owner_id != get_current_user_id.id:
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'you are tryin to get somenone')
    return  post


@router.put("/update/{id}",response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db),get_current_user_id: int = Depends(ouath2.get_current_user)):
    # cursor.execute("""update posts set title= %s, content = %s where id = %s returning *""",
    #                (post.title, post.content,str(id)))
    # updated_post = cursor.fetchone()
    # print(updated_post)
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    
    print("post_query",post_query)
    post = post_query.first()
    print("post",post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id} does not exist')
        
    if post.owner_id != get_current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'you are tryin to update someone else post')
        
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    #print(post_query.first())
    return post_query.first()
    #conn.commit()


              
@router.delete("/delete/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),get_current_user_id: int = Depends(ouath2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""delete from posts where id = %s returning * """,(str(id),))

    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
   
    post = deleted_post.first()
    print(post)
        
    if post.owner_id != get_current_user_id.id: 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


    


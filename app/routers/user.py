from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from app import models, schemas, utils # or from .. import 
from sqlalchemy.orm import Session 
from app.database import get_db  # from ..database
from typing import Optional,List

router = APIRouter(
    tags=['Users']
)

@router.post("/users/create", status_code=status.HTTP_201_CREATED,response_model=schemas.GetResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password- user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    print("new_user is.......",new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print('after......',new_user)
    return new_user

@router.get("/get/users/",response_model=List[schemas.GetResponse])
def users(db: Session = Depends(get_db)):
    fetched_users = db.query(models.User).all()
    return fetched_users

@router.get("/get/oneuser/{id}",response_model=schemas.GetResponse)
def users(id: int , db: Session = Depends(get_db)):
    fetched_one_user = db.query(models.User).filter(models.User.id == id).first()
    if fetched_one_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this {id} is not found')
    fetched_one_user
    print(fetched_one_user)
    return fetched_one_user


@router.put("/update/user/{id}",response_model=schemas.GetResponse)
def update_user(id: int, update_post:schemas.UserCreate, db: Session = Depends(get_db)):
    _query = db.query(models.User).filter(models.User.id == id)
    # print("i",_query.first())
    # j= _query.first()
    # print('j',j)
    if _query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'this {id} is not found')
    _query.update(update_post.dict(),synchronize_session=False)
    db.commit()
    return _query.first()

@router.delete('/delete/users/{id}',status_code = status.HTTP_204_NO_CONTENT)
def delete_users(id: int,db: Session = Depends(get_db)):
    query_= db.query(models.User).filter(models.User.id==id)
    if query_.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'this {id} is not found')
    query_.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


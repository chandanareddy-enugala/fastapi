from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app import schemas, utils, ouath2
router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model = schemas.Token)       #schemas.UserLogin
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email== user_credentials.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f'invaild and not found')
    
    #create a tokem
    # return token
    access_token = ouath2.create_access_token(data={"user_id": user.id, "user_mail": user.email})
    return {"access_token":access_token, "token_type":"bearer"}
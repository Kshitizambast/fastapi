from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import get_db
from schemas import *
import models
from oauth2 import *
from utils import verify_password

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect Credentials")
    
    #create token
    access_token = create_access_token(data = {"user_id": user.id})


    return {"access_token": access_token, "token_type": "bearer"}

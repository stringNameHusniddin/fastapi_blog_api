from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.hash import password_hash, verify_password
from utils.user_token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

import schemas, models, database

getdb = database.getdb
router = APIRouter(tags=["user"])

@router.get('/user', response_model=list[schemas.ShowUser])
def list_users(db:Session=Depends(getdb)):
    users = db.query(models.User).all()
    return users

@router.get("/user/{id}", response_model=schemas.ShowUser)
def detail_user(id:int, db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

@router.post("/user", response_model=schemas.ShowUser)
def create_user(req:schemas.CreateUser, db:Session=Depends(getdb)):
    new_user = models.User(username=req.username, email=req.email, password=password_hash(req.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete("/user/{id}")
def delete_user(id:int, db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user.delete()

    db.commit()

    return "done"

@router.post("/login")
def login(req:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.username == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if not verify_password(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
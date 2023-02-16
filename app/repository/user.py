from fastapi import status, Depends, HTTPException, APIRouter
import schemas, models, database, hashing
from sqlalchemy.orm import Session


#create user, response will contain Hashed password
def create_user_resp_display_password(request: schemas.User, db:Session):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#create user, response will not have password
def create_user(request: schemas.User, db:Session):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#list users
def get_user_list(db:Session):
    users = db.query(models.User).all()
    return users

#Get all user details
def get_user(id, db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user

#displays all blogs of the user
def get_user_along_with_blogs(id, db:Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user
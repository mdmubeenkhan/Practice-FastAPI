from fastapi import status, Depends, HTTPException, APIRouter
import schemas, models, database, hashing
from sqlalchemy.orm import Session
from typing import List
from repository import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
    )
get_db = database.get_db

#create user, response will contain Hashed password
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    return user.create_user_resp_display_password(request, db)


#create user, response will not have password
@router.post("/user-nopwd-in-resp", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    return user.create_user(request, db)

#list users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_user_list(db:Session=Depends(get_db)):
    return user.get_user_list(db)

#Get all user details
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id, db:Session=Depends(get_db)):
    return user.get_user(id, db)

#displays all blogs of the user
@router.get("/user-blogs/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser_Relationship)
def get_user(id, db:Session=Depends(get_db)):
    return user.get_user_along_with_blogs(id, db)
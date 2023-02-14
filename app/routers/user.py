from fastapi import status, Depends, HTTPException, APIRouter
import schemas, models, database, hashing
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["Users"]
    )
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/user-nopwd-in-resp", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user

#displays all blogs of the user
@router.get("/user-blogs/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser_Relationship)
def get_user(id, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user
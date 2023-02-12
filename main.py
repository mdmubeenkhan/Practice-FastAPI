from fastapi import FastAPI, status, Depends, HTTPException, Response
import schemas, models, database, hashing
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()

models.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.post("/blog-with-user-id", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schemas.Blog_User_Id, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#this displays all field values (id, title, body)
@app.get("/blogs", tags=["Blogs"])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title, body)
@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["Blogs"])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title)
@app.get("/blog-title", response_model=List[schemas.ShowTitle], tags=["Blogs"])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title, body)
@app.get("/blog-body", response_model=List[schemas.ShowBody], tags=["Blogs"])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only particular blog
@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["Blogs"])
def get_particular_blog(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog

#this deletes a particular blog
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    #Response body will not be sent in delete request, no matter what.
    return {"detail": f"Blog with id = {id} is deleted."}    

#this deletes a particular blog
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id, request:schemas.Blog, db:Session=Depends(get_db)):
    print(f"Mubeen = {dict(request)}=.")
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.update(dict(request))
    db.commit()
    return {"detail": f"Blog with id = {id} is updated."}  


#this displays blogs of given user
@app.get("/blog-with-user-detail/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog_Relationship, tags=["Blogs"])
def get_particular_blog(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog


@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/user-nopwd-in-resp", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["Users"])
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["Users"])
def get_user(id, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user

#displays all blogs of the user
@app.get("/user-blogs/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser_Relationship, tags=["Users"])
def get_user(id, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found.")
    return user
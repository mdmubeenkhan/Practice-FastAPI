from fastapi import status, Depends, HTTPException, APIRouter
import schemas, models, database
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(tags=["Blogs"])
get_db = database.get_db



@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.post("/blog-with-user-id", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog_User_Id, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#this displays all field values (id, title, body)
@router.get("/blogs")
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title, body)
@router.get("/blog", response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title)
@router.get("/blog-title", response_model=List[schemas.ShowTitle])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title, body)
@router.get("/blog-body", response_model=List[schemas.ShowBody])
def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only particular blog
@router.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_particular_blog(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog

#this deletes a particular blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    #Response body will not be sent in delete request, no matter what.
    return {"detail": f"Blog with id = {id} is deleted."}    

#this deletes a particular blog
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:Session=Depends(get_db)):
    print(f"Mubeen = {dict(request)}=.")
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.update(dict(request))
    db.commit()
    return {"detail": f"Blog with id = {id} is updated."}  


#this displays blogs of given user
@router.get("/blog-with-user-detail/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog_Relationship)
def get_particular_blog(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog


from fastapi import status, HTTPException
import schemas, models
from sqlalchemy.orm import Session

def create(request: schemas.Blog, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def create_with_user_id(request: schemas.Blog_User_Id, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#this displays all field values (id, title, body)
def get_all_blogs_with_all_details(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

#this displays only (title, body)
def get_all_blogs_with_title_and_body(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


#this displays only (title)
def get_all_blogs_title(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


#this displays only body
def get_all_blog_body(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


#this displays only particular blog
def get_a_particular_blog(id, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog


#this deletes a particular blog
def delete(id, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    #Response body will not be sent in delete request, no matter what.
    return {"detail": f"Blog with id = {id} is deleted."}  


#this updates a particular blog
def update(id, request:schemas.Blog, db:Session):
    print(f"Mubeen = {dict(request)}=.")
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    blog.update(dict(request))
    db.commit()
    return {"detail": f"Blog with id = {id} is updated."}  


#this displays blogs of given user
def get_particular_blog(id, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id = {id} not found.")
    return blog
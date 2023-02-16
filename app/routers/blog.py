from fastapi import status, Depends, APIRouter
import schemas, database
from sqlalchemy.orm import Session
from typing import List
from repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
    )
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session=Depends(get_db)):
    return blog.create(request, db)


@router.post("/blog-with-user-id", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog_User_Id, db:Session=Depends(get_db)):
    return blog.create_with_user_id(request, db)


#this displays all field values (id, title, body)
@router.get("/blogs")
def get_all_blogs(db:Session=Depends(get_db)):
    return blog.get_all_blogs_with_all_details(db)

#this displays only (title, body)
@router.get("/", response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session=Depends(get_db)):
    return blog.get_all_blogs_with_title_and_body(db)

#this displays only (title)
@router.get("/blog-title", response_model=List[schemas.ShowTitle])
def get_all_blogs(db:Session=Depends(get_db)):
    return blog.get_all_blogs_title(db)

#this displays only body
@router.get("/blog-body", response_model=List[schemas.ShowBody])
def get_all_blogs(db:Session=Depends(get_db)):
    return blog.get_all_blog_body(db)

#this displays only particular blog
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_particular_blog(id, db:Session=Depends(get_db)):
    return blog.get_a_particular_blog(id, db)

#this deletes a particular blog
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:Session=Depends(get_db)):
    return blog.delete(id, db)   

#this updates a particular blog
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:Session=Depends(get_db)):
    return blog.update(id, request, db) 


#this displays blogs of given user
@router.get("/blog-with-user-detail/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog_Relationship)
def get_particular_blog(id, db:Session=Depends(get_db)):
    return blog.get_a_particular_blog(id, db)


from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title:str
    body:str


class Blog_User_Id(BaseModel):
    title:str
    body:str
    user_id:int

# this will display only (title and body)
class ShowBlog(Blog):
    class Config():
        orm_mode = True

# this will display only (title)
class ShowTitle(BaseModel):
    title:str
    class Config():
        orm_mode = True

# this will display only (body)
class ShowBody(BaseModel):
    body:str
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

# this will display only (body)
class ShowBlog_Relationship(BaseModel):
    title:str
    body:str

    #creator details
    creator:ShowUser

    class Config():
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str


class ShowUser_Relationship(BaseModel):
    name:str
    email:str

    #populating blogs for given user
    blogs:List[ShowBlog_Relationship] = []

    class Config():
        orm_mode = True
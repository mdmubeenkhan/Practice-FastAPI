from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str

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
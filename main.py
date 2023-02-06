from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

@app.get("/")
def index():
    return {"data":"blog post"}

@app.get("/blog/{id}")
def blogs(id:int):
    return {"data": id}

@app.get("/about")
def about():
    return {"data":"about page."}

@app.get("/blog/{id}/comments")
def comments(id:int):
    return {"data":{id:["comment 1", "comment 2"]}}

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]


@app.post("/create-blog")
def create_blog(request:Blog):
    return {
        "data":f'Blog is created with title as {request.title}'
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
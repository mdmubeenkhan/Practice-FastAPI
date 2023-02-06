from fastapi import FastAPI


app = FastAPI()

@app.post("/blog")
def create(title, body):
    return {"data":f"creating blog with title = {title} and body = {body}"}
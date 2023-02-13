from fastapi import FastAPI
import models, database
from routers import blog, user

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(blog.router)
app.include_router(user.router)



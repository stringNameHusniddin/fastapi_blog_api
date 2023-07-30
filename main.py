from fastapi import FastAPI
from routers import user, blog
import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router=user.router)
app.include_router(router=blog.router)
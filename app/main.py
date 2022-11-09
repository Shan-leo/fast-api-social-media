from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import user, post, auth
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

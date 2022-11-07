import time
import psycopg2
from fastapi import FastAPI, Request, HTTPException, Response, Depends, status
from psycopg2.extras import RealDictCursor
from app import models, schemas, utils
from app.database import engine, get_db
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()

get_db()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Coolipso2022',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
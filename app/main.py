import time
from typing import Optional
import psycopg2
from fastapi import FastAPI, Request, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

app: FastAPI = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


@app.get("/")
async def root():
    arr = [x for x in range(5)]
    return {"message": arr}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"message": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))

    new_post = cursor.fetchone()

    conn.commit()

    return {"message": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} was not found")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s , content = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updated_post}

from random import randrange
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.params import Body
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

app: FastAPI = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"id": 1, "title": "Shan", "content": "Hi guys.. Its a beautiful day"}]


@app.get("/")
async def root():
    arr = [x for x in range(5)]
    return {"message": arr}


@app.get("/posts")
def get_posts():
    return {"message": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"message": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    return {"post_details": f"Here is the post {id}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    return "Updated"

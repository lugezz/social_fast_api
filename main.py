from typing import Optional
from fastapi import FastAPI
# from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Cachulengo"}


@app.get("/posts")
def get_post():
    return {"Data": "This is your posts"}


@app.post("/createposts")
def create_post(new_post: Post):
    # We expect: title: str, body: str

    print(new_post)
    summary = f"Title: {new_post.title}, Content: {new_post.content}, Rating: {new_post.rating}"
    if new_post.published:
        summary += ", and it's published"

    return {'new_post': summary}

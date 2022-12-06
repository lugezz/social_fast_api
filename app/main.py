from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, status
# from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


app = FastAPI()
my_posts = [
    {'id': 1, 'title': 'favourite food', 'content': 'this is the favourite food for Artime'},
    {'id': 2, 'title': 'favourite music', 'content': 'this is the favourite music for Artime in 2022'},
    {'id': 3, 'title': 'old favourite music', 'content': 'this is the favourite music for Artime in 2021'},
]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', dbname='fastapi', user='artime', password='artime80',
                            cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("Database connection was successfully")

except Exception as error:
    print("Connection to database failed")
    print("Error:", error)


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Cachulengo"}


@app.get("/posts")
def get_posts():
    return {"Data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # We expect: title: str, body: str
    post_dict = post.dict()
    post_dict['id'] = randrange(3, 1000)

    my_posts.append(post_dict)

    return {'all_posts': my_posts}


def get_data_from_id(id: int) -> dict:
    resp = {}

    for post in my_posts:
        if post['id'] == id:
            resp = post
            break

    return resp


def get_index_from_id(id: int) -> dict:
    resp = -1

    for ind, post in enumerate(my_posts):
        if post['id'] == id:
            resp = ind
            break

    return resp


@app.get("/posts/latest")
def get_latest():
    this_post = my_posts[-1]

    return {"Data": this_post}


@app.get("/posts/{id}")
def get_post(id: int):
    this_post = get_data_from_id(id)

    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Id {id} not found'}

    return {"Data": this_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    this_post_index = get_index_from_id(id)
    deleted_post = ''

    if this_post_index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})
    else:
        deleted_post = my_posts.pop(this_post_index)

    return {"Data": f"Post {deleted_post['title']} deleted"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    this_post_index = get_index_from_id(id)

    if this_post_index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})
    else:
        this_post = post.dict()
        this_post['id'] = id
        my_posts[this_post_index] = this_post
        print(my_posts)

    return {"Data": f"Post {this_post['title']} updated"}

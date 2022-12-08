import time
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
retries = 5


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while retries > 0:
    try:
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='artime', password='artime80',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)
        retries -= 1


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Cachulengo"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"Data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    sql_sentence = f"INSERT INTO posts (title, content, published) VALUES ('{post.title}', '{post.content}',{post.published})"
    sql_sentence += " RETURNING *"
    print(sql_sentence)

    cursor.execute(sql_sentence)
    new_post = cursor.fetchone()

    # Commit changes
    conn.commit()

    return {'new_post': new_post}


@app.get("/posts/latest")
def get_latest():
    this_post = my_posts[-1]

    return {"Data": this_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(f"SELECT * FROM posts WHERE ID = {id}")
    this_post = cursor.fetchone()

    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Id {id} not found'}

    return {"Data": this_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(f"DELETE FROM posts WHERE ID = {id} RETURNING *")
    this_deleted_post = cursor.fetchone()

    if not this_deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    conn.commit()

    return {"Data": f"Post {this_deleted_post['title']} deleted"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    sql_sentence = "UPDATE posts SET "
    sql_sentence += f"title = '{post.title}', content = '{post.content}'"
    if post.published:
        sql_sentence += f", published = {post.published}"
    sql_sentence += f" WHERE id = {id} RETURNING *"

    cursor.execute(sql_sentence)
    this_post = cursor.fetchone()
    conn.commit()

    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return {"Data": f"Post {this_post['title']} updated"}

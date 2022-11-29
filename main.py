from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Cachulengo"}


@app.get("/posts")
def get_post():
    return {"Data": "This is your posts"}


@app.post("/createposts")
def create_post(pay_load: dict = Body):
    print(pay_load)
    return {'new_post': f"Title: {pay_load['title']}, Content: {pay_load['content']}"}

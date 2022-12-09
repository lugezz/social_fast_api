from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import post, user


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World my old friend"}

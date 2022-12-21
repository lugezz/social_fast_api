from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import auth, post, user, vote


origins = [
    "http://localhost",
    "http://localhost:8080",
]

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Change in Docker!!!"}

import logging

from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI

from app.database.database import Base, engine

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from Render"}
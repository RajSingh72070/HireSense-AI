import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

print("1")

from fastapi import FastAPI
print("2")

from app.database.database import Base, engine
print("3")

from app.database import models
print("4")

Base.metadata.create_all(bind=engine)
print("5")

app = FastAPI()

@app.get("/")
def home():
    return {"status": "working"}
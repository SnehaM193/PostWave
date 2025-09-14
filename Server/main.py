from database import SessionLocal, engine, base
from fastapi import FastAPI
from routes import user

base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(user.router)
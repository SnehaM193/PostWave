from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, base
from models.UserModel import User
import schemas
import bcrypt

base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash                                                                     
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all users
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_users(user_id: int ,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 400, detail="User Not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_users(user_id: int, updated_data: schemas.UserCreate,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code= 400, details="User not found")
    
    user.first_name = updated_data.first_name
    user.last_name = updated_data.last_name
    user.email = updated_data.email

    if updated_data.password:
        bytes_pw = updated_data.password.encode('utf-8')
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(bytes_pw, salt).decode("utf-8") 

        db.commit()
        db.refresh(user)
        return user

@app.delete("/users/")
def delete_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 400, details = "User not found")
    
    db.delete(user)
    db.commit()
    return({"message": "deleted Successfully"})

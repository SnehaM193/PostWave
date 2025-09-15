from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import bcrypt
from schemas import user as user_schemas
from models.user import User
from database import get_db

def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    bytes_pw = user.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(bytes_pw, salt).decode("utf-8")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_pw                                                                     
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User Not found")
    return user


def update_user(user_id: int, updated_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    user.first_name = updated_data.first_name
    user.last_name = updated_data.last_name
    user.email = updated_data.email

    if updated_data.password:
        bytes_pw = updated_data.password.encode("utf-8")
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(bytes_pw, salt).decode("utf-8") 

    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User Deleted Successfully"}

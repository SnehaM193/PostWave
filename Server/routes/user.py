from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers import user

router = APIRouter(prefix="/users", tags=["users"])

db = get_db()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user_to_create: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create_user(user_to_create, db)

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int ,db: Session = Depends(get_db)):
    return user.get_user_by_id(user_id, db)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_users(user_id: int, updated_data: schemas.UserCreate,db: Session = Depends(get_db)):
    return user.update_user(user_id, updated_data, db)

@router.delete("/")
def delete_users(user_id: int, db: Session = Depends(get_db)):
    return user.delete_user(user_id, db)
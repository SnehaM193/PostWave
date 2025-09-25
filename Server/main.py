from database import engine, base, get_db
from fastapi import FastAPI
from routes import user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
import schemas.user as schemas
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "supersecretkey"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(user.router)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}



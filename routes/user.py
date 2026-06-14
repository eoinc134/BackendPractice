
import os
import jwt

from dotenv import load_dotenv
from sqlmodel import select
from typing import Annotated
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.database import SessionDep
from db.models import User, TokenData, Token, UserRead

# Router Setup
user_router = APIRouter(prefix='/users', tags=['users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
password_hash = PasswordHash.recommended()

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# HELPER FUNCTIONS
# Get user by username
def get_user(username: str, session: SessionDep):
    return session.exec(select(User).where(User.username == username)).first()

# Authenticate user
def authenticate_user(username: str, password: str, session: SessionDep):
    user = get_user(username, session)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

# Get current user
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
        
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user
        
# Get current active user
def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Password hashing and verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# ROUTES
# GET current user
@user_router.get('/current', response_model=UserRead)
async def read_current_users(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# LOGIN
@user_router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    
    if not user :
        raise HTTPException(status_code=400, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

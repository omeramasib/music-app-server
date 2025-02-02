import uuid
import bcrypt
from fastapi import HTTPException
from fastapi.params import Depends
from database import get_db
from models.user import User
from schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session

from schemas.user_login import UserLogin

router = APIRouter()

@router.post('/signup', status_code=201)
def singup_user(user: UserCreate, db:Session=Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400, "User already exists")
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db = User(id=str(uuid.uuid4()), email=user.email, password= hashed_pw, name= user.name)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

@router.post('/login')
def login_user(user: UserLogin, db:Session=Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(400, "User not found")
    is_match = bcrypt.checkpw(user.password.encode(), user_db.password)
    if not is_match:
        raise HTTPException(400, "Invalid password")
    return user_db
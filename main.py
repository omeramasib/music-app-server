from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import VARCHAR, Column, TEXT, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from . import database
import uuid
import bcrypt

app = FastAPI()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

database.Base.metadata.create_all(bind=database.engine)



@app.post('/singup')
def singup_user(user: UserCreate):
    user_db = database.db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400, "User already exists")
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db = User(id=str(uuid.uuid4()), email=user.email, password= hashed_pw, name= user.name)
    database.db.add(user_db)
    database.db.commit()
    database.db.refresh(user_db)

    return user_db
    

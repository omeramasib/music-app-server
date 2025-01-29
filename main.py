from fastapi import FastAPI, Request
from pydantic import BaseModel
from sqlalchemy import VARCHAR, Column, TEXT, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

DATABASE_URL = "postgresql://postgres:password123@localhost:5432/musicapp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
db = SessionLocal()
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)


Base.metadata.create_all(bind=engine)
@app.post('/singup')
def singup_user(user: UserCreate):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        return "User already exists"
from datetime import datetime, timedelta #date and timedelta to generate a jwt token.
#fast api
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles

#jwt creation
from jose import jwt

#SqlLite
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

Base = declarative_base()
engine = create_engine("sqlite:///./credentials.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SECRET_KEY = "key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@app.post("/login/")
async def login_for_access_token(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        # if authenticated generate token.
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        # If authentication fails, return an error
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
@app.post("/add_user/")
async def add_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    new_user = User(username=username, password=password)
    db.add(new_user)
    try:
        db.commit()
        return {"message": f"User {username} added successfully."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

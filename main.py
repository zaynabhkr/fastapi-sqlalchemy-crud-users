from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel

from typing import Optional
#initialize FastAPI application
from fastapi import FastAPI, Form, Depends, HTTPException
app = FastAPI()

#Basic connection to SQL database
DATABASE_URL = "sqlite:///./test.db"
#SQLite referral with /// mneaning it is in the current directory
## and ./test.db is the directory where the database will be created

engine = create_engine(DATABASE_URL,  connect_args={"check_same_thread": False})
#"check_same_thread" is used for SQLite to not allow multiple thread connections

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#sessionmaker is used to create a new session objects (database connections)
##autcommit=False means that you manually commit your changes to the database
##autoflUsh=False means that you manually control when changes are saved
##bind=engine means that I am bounding this connection to the variable engine

Base = declarative_base()
#Session = is used to interact with the database
#Engine = is the connection between the database and Python
#base = is the structure for our model

#creating the database columns and structure
class User(Base):
    __tablename__ = "users"
    id : int = Column(Integer, primary_key=True, index=True)
    name : str = Column(String, index=True)
    email : str = Column(String, unique=True, index=True)


#PYDANTIC MODEL FOR Response
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True
    

Base.metadata.create_all(bind=engine)
#look at all classes that inheret from Base (like User)
##and create tables for the database using engine

def get_db():
    db = SessionLocal() #Sessionlocal() is like a factory that creates new database sessions
    try:
        yield db #yield is like return but temporary
    finally:
        db.close() #make sure database is closed DESPITE ERRORS
"""
#using CRUD operations to create a new user with the session
@app.post("/users/", response_model=User)
#response model will follow the structure of the User model
def create_users(user:User, db : Session=Depends(get_db)):
"""
##### ---------------------- Reading Records from the Database ------------------------------
#1/ Creating a pytdantic Model called UserCreate
class UserCreate(BaseModel):
    name: str
    email: str

#2/ ing create operation with POST whose response will be in the form of the "User" Model
@app.post("/users/", response_model = UserResponse)
def create_users(users: UserCreate, db : Session=Depends(get_db)):
    ## for the depends(get_db) FPI tells python to run the get_db function to get a database session.
    ##Creating an instance of Users using the CreateUser Pydantic Model
    new_user = User(name=users.name, email=users.email)
    ## add the new_user to the session db
    db.add(new_user)
    ## commit the changes to the database
    db.commit()
    ## refresh in case of "id" reloading
    db.refresh(new_user)
    ## return the new_user instance in the form of JSON
    return new_user

###### ---------------------- Reading Records from the Database ----------------------------

#1/ creating an end points which returns list of all users in database
@app.get("/users/", response_model=list[UserResponse])
#2/ limit the nubmer of users returned to 10 and skip the first 0 users
def get_users(skip : int = 0, limit : int= 10, db : Session=Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    #query is a method that is another way of saying:
    ## it is like "SELECT * FROM users"
    ## .......... "LIMIT 10 OFFSET 0"
    return users

#3/ filter out data based on user ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_id(user_id: int, db : Session=Depends(get_db)):
                user = db.query(User).filter(User.id == user_id).first()
                if user is None:
                    raise HTTPException(status_code=404, detail="User not found")
                    ##return an appropriate HTTP response (like 404, 400, 401, 500, etc.) 
                else: 
                    return user
                    
###### ---------------------- Updating Records from the Database ----------------------------
#1/ creating a pydantic Model for updates

class UserUpdate(BaseModel):
     name : Optional[str] = None # means that this field can be str or None
     email : Optional[str] = None

@app.put("/users/{user_id}", response_model = UserResponse)
def update_user(user_id : int, user: UserUpdate,db : Session=Depends(get_db)):
     db_user = db.query(User).filter(user_id == User.id).first()
     if user is None :
        raise HTTPException(status_code=404, detail="User not found")
     else:
        db_user.name = user.name if user.name is not None else User.name
        db_user.email = user.email if user.email is not None else User.email
        db.commit()
        db.refresh(db_user)
        ##remember db_user is the existing user record while user is the income data from teh API
        return db_user

###### ---------------------- Deleting Records from the Database ----------------------------

@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id : int, db : Session=Depends(get_db)):
     db_user = db.query(User).filter(user_id == User.id).first()
     if db_user is None:
          raise HTTPException(status_code=404, detail="User not found")
     db.delete(db_user)
     db.commit()
     return db_user
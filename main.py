from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import authentication
import crud
import models
import schemas
import database


# from .database import SessionLocal, engine

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def authenticate_user( username: str, password: str ,db:Session):
    user = crud.get_user_by_email(db= db, email =username)
    if not user:
        return False
    if not authentication.verify_password(password, user.password):
        return False
    return user


    
async def get_current_user(token: str = Depends(authentication.oauth2_scheme) , db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(token, authentication.SECRET_KEY, algorithms=[authentication.ALGORITHM])
        username=  payload.get("sub")  
        if username is None:
            raise credentials_exception
        token_data_username= authentication.TokenData(username=username).username
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data_username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


#*********************
#Users / Login / Auth
#*********************

@app.post("/token", response_model=authentication.Token,)
async def login_for_access_token(form_data: schemas.Login, db: Session = Depends(get_db)):
    user = authenticate_user( form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.post("/users/CreateUser", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_200_OK, 
            detail="Email already registered"
        )
    response =  crud.create_user(db=db, user=user)
    return response




@app.get("/users/", response_model=list[schemas.User])
def read_users(token: str = Depends(authentication.oauth2_scheme) ,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # return users
    return users



@app.get("/users/me")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user






#*********************
#Meetings
#*********************



@app.post("/meeting/CreateMeeting", response_model=schemas.Meeting)
def create_meeting( meeting: schemas.MeetingBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_meeting(db=db, meeting=meeting)
    return responseBody




#*********************
#Conferences
#*********************


@app.post("/conference/CreateConference", response_model=schemas.Conference)
def create_conference( conference: schemas.ConferenceBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_conference(db=db, conference=conference)
    return responseBody



#*********************
#Workshops
#*********************


@app.post("/workshop/CreateWorkshop", response_model=schemas.Workshop)
def create_workshop( workshop: schemas.WorkshopBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_workshop(db=db, workshop=workshop)
    return responseBody







@app.get("/users/{user_id}", response_model=schemas.User)
def read_user( user_id: int,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

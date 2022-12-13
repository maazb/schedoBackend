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

@app.post("/token",tags=["Users"])
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
    return {"access_token": access_token, "token_type": "bearer", "detail": {
    "name": user.name,
    "email": user.email,
    "contact": user.contact,
    "image" : user.image,
    "meetingCal": user.meetingCal,
    "eventCal": user.eventCal,
    "newMeetingsOnHome": user.newMeetingsOnHome,
    "newMessagesOnHome": user.newMessagesOnHome,
    "newMessageNotifications": user.newMessageNotifications,
    "newMeetingNotifications": user.newMeetingNotifications,
    "requested": user.requested,
    "added": user.added,
    "id": user.id,
    "is_active": user.is_active
} }




@app.post("/users/CreateUser", response_model=schemas.User,tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_200_OK, 
            detail="Email already registered"
        )
    response =  crud.create_user(db=db, user=user)
    return response




@app.get("/users/", response_model=list[schemas.User],tags=["Users"])
def read_users(token: str = Depends(authentication.oauth2_scheme) ,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # return users
    return users

@app.put("/users/EditUser", response_model=schemas.User,tags=["Users"])
def edit_user( user: schemas.UserBase,token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    responseBody =  crud.edit_user(db, user, id)
    return responseBody

@app.delete("/users/DeleteUser",tags=["Users"])
def delete_user(token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    crud.delete_user(db, id)
    return {"success" : "user deleted"}


@app.get("/users/{user_id}", response_model=schemas.User,tags=["Users"])
def read_user( user_id: int,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




@app.get("/users/me",tags=["Users"])
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user






#*********************
#Meetings
#*********************



@app.post("/meeting/CreateMeeting", response_model=schemas.Meeting,tags=["Meeting"])
def create_meeting( meeting: schemas.MeetingBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_meeting(db=db, meeting=meeting)
    return responseBody


@app.get("/meeting/GetMeetings", response_model=list[schemas.Meeting],tags=["Meeting"])
def read_meetings(token: str = Depends(authentication.oauth2_scheme) ,date: str = "2022-12-11", db: Session = Depends(get_db)):
    meetings = crud.get_meetings(db, date)
    # return meetings
    return meetings


@app.get("/meeting/GetMeetingsByUser", response_model=list[schemas.Meeting],tags=["Meeting"])
def read_meetings_user(token: str = Depends(authentication.oauth2_scheme) ,date: str = "2022-12-11", userId: int =0, db: Session = Depends(get_db)):
    meetings = crud.get_user_meetings(db, date, userId)
    # return meetings
    return meetings


@app.put("/meeting/EditMeeting", response_model=schemas.Meeting,tags=["Meeting"])
def edit_meeting( meeting: schemas.MeetingBase,token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    responseBody =  crud.edit_meeting(db, meeting, id)
    return responseBody

@app.delete("/meeting/DeleteMeeting",tags=["Meeting"])
def delete_meeting(token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    crud.delete_meeting(db, id)
    return {"success" : "meeting deleted"}




#*********************
#Events
#*********************



@app.post("/event/CreateEvent", response_model=schemas.Event,tags=["Event"])
def create_event( event: schemas.EventBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_event(db=db, event=event)
    return responseBody


@app.get("/event/GetEvents", response_model=list[schemas.Event],tags=["Event"])
def read_events(token: str = Depends(authentication.oauth2_scheme) ,date: str = "2022-12-11", db: Session = Depends(get_db)):
    events = crud.get_events(db, date)
    # return meetings
    return events

@app.get("/event/GetEventsByUser", response_model=list[schemas.Event],tags=["Event"])
def read_events_user(token: str = Depends(authentication.oauth2_scheme) ,date: str = "2022-12-11", userId: int =0, db: Session = Depends(get_db)):
    events = crud.get_user_events(db, date,userId)
    # return meetings
    return events

@app.put("/event/EditEvent", response_model=schemas.Event,tags=["Event"])
def edit_event( event: schemas.EventBase,token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    responseBody =  crud.edit_event(db, event, id)
    return responseBody

@app.delete("/event/DeleteEvent",tags=["Event"])
def delete_event(token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    crud.delete_event(db, id)
    return {"success" : "event deleted"}





@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

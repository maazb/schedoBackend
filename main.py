from datetime import datetime, timedelta
from time import strptime
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import authentication
import crud
from fcm_admin import event_cancelled, initializeFB, meeting_cancelled, new_event, new_meeting
import models
import schemas
import database
from support import checkSlots, checkSlotsEvents, sendOTP


# from .database import SessionLocal, engine

models.database.Base.metadata.create_all(bind=database.engine)



app = FastAPI()


@app.on_event("startup")
async def startup_event():
    init = initializeFB()

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
    "fcmId" : user.fcmId,
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
    
    
@app.post("/users/UpdatePassword",tags=["Users"])
async def update_password( form_data: schemas.UpdatePassword, token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):
    user = authenticate_user( form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    crud.update_password(db,user.id, form_data.newPassword)
    
    return {"success": "password updated"}


@app.post("/users/NewPassword",tags=["Users"])
async def new_password( token: str = Depends(authentication.oauth2_scheme),email: str = "", newPassword: str = "", db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    crud.update_password(db, user.id, newPassword )
    
    return {"success": "password updated"}


@app.post("/users/SendOTP",tags=["Users"])
async def send_otp( token: str = Depends(authentication.oauth2_scheme),email: str = "", db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    otp= sendOTP(email)
    
    return {"otp": otp}




@app.post("/users/CreateUser", response_model=schemas.User,tags=["Users"])
def create_user( user: schemas.UserCreate,  db: Session = Depends(get_db)):
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

@app.get("/users/Names", response_model=list[schemas.UserShrinked],tags=["Users"])
def read_user_names(token: str = Depends(authentication.oauth2_scheme) , db: Session = Depends(get_db)):
    users = crud.get_users_all(db)
    return users

@app.get("/users/Search", response_model=list[schemas.UserShrinked],tags=["Users"])
def search_users(token: str = Depends(authentication.oauth2_scheme) , query: str = "", db: Session = Depends(get_db)):
    users = crud.get_users_by_name_email(db, query)
    return users

@app.get("/users/Requests", response_model=list[schemas.UserShrinked],tags=["Users"])
def get_requests(token: str = Depends(authentication.oauth2_scheme) , uId: int = 0, db: Session = Depends(get_db)):
    users = crud.get_user_requests(db, uId)
    return users

@app.put("/users/EditUser", response_model=schemas.User,tags=["Users"])
def edit_user( user: schemas.UserBase,token: str = Depends(authentication.oauth2_scheme), id: int =0 , db: Session = Depends(get_db)):    
    responseBody =  crud.edit_user(db, user, id)
    return responseBody

@app.put("/users/UpdateFcm", response_model=schemas.User,tags=["Users"])
def updateFcm(token: str = Depends(authentication.oauth2_scheme),fcmId: str = "", id: int =0 , db: Session = Depends(get_db)):    
    responseBody =  crud.update_fcmId(db, fcmId, id)
    return responseBody

# @app.put("/users/sendReq", response_model=schemas.User,tags=["Users"])
# def send_req(token: str = Depends(authentication.oauth2_scheme), fromId: int =0 , toId: int =0 , db: Session = Depends(get_db)):    
#     responseBody =  crud.send_req(db, fromId, toId)
#     return responseBody

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
    tokens = crud.get_users_noti(db,meeting)
    new_meeting(tokens, meeting.title, meeting.start_date)
    return responseBody

@app.post("/meeting/CreateMeetingAuto",tags=["Meeting"])
def create_meeting_auto( meeting: schemas.MeetingBase,token: str = Depends(authentication.oauth2_scheme), duration: int =0, db: Session = Depends(get_db)):  
        
        
    # td = timedelta(minutes=duration)
    commonSlots = checkSlots(db=db,dt=meeting.start_date,pst=meeting.start_time,pet=meeting.end_time,uids=meeting.attendees, min=duration)
    if not commonSlots:
        st = datetime.strptime(meeting.start_time,'%Y-%m-%dT%H:%M:%SZ')
        et = datetime.strptime(meeting.end_time,'%Y-%m-%dT%H:%M:%SZ')
        st = st.replace(hour=9 , minute= 0)
        et = et.replace(hour=21 , minute= 0)
        tst = datetime.strftime(st,'%Y-%m-%dT%H:%M:%SZ')
        tet = datetime.strftime(et,'%Y-%m-%dT%H:%M:%SZ')
        recommendedSlots = checkSlots(db=db,dt=meeting.start_date,pst=tst,pet=tet,uids=meeting.attendees,min=duration)
        print("rec len: ")
        print(len(recommendedSlots))
        responseBody = {"status" : False,
            "recomended" : 
            recommendedSlots
        }
        return responseBody
        
    else:
        s = next(iter(commonSlots))
        temp = meeting
        temp.start_time = s[0]
        temp.end_time = s[1]
        mt =  crud.create_meeting(db=db, meeting=temp)
        tokens = crud.get_users_noti(db,meeting)
        new_meeting(tokens, meeting.title, meeting.start_date)
        return {"status" : True,
            "detail" : 
            {
                "title": mt.title,
                "detail": mt.detail,
                "meeting_type": mt.meeting_type,
                "start_date": mt.start_date,
                "end_date": mt.end_date,
                "start_time": mt.start_time,
                "end_time": mt.end_time,
                "createdBy": mt.createdBy,
                "link": mt.link,
                "attendees": mt.attendees,
                "seen": mt.seen,
                "id": mt.id
            }
        }
        
    
    # # for x in commonFreeSlots:
    # print("Slot selected: ")
    # print(r)
    
    # responseBody =  crud.create_meeting(db=db, meeting=meeting)
    # tokens = crud.get_users_noti(db,meeting)
    # new_meeting(tokens, meeting.title, meeting.start_date)
    # return responseBody


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
    mt =  crud.get_meeting_by_id(db,id)
    tokens =crud.get_users_noti(db, mt)
    meeting_cancelled(tokens,mt)    
    crud.delete_meeting(db, id)
    return {"success" : "meeting deleted"}




#*********************
#Events
#*********************



@app.post("/event/CreateEvent", response_model=schemas.Event,tags=["Event"])
def create_event( event: schemas.EventBase,token: str = Depends(authentication.oauth2_scheme), db: Session = Depends(get_db)):    
    responseBody =  crud.create_event(db=db, event=event)
    tokens = crud.get_users_noti_event(db,event)
    new_event(tokens, event.title, event.date)
    return responseBody


@app.post("/event/CreateEventAuto",tags=["Event"])
def create_event_auto( event: schemas.EventBase,token: str = Depends(authentication.oauth2_scheme), duration: int = 0, db: Session = Depends(get_db)):  
    # td = timedelta(minutes=duration)
    commonSlots = checkSlotsEvents(db=db,dt=event.date,pst=event.start_time,pet=event.end_time,uids=event.attendees, min=duration)
    if not commonSlots:
        st = datetime.strptime(event.start_time,'%Y-%m-%dT%H:%M:%SZ')
        et = datetime.strptime(event.end_time,'%Y-%m-%dT%H:%M:%SZ')
        st = st.replace(hour=9 , minute= 0)
        et = et.replace(hour=21 , minute= 0)
        tst = datetime.strftime(st,'%Y-%m-%dT%H:%M:%SZ')
        tet = datetime.strftime(et,'%Y-%m-%dT%H:%M:%SZ')
        recommendedSlots = checkSlotsEvents(db=db,dt=event.date,pst=tst,pet=tet,uids=event.attendees, min=duration)
        print("rec len: ")
        print(len(recommendedSlots))
        responseBody = {"status" : False,
            "recomended" : 
            recommendedSlots
        }
        return responseBody
    
    else:
        s = next(iter(commonSlots))
        temp = event
        temp.start_time = s[0]
        temp.end_time = s[1]
        mt =  crud.create_event(db=db, event=temp)
        tokens = crud.get_users_noti(db,event)
        new_event(tokens, event.title, event.date)
        return {"status" : True,
            "detail" : 
            {
                "title": mt.title,
                "detail": mt.detail,
                "event_type": mt.event_type,
                "date": mt.date,
                "start_time": mt.start_time,
                "end_time": mt.end_time,
                "createdBy": mt.createdBy,
                "attendees": mt.attendees,
                "id": mt.id
            }
        }


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
    mt =  crud.get_event_by_id(db,id)
    tokens =crud.get_users_noti_event(db, mt)
    event_cancelled(tokens,mt)   
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

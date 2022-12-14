from sqlalchemy import func, true
from sqlalchemy.orm import Session
import json as js
import models
import schemas
import authentication
from support import checkEmail



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(func.lower(models.User.email) == email.lower()).first()

def get_users_by_name_email(db: Session, query: str):
    if(checkEmail(query)):
        return db.query(models.User).filter(func.lower(models.User.email) == query.lower()).all()
    else:
        return db.query(models.User).filter(func.lower(models.User.name).contains(query.lower())).all()
    

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_all(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    passHash = authentication.get_password_hash(user.password)
    db_user = models.User(email=user.email,password = passHash,contact = user.contact, name = user.name, image = user.image, meetingCal = user.meetingCal, eventCal = user.eventCal, newMeetingsOnHome = user.newMeetingsOnHome, newMessagesOnHome = user.newMessagesOnHome, newMessageNotifications = user.newMessageNotifications, newMeetingNotifications = user.newMeetingNotifications, requested = user.requested, added = user.added)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_user(db: Session, user: schemas.UserBase,  id: int = 0,):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.contact = user.contact
        db_user.image = user.image
        db_user.meetingCal = user.meetingCal
        db_user.eventCal = user.eventCal
        db_user.newMeetingsOnHome = user.newMeetingsOnHome
        db_user.newMessagesOnHome = user.newMessagesOnHome
        db_user.newMessageNotifications = user.newMessageNotifications
        db_user.newMeetingNotifications = user.newMeetingNotifications
        db_user.requested = user.requested
        db_user.added = user.added
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, id: int = 0, newPass: str = "xbcx"):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        db_user.password = authentication.get_password_hash(newPass)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session,  id: int = 0,):
    db_user = db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return True








def create_meeting(db: Session, meeting: schemas.MeetingBase):
    db_meeting = models.Meeting(title= meeting.title, detail= meeting.detail, meeting_type = meeting.meeting_type, start_date = meeting.start_date, end_date = meeting.end_date, start_time = meeting.start_time, end_time = meeting.end_time,seen = meeting.seen, createdBy = meeting.createdBy, link = meeting.link, attendees = meeting.attendees)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def get_meetings(db: Session, date: str = ""):
    return db.query(models.Meeting).filter(models.Meeting.start_date == date).all()

def get_user_meetings(db: Session, date: str = "", userId: int = 0):
    return db.query(models.Meeting).where(models.Meeting.start_date == date, models.Meeting.attendees.any(userId)).all()

def edit_meeting(db: Session, meeting: schemas.MeetingBase,  id: int = 0,):
    db_meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if db_meeting:
        db_meeting.title = meeting.title
        db_meeting.detail = meeting.detail
        db_meeting.meeting_type = meeting.meeting_type
        db_meeting.start_date = meeting.start_date
        db_meeting.end_date = meeting.end_date
        db_meeting.start_time = meeting.start_time
        db_meeting.end_time = meeting.end_time
        db_meeting.seen = meeting.seen
        db_meeting.createdBy = meeting.createdBy
        db_meeting.link = meeting.link
        db_meeting.attendees = meeting.attendees
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def delete_meeting(db: Session,  id: int = 0,):
    db_meeting = db.query(models.Meeting).filter(models.Meeting.id == id).delete()
    db.commit()
    return True





def create_event(db: Session, event: schemas.EventBase):
    db_event = models.Event(title= event.title, detail = event.detail, event_type = event.event_type, date = event.date, start_time = event.start_time, end_time = event.end_time, createdBy = event.createdBy, attendees = event.attendees)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, date: str = ""):
    return db.query(models.Event).filter(models.Event.date == date).all()

def get_user_events(db: Session, date: str = "", userId: int = 0):
    return db.query(models.Event).filter(models.Event.date == date, models.Event.attendees.any(userId)).all()

def edit_event(db: Session, event: schemas.EventBase,  id: int = 0,):
    db_event = db.query(models.Event).filter(models.Event.id == id).first()
    if db_event:
        db_event.title = event.title
        db_event.detail = event.detail
        db_event.event_type = event.event_type
        db_event.date = event.date
        db_event.start_time = event.start_time
        db_event.end_time = event.end_time
        db_event.createdBy = event.createdBy
        db_event.attendees = event.attendees
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session,  id: int = 0,):
    db_event = db.query(models.Event).filter(models.Event.id == id).delete()
    db.commit()
    return True



# def create_conference(db: Session, conference: schemas.ConferenceBase):
#     db_conference = models.Conference(title= conference.title, start_date = conference.start_date, end_date = conference.end_date, start_time = conference.start_time, end_time = conference.end_time,seen = conference.seen, attendees = conference.attendees)
#     db.add(db_conference)
#     db.commit()
#     db.refresh(db_conference)
#     return db_conference

# def create_workshop(db: Session, workshop: schemas.WorkshopBase):
#     db_workshop = models.Workshop(title= workshop.title, start_date = workshop.start_date, end_date = workshop.end_date, start_time = workshop.start_time, end_time = workshop.end_time,seen = workshop.seen, attendees = workshop.attendees)
#     db.add(db_workshop)
#     db.commit()
#     db.refresh(db_workshop)
#     return db_workshop


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

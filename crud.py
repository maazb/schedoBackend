from sqlalchemy.orm import Session
import json as js
import models
import schemas
import authentication



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    passHash = authentication.get_password_hash(user.password)
    db_user = models.User(email=user.email,password = passHash,contact = user.contact, name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_meeting(db: Session, meeting: schemas.MeetingBase):
    db_meeting = models.Meeting(title= meeting.title, date = meeting.date, start_time = meeting.start_time, end_time = meeting.end_time,seen = meeting.seen, attendees = meeting.attendees)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def create_conference(db: Session, conference: schemas.ConferenceBase):
    db_conference = models.Conference(title= conference.title, start_date = conference.start_date, end_date = conference.end_date, start_time = conference.start_time, end_time = conference.end_time,seen = conference.seen, attendees = conference.attendees)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference

def create_workshop(db: Session, workshop: schemas.WorkshopBase):
    db_workshop = models.Workshop(title= workshop.title, start_date = workshop.start_date, end_date = workshop.end_date, start_time = workshop.start_time, end_time = workshop.end_time,seen = workshop.seen, attendees = workshop.attendees)
    db.add(db_workshop)
    db.commit()
    db.refresh(db_workshop)
    return db_workshop


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

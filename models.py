from ast import List
import datetime
from operator import index
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import database


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    contact = Column(String)
    name = Column(String)
    password = Column(String)
    
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    

class Meeting(database.Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(String )
    start_time = Column(String)
    end_time  = Column(String)
    attendees = Column(ARRAY(Integer))
    seen = Column(Boolean)
    
    
class Conference(database.Base):
    __tablename__ = "conferences"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start_date = Column(String)
    end_date = Column(String)
    start_time = Column(String)
    end_time  = Column(String)
    attendees = Column(ARRAY(Integer))
    seen = Column(Boolean)

class Workshop(database.Base):
    __tablename__ = "workshops"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start_date = Column(String)
    end_date = Column(String)
    start_time = Column(String)
    end_time  = Column(String)
    attendees = Column(ARRAY(Integer))
    seen = Column(Boolean)


class Item(database.Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

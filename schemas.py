from typing import Union

from pydantic import BaseModel

class MeetingBase(BaseModel):
    title: str
    meeting_type: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    attendees: list[int] = []
    seen : bool
    
class EventBase(BaseModel):
    title: str
    event_type: str
    date: str
    start_time: str
    end_time: str
    attendees: list[int] = []
    
    
# class ConferenceBase(BaseModel):
#     title: str
#     start_date: str
#     end_date: str
#     start_time: str
#     end_time: str
#     attendees: list[int] = []
#     seen : bool
    
# class WorkshopBase(BaseModel):
#     title: str
#     start_date: str
#     end_date: str
#     start_time: str
#     end_time: str
#     attendees: list[int] = []
#     seen : bool
    
# class MeetingCreate(MeetingBase):
#     id:int
   
class Meeting(MeetingBase):
    id:int
    
    class Config:
        orm_mode = True
        
        
class Event(EventBase):
    id:int
    
    class Config:
        orm_mode = True
        
# class Conference(ConferenceBase):
#     id:int
    
#     class Config:
#         orm_mode = True
        
# class Workshop(WorkshopBase):
#     id:int
    
#     class Config:
#         orm_mode = True
    
    



class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    contact : str
    image : str
    meetingCal : str
    eventCal: str
    newMeetingsOnHome : bool
    newMessagesOnHome : bool
    newMessageNotifications : bool
    newMeetingNotifications : bool
    requested: list[int] = []
    added: list[int] = []
    
class Login(BaseModel):
    username: str
    password: str
    


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # items: list[Item] = []

    class Config:
        orm_mode = True

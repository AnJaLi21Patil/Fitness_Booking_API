from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ClassCreate(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

class BookingCreate(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

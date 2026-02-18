from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class FitnessClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_time = Column(DateTime)
    instructor = Column(String)
    available_slots = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    client_name = Column(String)
    client_email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

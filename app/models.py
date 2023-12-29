from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    location = Column(String, nullable=False)
    time = Column(Time)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    # owner = relationship("User")
    



from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.datetime.utcnow)

    applications=relationship("JobApplication",back_populates="user")


class JobApplication(Base):
    __tablename__="job_applications"

    id=Column(Integer,primary_key=True,index=True)
    company=Column(String,nullable=False)
    role=Column(String,nullable=False)
    status=Column(String,default="Applied")
    applied_at=Column(DateTime,default=datetime.datetime.utcnow)
    user_id=Column(Integer,ForeignKey("users.id"))

    user=relationship("User",back_populates="applications")
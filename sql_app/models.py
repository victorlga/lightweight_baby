from sqlalchemy import Float, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Plan(Base):
    __tablename__ = "plans"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False)
    value = Column(Float, nullable=False)
    description = Column(String(200))

class Member(Base):
    __tablename__ = "members"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(50), unique=True, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.ID"), nullable=False)
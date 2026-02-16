from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    plans = relationship("Plan", back_populates="owner")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    owner = relationship("Profile", back_populates="plans")
    macrocycles = relationship("Macrocycle", back_populates="plan")


class Macrocycle(Base):
    __tablename__ = "macrocycles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))

    plan = relationship("Plan", back_populates="macrocycles")
    microcycles = relationship("Microcycle", back_populates="macrocycle")


class Microcycle(Base):
    __tablename__ = "microcycles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    macrocycle_id = Column(Integer, ForeignKey("macrocycles.id"))

    macrocycle = relationship("Macrocycle", back_populates="microcycles")
    sessions = relationship("Session", back_populates="microcycle")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    sport = Column(String)
    duration_minutes = Column(Integer)
    date_start = Column(DateTime)
    perceived_exertion = Column(Integer) # 1-10
    microcycle_id = Column(Integer, ForeignKey("microcycles.id"))

    microcycle = relationship("Microcycle", back_populates="sessions")

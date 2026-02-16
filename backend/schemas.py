from typing import List, Optional
from pydantic import BaseModel
from datetime import date

# Session Schemas
class SessionBase(BaseModel):
    description: str
    sport: str
    duration_minutes: int
    date_start: date
    perceived_exertion: int

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    microcycle_id: int

    class Config:
        from_attributes = True

# Microcycle Schemas
class MicrocycleBase(BaseModel):
    name: str

class MicrocycleCreate(MicrocycleBase):
    pass

class Microcycle(MicrocycleBase):
    id: int
    macrocycle_id: int
    sessions: List[Session] = []

    class Config:
        from_attributes = True

# Macrocycle Schemas
class MacrocycleBase(BaseModel):
    name: str

class MacrocycleCreate(MacrocycleBase):
    pass

class Macrocycle(MacrocycleBase):
    id: int
    plan_id: int
    microcycles: List[Microcycle] = []

    class Config:
        from_attributes = True

# Plan Schemas
class PlanBase(BaseModel):
    title: str
    description: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    profile_id: int
    macrocycles: List[Macrocycle] = []

    class Config:
        from_attributes = True

# Profile Schemas
class ProfileBase(BaseModel):
    username: str

class ProfileCreate(ProfileBase):
    password: str

class Profile(ProfileBase):
    id: int
    plans: List[Plan] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Profile
def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profile_by_username(db: Session, username: str):
    return db.query(models.Profile).filter(models.Profile.username == username).first()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    hashed_password = get_password_hash(profile.password)
    db_profile = models.Profile(username=profile.username, password_hash=hashed_password)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Plan
def get_plans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plan).offset(skip).limit(limit).all()

def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

def get_user_plans(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Plan).filter(models.Plan.profile_id == user_id).offset(skip).limit(limit).all()

def create_user_plan(db: Session, plan: schemas.PlanCreate, user_id: int):
    db_plan = models.Plan(**plan.dict(), profile_id=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# Macrocycle
def get_macrocycles(db: Session, plan_id: int, skip: int = 0, limit: int = 100):
   return db.query(models.Macrocycle).filter(models.Macrocycle.plan_id == plan_id).offset(skip).limit(limit).all()

def get_macrocycle(db: Session, macrocycle_id: int):
    return db.query(models.Macrocycle).filter(models.Macrocycle.id == macrocycle_id).first()

def create_plan_macrocycle(db: Session, macrocycle: schemas.MacrocycleCreate, plan_id: int):
    db_macrocycle = models.Macrocycle(**macrocycle.dict(), plan_id=plan_id)
    db.add(db_macrocycle)
    db.commit()
    db.refresh(db_macrocycle)
    return db_macrocycle

# Microcycle
def get_microcycles(db: Session, macrocycle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Microcycle).filter(models.Microcycle.macrocycle_id == macrocycle_id).offset(skip).limit(limit).all()

def get_microcycle(db: Session, microcycle_id: int):
    return db.query(models.Microcycle).filter(models.Microcycle.id == microcycle_id).first()

def create_macrocycle_microcycle(db: Session, microcycle: schemas.MicrocycleCreate, macrocycle_id: int):
    db_microcycle = models.Microcycle(**microcycle.dict(), macrocycle_id=macrocycle_id)
    db.add(db_microcycle)
    db.commit()
    db.refresh(db_microcycle)
    return db_microcycle

# Session
def get_sessions(db: Session, microcycle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Session).filter(models.Session.microcycle_id == microcycle_id).offset(skip).limit(limit).all()

def create_microcycle_session(db: Session, session: schemas.SessionCreate, microcycle_id: int):
    db_session = models.Session(**session.dict(), microcycle_id=microcycle_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

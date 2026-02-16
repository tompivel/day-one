from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_user = crud.get_profile_by_username(db, username=profile.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_profile(db=db, profile=profile)

@router.get("/me", response_model=schemas.Profile)
def read_users_me(current_user: models.Profile = Depends(auth.get_current_user)):
    return current_user

@router.get("/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_profile(db, profile_id=profile_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/by-username/{username}", response_model=schemas.Profile)
def read_profile_by_username(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_profile_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

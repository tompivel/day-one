from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Plan)
def create_plan(
    plan: schemas.PlanCreate, 
    db: Session = Depends(get_db), 
    current_user: models.Profile = Depends(auth.get_current_user)
):
    return crud.create_user_plan(db=db, plan=plan, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Plan])
def read_plans(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.Profile = Depends(auth.get_current_user)
):
    # Filter plans by current user
    return crud.get_user_plans(db, user_id=current_user.id, skip=skip, limit=limit)

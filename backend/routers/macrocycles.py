from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/macrocycles",
    tags=["macrocycles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{plan_id}/", response_model=schemas.Macrocycle)
def create_macrocycle_for_plan(
    plan_id: int, 
    macrocycle: schemas.MacrocycleCreate, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    plan = crud.get_plan(db, plan_id=plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    if plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this plan")
    return crud.create_plan_macrocycle(db=db, macrocycle=macrocycle, plan_id=plan_id)

@router.get("/{plan_id}/", response_model=List[schemas.Macrocycle])
def read_macrocycles(
    plan_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    plan = crud.get_plan(db, plan_id=plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    if plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this plan")
    macrocycles = crud.get_macrocycles(db, plan_id=plan_id, skip=skip, limit=limit)
    return macrocycles

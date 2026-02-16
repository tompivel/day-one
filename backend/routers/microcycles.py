from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/microcycles",
    tags=["microcycles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{macrocycle_id}/", response_model=schemas.Microcycle)
def create_microcycle_for_macrocycle(
    macrocycle_id: int, 
    microcycle: schemas.MicrocycleCreate, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    macrocycle = crud.get_macrocycle(db, macrocycle_id=macrocycle_id)
    if not macrocycle:
        raise HTTPException(status_code=404, detail="Macrocycle not found")
    # Check hierarchy: Macrocycle -> Plan -> Profile
    if macrocycle.plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this macrocycle")
        
    return crud.create_macrocycle_microcycle(db=db, microcycle=microcycle, macrocycle_id=macrocycle_id)

@router.get("/{macrocycle_id}/", response_model=List[schemas.Microcycle])
def read_microcycles(
    macrocycle_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    macrocycle = crud.get_macrocycle(db, macrocycle_id=macrocycle_id)
    if not macrocycle:
        raise HTTPException(status_code=404, detail="Macrocycle not found")
    if macrocycle.plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this macrocycle")
        
    microcycles = crud.get_microcycles(db, macrocycle_id=macrocycle_id, skip=skip, limit=limit)
    return microcycles

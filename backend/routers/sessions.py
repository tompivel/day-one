from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/{microcycle_id}/", response_model=schemas.Session)
def create_session_for_microcycle(
    microcycle_id: int, 
    session: schemas.SessionCreate, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    microcycle = crud.get_microcycle(db, microcycle_id=microcycle_id)
    if not microcycle:
        raise HTTPException(status_code=404, detail="Microcycle not found")
    # Check hierarchy: Microcycle -> Macrocycle -> Plan -> Profile
    if microcycle.macrocycle.plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this microcycle")
        
    return crud.create_microcycle_session(db=db, session=session, microcycle_id=microcycle_id)

@router.get("/{microcycle_id}/", response_model=List[schemas.Session])
def read_sessions(
    microcycle_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Profile = Depends(auth.get_current_user)
):
    microcycle = crud.get_microcycle(db, microcycle_id=microcycle_id)
    if not microcycle:
        raise HTTPException(status_code=404, detail="Microcycle not found")
    if microcycle.macrocycle.plan.profile_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this microcycle")
        
    sessions = crud.get_sessions(db, microcycle_id=microcycle_id, skip=skip, limit=limit)
    return sessions

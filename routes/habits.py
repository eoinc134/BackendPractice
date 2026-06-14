from fastapi import APIRouter, HTTPException
import logging
from db.database import SessionDep
from sqlmodel import select

from db.models import Habit, HabitCreate, HabitRead, HabitUpdate

# Router Setup
router = APIRouter(prefix='/habits', tags=['habits'])
logger = logging.getLogger(__name__)

# GET habits
@router.get('/', response_model=list[HabitRead])
def get_habits(session: SessionDep) -> list[Habit]:
    logger.info("Fetching all habits")
    return session.exec(select(Habit)).all()

# GET habit by ID
@router.get('/{id}', response_model=HabitRead)
def get_habit(id: int, session: SessionDep) -> Habit:
    logger.info(f"Fetching habit with ID: {id}")
    habit = session.get(Habit, id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    return habit

# POST habits
@router.post('/', response_model=HabitRead)
def create_habit(habit: HabitCreate, session: SessionDep) -> Habit:
    logger.info(f"Creating habit: {habit.name}")
    db_habit = Habit.model_validate(habit)
    
    session.add(db_habit)
    
    session.commit()
    session.refresh(db_habit)
    
    return db_habit

# PATCH habits
@router.patch('/{id}', response_model=HabitRead)
def update_habit(id: int, habit: HabitUpdate, session: SessionDep) -> Habit:
    logger.info(f"Updating habit with ID: {id}")
    db_habit = session.get(Habit, id)
    
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    updates = habit.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(db_habit, key, value)

    session.commit()
    session.refresh(db_habit)
    
    return db_habit

# DELETE habits
@router.delete('/{id}')
def delete_habit(id: int, session: SessionDep):
    logger.info(f"Deleting habit with ID: {id}")
    habit = session.get(Habit, id)
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    session.delete(habit)
    session.commit()
    
    return {"message": "Habit deleted successfully"}
from fastapi import APIRouter, HTTPException
import logging
from models.habit import Habit

router = APIRouter(prefix='/habits', tags=['habits'])
logger = logging.getLogger(__name__)

habits: list[Habit] = [
    Habit(id=1, name="Exercise", frequency="Daily"),
    Habit(id=2, name="Read", frequency="Daily"),
    Habit(id=3, name="Meditate", frequency="Daily"),
    Habit(id=4, name="Drink Water", frequency="Daily"),
    Habit(id=5, name="Sleep Early", frequency="Daily"),
]

@router.get('/habits')
def get_habits() -> list[Habit]:
    logger.info("Fetching all habits")
    return habits

@router.get('/habits/{id}')
def get_habit(id: int) -> Habit:
    logger.info(f"Fetching habit with ID: {id}")
    for habit in habits:
        if habit.id == id:
            return habit
    raise HTTPException(status_code=404, detail="Habit not found")

@router.post('/habits')
def create_habit(habit: Habit) -> Habit:
    logger.info(f"Creating habit: {habit.name}")
    habit.id = habits[-1].id + 1 if habits else 1
    habits.append(habit)
    return habit

@router.patch('/habits/{id}')
def update_habit(id: int, habit: Habit) -> Habit:
    logger.info(f"Updating habit with ID: {id}")
    for h in habits:
        if h.id == id:
            h = habit
            return h
    raise HTTPException(status_code=404, detail="Habit not found")

@router.delete('/habits/{id}')
def delete_habit(id: int):
    logger.info(f"Deleting habit with ID: {id}")
    for h in habits:
        if h.id == id:
            habits.remove(h)
            return {"message": "Habit deleted"}
    raise HTTPException(status_code=404, detail="Habit not found")
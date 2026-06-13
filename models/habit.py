from pydantic import BaseModel

class Habit(BaseModel):
    id: int
    name: str
    frequency: str
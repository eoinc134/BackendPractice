from sqlmodel import SQLModel, Field

# USER model
class UserBase(SQLModel):
    name: str
    email: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    disabled: bool = False
    
class UserRead(UserBase):
    id: int
    name: str
    email: str
    username: str
    
# TOKEN model
class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str | None = None

# HABIT model
class HabitBase(SQLModel):
    name: str
    frequency: str
    
class Habit(HabitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
class HabitCreate(HabitBase):
    user_id: int
    
class HabitRead(HabitBase):
    id: int
    user_id: int
    
class HabitUpdate(HabitBase):
    name: str | None = None
    frequency: str | None = None

# COMPLETION model  
class Completion(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habit.id")
    completed_at: str
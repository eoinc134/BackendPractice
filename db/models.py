from sqlmodel import SQLModel, Field

# USER model
class UserBase(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=100)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=50)
    hashed_password: str = Field(min_length=6, max_length=100)
    disabled: bool = False
    profile_picture: str | None = None 
    
class UserCreate(UserBase):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)

class UserRead(UserBase):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    profile_picture: str | None = None  
    username: str = Field(min_length=3, max_length=50)
    
# TOKEN model
class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str | None = None

# HABIT model
class HabitBase(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    frequency: str = Field(min_length=2, max_length=50)  # e.g., "daily", "weekly", etc.
    
class Habit(HabitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
class HabitCreate(HabitBase):
    user_id: int = Field(foreign_key="user.id")  # Ensure user_id is provided when creating a habit
    
class HabitRead(HabitBase):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
class HabitUpdate(HabitBase):
    name: str | None = None
    frequency: str | None = None

# COMPLETION model  
class Completion(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habit.id")
    completed_at: str = Field(default=None)  # Store completion timestamp as a string (ISO format)
from fastapi import FastAPI

app = FastAPI()

habits = [
    {"id": 1, "name": "Exercise", "frequency": "Daily"},
    {"id": 2, "name": "Read", "frequency": "Daily"},
    {"id": 3, "name": "Meditate", "frequency": "Daily"},
    {"id": 4, "name": "Drink Water", "frequency": "Daily"},
    {"id": 5, "name": "Sleep Early", "frequency": "Daily"},
]

@app.get('/')
def root():
    return {"message": "Hello World!"}

@app.get('/habits')
def get_habits():
    return habits

@app.get('/habits/{id}')
def get_habit(id: int):
    for habit in habits:
        if habit["id"] == id:
            return habit
    return {"message": "Habit not found"}

@app.post('/habits')
def create_habit(habit: dict):
    habit['id'] = habits[-1]['id'] + 1 if habits else 1
    habits.append(habit)
    return habit

@app.patch('habits/{id}')
def update_habit(id: int, habit: dict):
    for h in habits:
        if h['id'] == id:
            h.update(habit)
            return h
    return {"message": "Habit not found"}

@app.delete('habits/{id}')
def delete_habit(id: int):
    for h in habits:
        if h['id'] == id:
            habits.remove(h)
            return {'message': 'Habit deleted'}
    return {"message": "Habit not found"}

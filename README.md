# Backend Roadmap Practice

Following along with **The Ultimate Backend Roadmap** and documenting my progress as I build and improve backend projects.

This repository contains the code, notes, and exercises I complete throughout the roadmap. New features, technologies, and projects will be added as I progress.

## Goal

Learn backend development by building real projects and applying concepts as they are introduced.

## Project: Habits API

A REST API for managing habits, built with FastAPI.

### Structure

```
BackendPractice/
├── main.py              # App init, global error handler, router registration
├── routes/
│   ├── habits.py        # All /habits endpoints using APIRouter
│   └── user.py          # Auth endpoints and JWT helper functions
├── db/
│   ├── database.py      # Engine, session, SessionDep dependency
│   └── models.py        # SQLModel table definitions and schemas
└── .env                 # DATABASE_URL, SECRET_KEY, ALGORITHM (not committed)
```

### Features

- Route organisation with `APIRouter` and prefix/tag grouping
- SQLModel for database models with separate `Create`, `Read`, and `Update` schemas
- SQLite database via SQLAlchemy, configured through `DATABASE_URL` in `.env`
- Request validation via Pydantic/SQLModel (automatic 422 on bad input)
- Proper HTTP error responses using `HTTPException` (404 for missing resources)
- JWT authentication with `python-jose`, token issued at `/users/token`
- Password hashing with `pwdlib`
- Protected routes via `OAuth2PasswordBearer` dependency
- Structured logging with `logging.getLogger(__name__)` per module
- Global exception handler for unexpected server errors

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/users/token` | No | Login and receive a JWT |
| GET | `/users/current` | Yes | Get the current logged-in user |
| GET | `/habits/` | Yes | List all habits |
| GET | `/habits/{id}` | Yes | Get a single habit by ID |
| POST | `/habits/` | Yes | Create a new habit |
| PATCH | `/habits/{id}` | Yes | Update an existing habit |
| DELETE | `/habits/{id}` | Yes | Delete a habit |


## Progress

* [x] Getting started
* [x] FastAPI basics — routing, path parameters, request body
* [x] Project structure — routers and models split into separate modules
* [x] Validation — Pydantic models replacing raw `dict` parameters
* [x] Error handling — `HTTPException` and a global exception handler
* [x] Logging — per-module loggers with `logging.getLogger(__name__)`
* [x] Database — SQLite with SQLModel, environment-based config via `.env`
* [x] Authentication — JWT-based auth with password hashing and protected routes
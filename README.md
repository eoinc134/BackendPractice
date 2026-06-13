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
│   └── habits.py        # All /habits endpoints using APIRouter
└── models/
    └── habit.py         # Pydantic model for request/response validation
```

### Features

- Route organisation with `APIRouter` and prefix/tag grouping
- Request validation via Pydantic models (automatic 422 on bad input)
- Proper HTTP error responses using `HTTPException` (404 for missing habits)
- Structured logging with `logging.getLogger(__name__)` per module
- Global exception handler for unexpected server errors

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/habits` | List all habits |
| GET | `/habits/{id}` | Get a single habit by ID |
| POST | `/habits` | Create a new habit |
| PATCH | `/habits/{id}` | Update an existing habit |
| DELETE | `/habits/{id}` | Delete a habit |

## Progress

* [x] Getting started
* [x] FastAPI basics — routing, path parameters, request body
* [x] Project structure — routers and models split into separate modules
* [x] Validation — Pydantic models replacing raw `dict` parameters
* [x] Error handling — `HTTPException` and a global exception handler
* [x] Logging — per-module loggers with `logging.getLogger(__name__)`

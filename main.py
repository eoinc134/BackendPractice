import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routes.habits import habits_router
from routes.user import user_router
from db.database import create_db_and_tables

# Application Setup
app = FastAPI()
app.include_router(habits_router)
app.include_router(user_router)
logger = logging.getLogger(__name__)

# Startup Event
@app.on_event("startup")
def startup_event():
    logger.info("Application startup: Logging is configured.")
    create_db_and_tables()  # Ensure the database and tables are created on startup

# Global Exception Handler
@app.exception_handler(Exception)
def exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
    )
    
@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request, exc):
    logger.warning(f"Request validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"message": "Invalid request data."},
    )
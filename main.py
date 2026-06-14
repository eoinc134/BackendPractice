import logging

from fastapi import FastAPI

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
    logger.error(f"An error occurred: {exc}")
    return {"message": "An error occurred", "details": str(exc)}
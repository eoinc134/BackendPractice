import logging

from fastapi import FastAPI
from routes.habits import router

app = FastAPI()
app.include_router(router)
logger = logging.getLogger(__name__)
logger.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.exception_handler(Exception)
def exception_handler(request, exc):
    logger.error(f"An error occurred: {exc}")
    return {"message": "An error occurred", "details": str(exc)}
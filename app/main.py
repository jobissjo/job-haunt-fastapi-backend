from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import db as _db
from app.routes import router
from app.settings import settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS.split(","),
    allow_headers=settings.CORS_HEADERS.split(","),
)

app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to Job Haunt Backend", "success": True}

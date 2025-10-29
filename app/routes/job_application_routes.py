from fastapi import APIRouter

from app.services.job_application_service import JobApplicationService

router = APIRouter(prefix="/job_applications", tags=["Job Applications"])

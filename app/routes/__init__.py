from fastapi import APIRouter

from .job_application_routes import router as job_application_router
from .job_skills import router as job_skills_router
from .user_routes import router as user_router
from .job_statuses import router as job_statuses_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(user_router)
router.include_router(job_application_router)
router.include_router(job_skills_router)
router.include_router(job_statuses_router)
router.include_router(admin_router)

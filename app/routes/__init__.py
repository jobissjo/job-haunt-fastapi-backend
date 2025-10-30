from fastapi import APIRouter

from .admin import router as admin_router
from .job_application_routes import router as job_application_router
from .job_skills import router as job_skills_router
from .job_statuses import router as job_statuses_router
from .learning_plans import router as learning_plans_router
from .learning_resource import router as learning_resource_router
from .learning_statuses import router as learning_status_router
from .user_routes import router as user_router
from .user_skills import router as user_skills_router
from .notification_preference import router as notification_preference_router
from .user_email_settings import router as user_email_settings_router

router = APIRouter()
router.include_router(user_router)
router.include_router(job_application_router)
router.include_router(job_skills_router)
router.include_router(job_statuses_router)
router.include_router(admin_router)
router.include_router(learning_plans_router)
router.include_router(learning_status_router)
router.include_router(user_skills_router)
router.include_router(learning_resource_router)
router.include_router(notification_preference_router)
router.include_router(user_email_settings_router)

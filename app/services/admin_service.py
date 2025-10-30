from app.repositories.job_skills import JobSkillRepository
from app.repositories.job_status_repository import JobStatusRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin_schema import AdminStats, AdminStatsResponse


class AdminService:
    def __init__(self):
        self.User_repository = UserRepository()
        self.JobSkillRepository = JobSkillRepository()
        self.JobStatusRepository = JobStatusRepository()

    async def get_stats(self) -> AdminStatsResponse:
        users_count = await self.User_repository.get_users_count()
        job_skills_count = await self.JobSkillRepository.get_job_skills_count()
        job_statuses_count = await self.JobStatusRepository.get_job_status_count()
        admin_stats = AdminStats(
            **{
                "total_users": users_count,
                "total_skills": job_skills_count,
                "total_statuses": job_statuses_count or 0,
                "recent_activity": 0,
            }
        )
        return AdminStatsResponse(
            data=admin_stats, success=True, message="Admin stats retrieved successfully"
        )

from app.repositories.job_application_repository import JobApplicationRepository
from app.schemas.job_application import JobApplication


class JobApplicationService:
    def __init__(self):
        self.repository = JobApplicationRepository()

    async def create_job_application(self, job_application: JobApplication):
        return await self.repository.create_job_application(job_application)

    async def get_job_applications(self):
        return await self.repository.get_job_applications()

    async def get_job_application_by_id(self, job_application_id):
        return await self.repository.get_job_application_by_id(job_application_id)

    async def update_job_application(self, job_application_id, job_application):
        return await self.repository.update_job_application(
            job_application_id, job_application
        )

    async def delete_job_application(self, job_application_id):
        return await self.repository.delete_job_application(job_application_id)

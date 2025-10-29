from app.repositories.job_statuses import JobStatusRepository
from app.schemas.job_status import JobStatusSchema


class JobStatusService:
    def __init__(self):
        self.repository = JobStatusRepository()

    async def get_job_statuses(self):
        return await self.repository.get_job_statuses()

    async def get_job_status_by_id(self, job_status_id):
        return await self.repository.get_job_status_by_id(job_status_id)

    async def create_job_status(self, job_status: JobStatusSchema):
        return await self.repository.create_job_status(job_status)

    async def update_job_status(self, job_status_id, job_status: JobStatusSchema):
        return await self.repository.update_job_status(job_status_id, job_status)

    async def delete_job_status(self, job_status_id: JobStatusSchema):
        return await self.repository.delete_job_status(job_status_id)

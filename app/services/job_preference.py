from app.repositories.job_preference import JobPreferenceRepository
from app.schemas.job_preference import JobPreferenceSchemaCreate, JobPreferenceDetailResponse
from app.services.common import CommonService
from app.schemas.common import BaseResponseSchema
from fastapi import HTTPException

class JobPreferenceService:
    def __init__(self):
        self.repository = JobPreferenceRepository()
    
    async def create_job_preference(self, job_preference: JobPreferenceSchemaCreate, user_id: str)->BaseResponseSchema:
        await self.repository.create_job_preference(job_preference, user_id)
        return {"message": "Job preference created successfully", "success": True}
    
    async def get_job_preference_by_user_id(self, user_id: str):
        data = await self.repository.get_job_preference_by_user_id(user_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Job preference not found")
        return {"data": data, "message": "Job preference fetched successfully", "success": True}
    
    async def update_job_preference(self, job_preference: JobPreferenceSchemaCreate, user_id: str)->BaseResponseSchema:
        await self.repository.update_job_preference(job_preference, user_id)
        return {"message": "Job preference updated successfully", "success": True}
    
   

from app.database import db
from app.schemas.job_application_automation import (
    JobApplicationAutomationResponse,
    JobApplicationAutomationSchema,
)
from bson.objectid import ObjectId
class JobApplicationAutomationRepository:
    def __init__(self):
        self.collection = db.job_application_automation

    async def get_job_application_automation_by_id(
        self, job_application: str
    ) -> JobApplicationAutomationResponse:
        return await self.collection.find_one(
            {"job_application": ObjectId(job_application)}
        )
    
    async def create_job_application_automation(
        self, job_application_automation: JobApplicationAutomationSchema, user_id: str
    ) -> None:
        result =await self.collection.insert_one(
            {**job_application_automation.model_dump(), "user_id": ObjectId(user_id),
            "job_application": ObjectId(job_application_automation.job_application)}
        )
        return result.inserted_id
    
    async def update_job_application_automation(
        self, job_application_automation_id: str, job_application_automation: JobApplicationAutomationSchema
    ) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(job_application_automation_id)},
            {"$set": job_application_automation.model_dump()},
        )
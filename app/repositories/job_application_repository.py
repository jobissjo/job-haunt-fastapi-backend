from bson import ObjectId

from app.database import db
from app.schemas.job_application import JobApplicationSchema


class JobApplicationRepository:
    def __init__(self):
        self.collection = db.job_applications

    async def create_job_application(self, job_application: JobApplicationSchema, user_id:str):
        await self.collection.insert_one({
            **job_application.model_dump(),
            "user_id": ObjectId(user_id),
            'status' : ObjectId(job_application.status),
            "skills": [ObjectId(skill) for skill in job_application.skills],
            "preferred_skills": [ObjectId(skill) for skill in job_application.preferred_skills],
            'application_url': str(job_application.application_url)
        })

    async def get_job_applications(self, user_id: str) -> list[JobApplicationSchema]:
        documents = []
        async for document in self.collection.find({"user_id": ObjectId(user_id)}):
            # Convert top-level ObjectIds to strings
            document["_id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            
            # Convert status ObjectId to string if present
            if "status" in document and isinstance(document["status"], ObjectId):
                document["status"] = str(document["status"])
            
            # Convert list of ObjectIds (skills)
            if "skills" in document and isinstance(document["skills"], list):
                document["skills"] = [
                    str(skill) if isinstance(skill, ObjectId) else skill
                    for skill in document["skills"]
                ]
            
            # Convert list of ObjectIds (preferred_skills)
            if "preferred_skills" in document and isinstance(document["preferred_skills"], list):
                document["preferred_skills"] = [
                    str(skill) if isinstance(skill, ObjectId) else skill
                    for skill in document["preferred_skills"]
                ]
            
            documents.append(document)
        
        return documents

    async def get_job_application_by_id(self, job_application_id: str):
        job_application_response = await self.collection.find_one(
            {"_id": ObjectId(job_application_id)}
        )
        job_application_response["_id"] = str(job_application_response["_id"])
        return job_application_response

    async def update_job_application(
        self, job_application_id: str, job_application: JobApplicationSchema
    ):
        job_application_response = await self.collection.update_one(
            {"_id": ObjectId(job_application_id)}, {"$set": job_application}
        )
        job_application_response["_id"] = str(job_application_response["_id"])
        return job_application_response

    async def delete_job_application(self, job_application_id: str):
        return await self.collection.delete_one({"_id": ObjectId(job_application_id)})

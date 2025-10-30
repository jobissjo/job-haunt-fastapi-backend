from bson.objectid import ObjectId

from app.database import db
from app.schemas.job_skill import JobSkillResponse, JobSkillSchema


class JobSkillRepository:
    def __init__(self):
        self.collection = db.job_skills

    async def create_job_skill(self, job_skill: JobSkillSchema):
        return await self.collection.insert_one(job_skill.model_dump())

    async def get_job_skills(self) -> list[JobSkillResponse]:
        documents = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents
    
    async def get_job_skills_count(self):
        return await self.collection.count_documents({})

    async def get_job_skill_by_id(self, job_skill_id) -> JobSkillResponse:
        job_skill_response = await self.collection.find_one(
            {"_id": ObjectId(job_skill_id)}
        )
        job_skill_response["_id"] = str(job_skill_response["_id"])
        return job_skill_response

    async def update_job_skill(self, job_skill_id, job_skill:JobSkillSchema)->None:
        await self.collection.update_one(
            {"_id": ObjectId(job_skill_id)}, {"$set": job_skill.model_dump()}
        )
        
    async def delete_job_skill(self, job_skill_id):
        return await self.collection.delete_one({"_id": ObjectId(job_skill_id)})

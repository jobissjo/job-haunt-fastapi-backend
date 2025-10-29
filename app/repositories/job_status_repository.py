from bson.objectid import ObjectId

from app.database import db
from app.schemas.job_status import BaseJobStatus, JobStatusResponse


class JobStatusRepository:
    def __init__(self):
        self.collection = db.job_status

    async def create_job_status(self, job_status: BaseJobStatus):
        await self.collection.insert_one(job_status.model_dump())

    async def get_job_status(self) -> list[JobStatusResponse]:
        documents = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents
    
    async def get_job_status_count(self):
        return await self.collection.count_documents({})

    async def get_job_status_by_id(self, job_status_id: str) -> JobStatusResponse:
        job_status_response = await self.collection.find_one(
            {"_id": ObjectId(job_status_id)}
        )
        job_status_response["_id"] = str(job_status_response["_id"])
        return job_status_response

    async def update_job_status(
        self, job_status_id: str, job_status: BaseJobStatus
    ) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(job_status_id)}, {"$set": job_status.model_dump()}
        )
        

    async def delete_job_status(self, job_status_id: str):
        await self.collection.delete_one({"_id": ObjectId(job_status_id)})

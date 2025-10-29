from app.schemas.job_application import JobApplication


class JobApplicationRepository:
    def __init__(self):
        self.collection = db.job_applications

    async def create_job_application(self, job_application: JobApplication):
        return await self.collection.insert_one(job_application)

    async def get_job_applications(self, user_id: str) -> list[JobApplication]:
        documents = []
        async for document in self.collection.find({"user_id": user_id}):
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_job_application_by_id(self, job_application_id: str):
        job_application_response = await self.collection.find_one(
            {"_id": ObjectId(job_application_id)}
        )
        job_application_response["_id"] = str(job_application_response["_id"])
        return job_application_response

    async def update_job_application(
        self, job_application_id: str, job_application: JobApplication
    ):
        job_application_response = await self.collection.update_one(
            {"_id": ObjectId(job_application_id)}, {"$set": job_application}
        )
        job_application_response["_id"] = str(job_application_response["_id"])
        return job_application_response

    async def delete_job_application(self, job_application_id: str):
        return await self.collection.delete_one({"_id": ObjectId(job_application_id)})

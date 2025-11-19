from bson import ObjectId

from app.database import db
from app.schemas.job_application import JobApplicationSchema, JobApplicationResponse


class JobApplicationRepository:
    def __init__(self):
        self.collection = db.job_applications

    async def create_job_application(
        self, job_application: JobApplicationSchema, user_id: str
    ):
        result = await self.collection.insert_one(
            {
                **job_application.model_dump(),
                "user_id": ObjectId(user_id),
                "status": ObjectId(job_application.status),
                "skills": [ObjectId(skill) for skill in job_application.skills],
                "preferred_skills": [
                    ObjectId(skill) for skill in job_application.preferred_skills
                ],
                "application_url": str(job_application.application_url),
            }
        )
        return result.inserted_id

    async def get_job_applications(self, user_id: str) -> list[dict]:
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            # Lookup for status
            {
                "$lookup": {
                    "from": "job_status",
                    "localField": "status",
                    "foreignField": "_id",
                    "as": "status_detail",
                }
            },
            {"$unwind": {"path": "$status_detail", "preserveNullAndEmptyArrays": True}},
            # Lookup for skills
            {
                "$lookup": {
                    "from": "job_skills",
                    "localField": "skills",
                    "foreignField": "_id",
                    "as": "skills_detail",
                }
            },
            # Lookup for preferred skills
            {
                "$lookup": {
                    "from": "job_skills",
                    "localField": "preferred_skills",
                    "foreignField": "_id",
                    "as": "preferred_skills_detail",
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        documents = []
        async for doc in cursor:
            # Convert ObjectIds to strings
            doc["_id"] = str(doc["_id"])
            doc["user_id"] = str(doc["user_id"])

            if "status" in doc and isinstance(doc["status"], ObjectId):
                doc["status"] = str(doc["status"])

            if "skills" in doc:
                doc["skills"] = [str(s) for s in doc["skills"]]

            if "preferred_skills" in doc:
                doc["preferred_skills"] = [str(s) for s in doc["preferred_skills"]]

            # Convert nested details’ _id to string
            if "status_detail" in doc and doc["status_detail"]:
                doc["status_detail"]["_id"] = str(doc["status_detail"]["_id"])

            if "skills_detail" in doc:
                for s in doc["skills_detail"]:
                    s["_id"] = str(s["_id"])

            if "preferred_skills_detail" in doc:
                for s in doc["preferred_skills_detail"]:
                    s["_id"] = str(s["_id"])

            documents.append(doc)

        return documents

    async def get_job_application_by_id(
        self, job_application_id: str, user_id: str
    ) -> JobApplicationResponse | None:
        pipeline = [
            {"$match": {"_id": ObjectId(job_application_id), "user_id": ObjectId(user_id)}},
            # Lookup for status
            {
                "$lookup": {
                    "from": "job_status",
                    "localField": "status",
                    "foreignField": "_id",
                    "as": "status_detail",
                }
            },
            {"$unwind": {"path": "$status_detail", "preserveNullAndEmptyArrays": True}},
            # Lookup for skills
            {
                "$lookup": {
                    "from": "job_skills",
                    "localField": "skills",
                    "foreignField": "_id",
                    "as": "skills_detail",
                }
            },
            # Lookup for preferred skills
            {
                "$lookup": {
                    "from": "job_skills",
                    "localField": "preferred_skills",
                    "foreignField": "_id",
                    "as": "preferred_skills_detail",
                }
            },
        ]

        cursor = await self.collection.aggregate(pipeline)
        job_application = await cursor.to_list(length=1)

        if not job_application:
            return None

        doc = job_application[0]

        # Convert ObjectIds to strings
        doc["_id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])

        if "status" in doc and isinstance(doc["status"], ObjectId):
            doc["status"] = str(doc["status"])

        if "skills" in doc:
            doc["skills"] = [str(s) for s in doc["skills"]]

        if "preferred_skills" in doc:
            doc["preferred_skills"] = [str(s) for s in doc["preferred_skills"]]

        # Convert nested details
        if "status_detail" in doc and doc["status_detail"]:
            print(doc["status_detail"])
            doc["status_detail"]["_id"] = str(doc["status_detail"]["_id"])

        if "skills_detail" in doc:
            for s in doc["skills_detail"]:
                s["_id"] = str(s["_id"])

        if "preferred_skills_detail" in doc:
            for s in doc["preferred_skills_detail"]:
                s["_id"] = str(s["_id"])

        return JobApplicationResponse(**doc)

    async def update_job_application(
        self, job_application_id: str, job_application: JobApplicationSchema,
        user_id: str
    ):
        await self.collection.update_one(
            {"_id": ObjectId(job_application_id), "user_id": ObjectId(user_id)},
            {
                "$set": {
                    **job_application.model_dump(),
                    "skills": [ObjectId(skill) for skill in job_application.skills],
                    "preferred_skills": [
                        ObjectId(skill) for skill in job_application.preferred_skills
                    ],
                    "application_url": str(job_application.application_url),
                }
            },
        )

    async def delete_job_application(self, job_application_id: str, user_id: str):
        return await self.collection.delete_one({"_id": ObjectId(job_application_id), "user_id": ObjectId(user_id)})

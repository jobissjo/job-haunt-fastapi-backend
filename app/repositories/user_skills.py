from bson import ObjectId

from app.database import db
from app.schemas.user_skills import UserSkillResponse, UserSkillSchema


class UserSkillRepository:
    def __init__(self):
        self.collection = db.user_skills

    async def create_user_skill(
        self, user_skill: UserSkillSchema, user_id: str
    ) -> UserSkillResponse:
        return await self.collection.insert_one(
            {
                **user_skill.model_dump(),
                "user_id": ObjectId(user_id),
                "skill_id": ObjectId(user_skill.skill),
            }
        )

    async def get_user_skills(self, user_id: str) -> list[UserSkillResponse]:
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": "job_skills",
                    "localField": "skill_id",
                    "foreignField": "_id",
                    "as": "skill_detail",
                }
            },
            {"$unwind": "$skill_detail"},
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"},
                    "user_id": {"$toString": "$user_id"},
                    "skill_id": {"$toString": "$skill_id"},
                    "skill_detail._id": {"$toString": "$skill_detail._id"},
                }
            },
        ]
        documents = []
        cursor = await self.collection.aggregate(pipeline)
        async for document in cursor:
            document["_id"] = str(document["_id"])
            documents.append(document)
        print(documents, "documents")
        return documents

    async def get_user_skill_by_id(self, user_skill_id: str) -> UserSkillResponse:
        user_skill_response = await self.collection.find_one(
            {"_id": ObjectId(user_skill_id)}
        )
        user_skill_response["_id"] = str(user_skill_response["_id"])
        return user_skill_response

    async def update_user_skill(
        self, user_skill_id: str, user_skill: UserSkillSchema
    ) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(user_skill_id)}, {"$set": user_skill.model_dump()}
        )
        

    async def delete_user_skill(self, user_skill_id: str) -> None:
        await self.collection.delete_one({"_id": ObjectId(user_skill_id)})

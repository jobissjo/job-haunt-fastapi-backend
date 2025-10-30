from bson import ObjectId

from app.database import db
from app.schemas.learning_plan import LearningPlanResponse, LearningPlanSchema


class LearningPlanRepository:
    def __init__(self):
        self.collection = db.learning_plans

    async def create_learning_plan(self, learning_plan:LearningPlanSchema)->None:
        await self.collection.insert_one(learning_plan.model_dump())

    async def get_learning_plans(self, user_id: str)->list[LearningPlanResponse]:
        documents = []
        async for document in self.collection.find({"user_id": user_id}):
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_learning_plan_by_id(self, learning_plan_id)->LearningPlanResponse:
        learning_plan_response = await self.collection.find_one(
            {"_id": ObjectId(learning_plan_id)}
        )
        learning_plan_response["_id"] = str(learning_plan_response["_id"])
        return learning_plan_response

    async def update_learning_plan(self, learning_plan_id, learning_plan:LearningPlanSchema)->None:
        await self.collection.update_one(
            {"_id": ObjectId(learning_plan_id)}, {"$set": learning_plan.model_dump()}
        )
        return await self.get_learning_plan_by_id(learning_plan_id)

    async def delete_learning_plan(self, learning_plan_id)->None:
        await self.collection.delete_one({"_id": ObjectId(learning_plan_id)})

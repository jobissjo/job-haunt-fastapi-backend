from bson.objectid import ObjectId

from app.database import db
from app.schemas.learning_status import LearningStatus, LearningStatusResponse


class LearningStatusRepository:
    def __init__(self):
        self.collection = db.learning_status

    async def create_learning_status(
        self, learning_status: LearningStatus
    ) -> LearningStatusResponse:
        return await self.collection.insert_one(learning_status)

    async def get_learning_status(self) -> list[LearningStatusResponse]:
        documents = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_learning_status_by_id(
        self, learning_status_id: str
    ) -> LearningStatusResponse:
        learning_status_response = await self.collection.find_one(
            {"_id": ObjectId(learning_status_id)}
        )
        learning_status_response["_id"] = str(learning_status_response["_id"])
        return learning_status_response

    async def update_learning_status(
        self, learning_status_id: str, learning_status: LearningStatus
    ) -> LearningStatusResponse:
        learning_status_response = await self.collection.update_one(
            {"_id": ObjectId(learning_status_id)}, {"$set": learning_status}
        )
        learning_status_response["_id"] = str(learning_status_response["_id"])
        return learning_status_response

    async def delete_learning_status(self, learning_status_id: str):
        return await self.collection.delete_one({"_id": ObjectId(learning_status_id)})

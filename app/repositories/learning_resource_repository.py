from bson.objectid import ObjectId
from typing import Optional

from app.database import db
from app.schemas.learning_resource import LearningResource, LearningResourceResponse


class LearningResourceRepository:
    def __init__(self):
        self.collection = db.learning_resources

    async def create_learning_resource(
        self, learning_resource: LearningResource, user_id
    ):
        await self.collection.insert_one(
            {
                **learning_resource.model_dump(),
                "learning_management": ObjectId(learning_resource.learning_management),
                "status": ObjectId(learning_resource.status),
                "user_id": ObjectId(user_id),
            }
        )

    async def get_learning_resources(
        self, user_id: str, learning_management_id: str = None
    ) -> list[LearningResourceResponse]:
        documents = []
        filters = {"user_id": ObjectId(user_id)}
        if learning_management_id:
            filters["learning_management"] = ObjectId(learning_management_id)
        async for document in self.collection.find(filters):
            document["_id"] = str(document["_id"])
            document["learning_management"] = str(document["learning_management"])
            document["status"] = str(document["status"])
            document["user_id"] = str(document["user_id"])
            documents.append(document)
        return documents

    async def get_learning_resource_by_id(
        self, learning_resource_id: str
    ) -> Optional[LearningResourceResponse]:
        learning_resource_response = await self.collection.find_one(
            {"_id": ObjectId(learning_resource_id)}
        )
        if not learning_resource_response:
            return None
        learning_resource_response["_id"] = str(learning_resource_response["_id"])
        learning_resource_response["learning_management"] = str(
            learning_resource_response["learning_management"]
        )
        learning_resource_response["status"] = str(learning_resource_response["status"])
        learning_resource_response["user_id"] = str(learning_resource_response["user_id"])
        return learning_resource_response

    async def update_learning_resource(
        self, learning_resource_id: str, learning_resource: LearningResource
    ) -> LearningResourceResponse:
        learning_resource_response = await self.collection.update_one(
            {"_id": ObjectId(learning_resource_id)}, {"$set": learning_resource}
        )
        learning_resource_response["_id"] = str(learning_resource_response["_id"])
        return learning_resource_response

    async def delete_learning_resource(self, learning_resource_id: str):
        return await self.collection.delete_one({"_id": ObjectId(learning_resource_id)})

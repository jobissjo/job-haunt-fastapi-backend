class LearningPlanRepository:
    def __init__(self):
        self.collection = db.learning_plans

    async def create_learning_plan(self, learning_plan):
        return await self.collection.insert_one(learning_plan)

    async def get_learning_plans(self):
        documents = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_learning_plan_by_id(self, learning_plan_id):
        learning_plan_response = await self.collection.find_one(
            {"_id": ObjectId(learning_plan_id)}
        )
        learning_plan_response["_id"] = str(learning_plan_response["_id"])
        return learning_plan_response

    async def update_learning_plan(self, learning_plan_id, learning_plan):
        learning_plan_response = await self.collection.update_one(
            {"_id": ObjectId(learning_plan_id)}, {"$set": learning_plan}
        )
        learning_plan_response["_id"] = str(learning_plan_response["_id"])
        return learning_plan_response

    async def delete_learning_plan(self, learning_plan_id):
        return await self.collection.delete_one({"_id": ObjectId(learning_plan_id)})

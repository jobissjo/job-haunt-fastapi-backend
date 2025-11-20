from app.database import db
from bson import ObjectId
from app.schemas.activity_log_schema import ActivityLogSchema
from datetime import datetime, timezone 

class ActivityLogRepository:
    def __init__(self) -> None:
        self.collection = db.activity_logs

    async def get_activity_logs(self, user_id:str, limit:int=10, offset:int=0):
        total = await self.collection.count_documents({"user_id": ObjectId(user_id)})
        documents = []
        async for document in self.collection.find({"user_id": ObjectId(user_id)} ).sort("created_at", -1).limit(limit).skip(offset):
            document["_id"] = str(document["_id"])
            document['user_id'] = str(document["user_id"])
            documents.append(document)
        return documents, total
    
    async def create_activity_log(self, user_id:str, data: ActivityLogSchema):
        return await self.collection.insert_one({
            **data.model_dump(),
            'user_id': ObjectId(user_id),
            "created_at": datetime.now(timezone.utc)
        })


    


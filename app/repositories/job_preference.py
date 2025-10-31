from app.database import db
from app.schemas.job_preference import JobPreferenceSchemaCreate
from bson.objectid import ObjectId
from datetime import datetime

class JobPreferenceRepository:
    def __init__(self):
        self.collection = db.job_preference
    
    async def create_job_preference(self, job_preference: JobPreferenceSchemaCreate, user_id: str):
        result = await self.collection.insert_one(
            {**job_preference.model_dump(), 
            "user_id": ObjectId(user_id),
            "created_at": datetime.now(),
            "updated_at": datetime.now()}
        )
        return result.inserted_id
    
    async def get_job_preference_by_user_id(self, user_id: str):
        data = await self.collection.find_one(
            {"user_id": ObjectId(user_id)}
        )
        if data is None:
            return None
        data['_id'] = str(data['_id'])
        data['user_id'] = str(data['user_id'])
        return data
    
    async def update_job_preference(self,  job_preference: JobPreferenceSchemaCreate, user_id: str):
        await self.collection.update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": job_preference.model_dump()},
        )
        return True
from app.database import db
from bson import ObjectId
from app.schemas.notification_preference import NotificationPreference


class NotificationPreferenceRepository:
    def __init__(self):
        self.collection = db.notification_preference

    async def create_default_notification_preference(self, user_id: str):
        await self.collection.insert_one({"user_id": ObjectId(user_id), **NotificationPreference(email=False, push=False, sms=False).model_dump()})

    async def create_or_update_notification_preference(
        self, user_id: str, notification_preference: NotificationPreference
    ):
        existing_preference = await self.get_notification_preference(user_id)
        if existing_preference:
            await self.collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$set": notification_preference.model_dump(exclude_unset=True)},
            )
            return
        
        await self.collection.insert_one(
            {"user_id": ObjectId(user_id), **notification_preference.model_dump()}
        )
        

    async def get_notification_preference(self, user_id: str):
        data = await self.collection.find_one({"user_id": ObjectId(user_id)})
        if data:

            data["_id"] = str(data["_id"])
            data["user_id"] = str(data["user_id"])
        return data
        

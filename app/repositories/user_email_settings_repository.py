from bson import ObjectId

from app.database import db
from app.schemas.user_mail_settings import EmailSettings, EmailSettingsUpdate, EmailSettingsResponse


class UserEmailSettingsRepository:
    def __init__(self):
        self.collection = db.user_email_settings

    async def create_email_setting(
        self, user_id: str, email_setting: EmailSettings
    ) -> dict:
        """Create a new email setting for a user"""
        # If this setting is marked as active, deactivate all other settings for this user
        if email_setting.is_active:
            await self.collection.update_many(
                {"user_id": ObjectId(user_id)}, {"$set": {"is_active": False}}
            )

        result = await self.collection.insert_one(
            {**email_setting.model_dump(), "user_id": ObjectId(user_id)}
        )

        created_setting = await self.collection.find_one({"_id": result.inserted_id})
        created_setting["_id"] = str(created_setting["_id"])
        created_setting["user_id"] = str(created_setting["user_id"])
        return created_setting

    async def get_email_settings(self, user_id: str) -> list[dict]:
        """Get all email settings for a user"""
        documents = []
        async for document in self.collection.find({"user_id": ObjectId(user_id)}):
            document["_id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            documents.append(document)
        return documents

    async def get_email_setting_by_id(
        self, email_setting_id: str, user_id: str
    ) -> dict | None:
        """Get a specific email setting by ID"""
        email_setting = await self.collection.find_one(
            {"_id": ObjectId(email_setting_id), "user_id": ObjectId(user_id)}
        )
        if email_setting:
            email_setting["_id"] = str(email_setting["_id"])
            email_setting["user_id"] = str(email_setting["user_id"])
        return email_setting

    async def get_active_email_setting(self, user_id: str) -> EmailSettingsResponse | None:
        """Get the active email setting for a user"""
        email_setting = await self.collection.find_one(
            {"user_id": ObjectId(user_id), "is_active": True}
        )
        if not email_setting:
            return None
        email_setting["_id"] = str(email_setting["_id"])
        email_setting["user_id"] = str(email_setting["user_id"])
        return EmailSettingsResponse(**email_setting)

    async def update_email_setting(
        self, email_setting_id: str, user_id: str, email_setting: EmailSettingsUpdate
    ) -> dict | None:
        """Update an email setting"""
        update_data = email_setting.model_dump(exclude_unset=True)

        # If setting is_active to True, deactivate all other settings
        if update_data.get("is_active") is True:
            await self.collection.update_many(
                {
                    "user_id": ObjectId(user_id),
                    "_id": {"$ne": ObjectId(email_setting_id)},
                },
                {"$set": {"is_active": False}},
            )

        result = await self.collection.update_one(
            {"_id": ObjectId(email_setting_id), "user_id": ObjectId(user_id)},
            {"$set": update_data},
        )

        if result.modified_count > 0 or result.matched_count > 0:
            return await self.get_email_setting_by_id(email_setting_id, user_id)
        return None

    async def delete_email_setting(self, email_setting_id: str, user_id: str) -> bool:
        """Delete an email setting"""
        result = await self.collection.delete_one(
            {"_id": ObjectId(email_setting_id), "user_id": ObjectId(user_id)}
        )
        return result.deleted_count > 0

    async def set_active_email_setting(
        self, email_setting_id: str, user_id: str
    ) -> dict | None:
        """Set a specific email setting as active (deactivates all others)"""
        # Deactivate all settings for this user
        await self.collection.update_many(
            {"user_id": ObjectId(user_id)}, {"$set": {"is_active": False}}
        )

        # Activate the specified setting
        result = await self.collection.update_one(
            {"_id": ObjectId(email_setting_id), "user_id": ObjectId(user_id)},
            {"$set": {"is_active": True}},
        )

        if result.modified_count > 0 or result.matched_count > 0:
            return await self.get_email_setting_by_id(email_setting_id, user_id)
        return None

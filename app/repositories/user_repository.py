from datetime import datetime

from bson import ObjectId

from app.database import db
from app.schemas.user import RegisterUserSchema


class UserRepository:
    def __init__(self):
        self.collection = db.users

    async def create_user(self, user: RegisterUserSchema):
        return await self.collection.insert_one({**user.model_dump(), 'is_active': True, 'join_date': datetime.now()})
    
    async def get_users_count(self):
        return await self.collection.count_documents({})

    async def get_users(self):
        documents = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def get_user_by_id(self, user_id):
        user_response = await self.collection.find_one({"_id": ObjectId(user_id)})
        user_response["_id"] = str(user_response["_id"])
        return user_response

    async def get_user_by_email(self, email):
        user_response = await self.collection.find_one({"email": email})
        user_response["_id"] = str(user_response["_id"])
        return user_response

    async def get_user_by_username_email_phone(
        self, username: str = None, email: str = None, phone_number: str = None
    ):
        if username is None and email is None and phone_number is None:
            return None

        if username is not None:
            user_response = await self.collection.find_one({"username": username})
        elif email is not None:
            user_response = await self.collection.find_one({"email": email})
        elif phone_number is not None:
            user_response = await self.collection.find_one(
                {"phone_number": phone_number}
            )

        user_response["_id"] = str(user_response["_id"])
        return user_response

    async def update_user(self, user_id, user):
        user_response = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user}
        )
        user_response["_id"] = str(user_response["_id"])
        return user_response

    async def delete_user(self, user_id):
        return await self.collection.delete_one({"_id": ObjectId(user_id)})

    async def update_user_password(self, user_id, password):
        return await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"password": password}}
        )

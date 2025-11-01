from bson import ObjectId
from datetime import datetime

from app.database import db
from app.schemas.resource_notes import BaseNoteSchema, NoteResponseSchema


class ResourceNoteRepository:
    def __init__(self):
        self.collection = db.resource_notes

    async def create_note(self, note: BaseNoteSchema, user_id: str) -> None:
        await self.collection.insert_one(
            {
                **note.model_dump(),
                "user_id": ObjectId(user_id),
                "resource_id": ObjectId(note.resource_id),
                "created_at": datetime.now(),
            }
        )

    async def get_notes(self, user_id: str, resource_id: str | None = None) -> list[NoteResponseSchema]:
        documents = []
        filter = {"user_id": ObjectId(user_id)}
        if resource_id:
            filter["resource_id"] = ObjectId(resource_id)
        async for document in self.collection.find(filter):
            document["_id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            document["resource_id"] = str(document["resource_id"])
            documents.append(document)
        return documents

    async def get_note_by_id(
        self, note_id: str, user_id: str
    ) -> NoteResponseSchema | None:
        note_response = await self.collection.find_one(
            {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
        )
        if note_response is None:
            return None
        note_response["_id"] = str(note_response["_id"])
        note_response["user_id"] = str(note_response["user_id"])
        note_response["resource_id"] = str(note_response["resource_id"])
        return note_response

    async def update_note(
        self, note_id: str, note: BaseNoteSchema, user_id: str
    ) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {
                "$set": {
                    **note.model_dump(),
                    "user_id": ObjectId(user_id),
                    "resource_id": ObjectId(note.resource_id),
                }
            },
        )

    async def delete_note(self, note_id: str, user_id: str) -> None:
        await self.collection.delete_one({"_id": ObjectId(note_id), "user_id": user_id})

from fastapi import Depends, HTTPException

from app.repositories.resource_note import ResourceNoteRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.resource_notes import (
    BaseNoteSchema,
    NoteDetailResponse,
    NoteListResponse,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService


class ResourceNoteService:
    def __init__(self):
        self.repository = ResourceNoteRepository()

    async def create_note(
        self,
        note: BaseNoteSchema,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> BaseResponseSchema:
        await self.repository.create_note(note, user_data.id)
        return BaseResponseSchema(success=True, message="Note created successfully")

    async def get_notes(
        self,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
        resource_id: str | None = None,
    ) -> NoteListResponse:
        data = await self.repository.get_notes(user_data.id, resource_id)
        return NoteListResponse(
            data=data, success=True, message="Notes fetched successfully"
        )

    async def get_note_by_id(
        self,
        note_id: str,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> NoteDetailResponse:
        data = await self.repository.get_note_by_id(note_id, user_data.id)
        if data is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return NoteDetailResponse(
            data=data, success=True, message="Note fetched successfully"
        )

    async def update_note(
        self,
        note_id: str,
        note: BaseNoteSchema,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> BaseResponseSchema:
        await self.repository.update_note(note_id, note, user_data.id)
        return BaseResponseSchema(success=True, message="Note updated successfully")

    async def delete_note(
        self,
        note_id: str,
        user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ) -> BaseResponseSchema:
        await self.repository.delete_note(note_id, user_data.id)
        return BaseResponseSchema(success=True, message="Note deleted successfully")

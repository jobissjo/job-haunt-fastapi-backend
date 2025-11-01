from fastapi import APIRouter, Depends, Query

from app.schemas.common import BaseResponseSchema
from app.schemas.resource_notes import (
    BaseNoteSchema,
    NoteDetailResponse,
    NoteListResponse,
)
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.resource_notes import ResourceNoteService

router = APIRouter()


@router.post("/notes", response_model=BaseResponseSchema, tags=["Resource Notes"])
async def create_note(
    note: BaseNoteSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceNoteService = Depends(ResourceNoteService),
) -> BaseResponseSchema:
    return await service.create_note(note, user_data)


@router.get("/notes", response_model=NoteListResponse, tags=["Resource Notes"])
async def get_notes(
    resource_id: str | None = Query(None, description="Filter notes by resource ID"),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceNoteService = Depends(ResourceNoteService),
) -> NoteListResponse:
    return await service.get_notes(user_data, resource_id)


@router.get("/notes/{note_id}", response_model=NoteDetailResponse, tags=["Resource Notes"])
async def get_note_by_id(
    note_id: str,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceNoteService = Depends(ResourceNoteService),
) -> NoteDetailResponse:
    return await service.get_note_by_id(note_id, user_data)


@router.put("/notes/{note_id}", response_model=BaseResponseSchema, tags=["Resource Notes"])
async def update_note(
    note_id: str,
    note: BaseNoteSchema,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceNoteService = Depends(ResourceNoteService),
) -> BaseResponseSchema:
    return await service.update_note(note_id, note, user_data)


@router.delete("/notes/{note_id}", response_model=BaseResponseSchema, tags=["Resource Notes"])
async def delete_note(
    note_id: str,
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    service: ResourceNoteService = Depends(ResourceNoteService),
) -> BaseResponseSchema:
    return await service.delete_note(note_id, user_data)

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema


class BaseNoteSchema(BaseModel):
    resource_id: str
    title: str = Field(..., description="Short title or subject of the note")
    content: str = Field(..., description="Detailed note content")
    priority: Optional[Literal["low", "medium", "high"]] = Field(
        default="medium", description="Indicates importance level of this note"
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.now)


class NoteResponseSchema(BaseNoteSchema):
    id: str = Field(default_factory=str, alias="_id")
    user_id: str
    model_config = ConfigDict(populate_by_name=True)


class NoteListResponse(BaseResponseSchema):
    data: list[NoteResponseSchema]


class NoteDetailResponse(BaseResponseSchema):
    data: NoteResponseSchema

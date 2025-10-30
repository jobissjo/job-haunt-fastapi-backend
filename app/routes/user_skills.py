from fastapi import APIRouter, Depends

from app.schemas.user import UserTokenDecodedData
from app.schemas.user_skills import (
    BaseResponseSchema,
    UserSkillDetailResponse,
    UserSkillListResponse,
    UserSkillSchema,
)
from app.services.common import CommonService
from app.services.user_skills import UserSkillService

router = APIRouter(prefix="/user-skills", tags=["User Skills"])


@router.get("/")
async def get_user_skills(
    service: UserSkillService = Depends(UserSkillService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
) -> UserSkillListResponse:
    return await service.get_user_skills(user_data.id)


@router.get("/{user_skill_id}")
async def get_user_skill_by_id(
    user_skill_id: str, service: UserSkillService = Depends(UserSkillService)
) -> UserSkillDetailResponse:
    return await service.get_user_skill_by_id(user_skill_id)


@router.post("/")
async def create_user_skill(
    user_skill: UserSkillSchema,
    service: UserSkillService = Depends(UserSkillService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
) -> BaseResponseSchema:
    return await service.create_user_skill(user_skill, user_data.id)


@router.put("/{user_skill_id}")
async def update_user_skill(
    user_skill_id: str,
    user_skill: UserSkillSchema,
    service: UserSkillService = Depends(UserSkillService),
) -> BaseResponseSchema:
    return await service.update_user_skill(user_skill_id, user_skill)


@router.delete("/{user_skill_id}")
async def delete_user_skill(
    user_skill_id: str, service: UserSkillService = Depends(UserSkillService)
) -> BaseResponseSchema:
    return await service.delete_user_skill(user_skill_id)

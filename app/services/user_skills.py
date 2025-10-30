from app.repositories.user_skills import UserSkillRepository
from app.schemas.user_skills import BaseResponseSchema, UserSkillDetailResponse, UserSkillListResponse, UserSkillSchema


class UserSkillService:
    def __init__(self):
        self.repository = UserSkillRepository()
    
    async def create_user_skill(self, user_skill: UserSkillSchema, user_id:str)->BaseResponseSchema:
        await self.repository.create_user_skill(user_skill, user_id)
        return {'message': 'User skill created successfully', 'success': True}
    
    async def get_user_skills(self, user_id: str)->UserSkillListResponse:
        data = await self.repository.get_user_skills(user_id)
        return {'data': data, 'message': 'User skills fetched successfully', 'success': True}
    
    async def get_user_skill_by_id(self, user_skill_id: str)->UserSkillDetailResponse:
        data = await self.repository.get_user_skill_by_id(user_skill_id)
        return {'data': data, 'message': 'User skill fetched successfully', 'success': True}
    
    async def update_user_skill(self, user_skill_id: str, user_skill: UserSkillSchema)->BaseResponseSchema:
        await self.repository.update_user_skill(user_skill_id, user_skill)
        return {'message': 'User skill updated successfully', 'success': True}
    
    async def delete_user_skill(self, user_skill_id: str)->BaseResponseSchema:
        await self.repository.delete_user_skill(user_skill_id)
        return {'message': 'User skill deleted successfully', 'success': True}

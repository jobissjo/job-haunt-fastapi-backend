from app.repositories.activity_log_repository import ActivityLogRepository
from app.schemas.activity_log_schema import ActivityLogSchema

class ActivityLogService:
    def __init__(self):
        self.activity_log_repository = ActivityLogRepository()
    
    async def get_activity_logs(self, user_id:str, limit:int, offset:int):
        response, total = await self.activity_log_repository.get_activity_logs(user_id, limit, offset)
        return {
            "data": response,
            "total_count": total

        }
    
    async def create_activity_log(self, user_id:str, data:ActivityLogSchema):
        await self.activity_log_repository.create_activity_log(user_id, data)
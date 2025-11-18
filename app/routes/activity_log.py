from fastapi import APIRouter, Depends
from app.schemas.user import UserTokenDecodedData
from app.services.common import CommonService
from app.services.activity_log_service import ActivityLogService


router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@router.get("/")
async def get_stats(
    service: ActivityLogService = Depends(ActivityLogService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    limit:int =10,
    offset:int=0
    ):
    return await service.get_activity_logs(user_data.id, limit=limit, offset=offset)
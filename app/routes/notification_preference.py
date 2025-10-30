from fastapi import APIRouter, Depends
from app.services.common import CommonService
from app.services.notification_preference import NotificationPreferenceService
from app.schemas.user import UserTokenDecodedData
from app.schemas.notification_preference import NotificationPreference, NotificationPreferenceUpdate

router = APIRouter(prefix="/notification-preference", tags=["Notification Preference"])

@router.get("/")
async def get_notification_preference(service: NotificationPreferenceService = Depends(NotificationPreferenceService), user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user)):
    return await service.get_notification_preference(user_data.id)

@router.put("/")
async def update_notification_preference(
    notification_preference: NotificationPreference,
    service: NotificationPreferenceService = Depends(NotificationPreferenceService), 
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user)
):
    return await service.create_or_update_notification_preference(user_data.id, notification_preference)

@router.patch("/")
async def patch_notification_preference(
    notification_preference: NotificationPreferenceUpdate,
    service: NotificationPreferenceService = Depends(NotificationPreferenceService), 
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user)
):

    return await service.create_or_update_notification_preference(user_data.id, notification_preference)


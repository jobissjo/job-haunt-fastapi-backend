from fastapi import APIRouter, Depends
from app.services.common import CommonService
from app.services.user_email_settings_service import UserEmailSettingsService
from app.schemas.user import UserTokenDecodedData
from app.schemas.user_mail_settings import (
    EmailSettings,
    EmailSettingsUpdate,
    EmailSettingsDetailResponse,
    EmailSettingsListResponse,
)

router = APIRouter(prefix="/user-email-settings", tags=["User Email Settings"])


@router.post("/", response_model=EmailSettingsDetailResponse)
async def create_email_setting(
    email_setting: EmailSettings,
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Create a new email setting for the authenticated user"""
    return await service.create_email_setting(user_data.id, email_setting)


@router.get("/", response_model=EmailSettingsListResponse)
async def get_email_settings(
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Get all email settings for the authenticated user"""
    return await service.get_email_settings(user_data.id)


@router.get("/active", response_model=EmailSettingsDetailResponse)
async def get_active_email_setting(
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Get the active email setting for the authenticated user"""
    return await service.get_active_email_setting(user_data.id)


@router.get("/{email_setting_id}", response_model=EmailSettingsDetailResponse)
async def get_email_setting_by_id(
    email_setting_id: str,
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Get a specific email setting by ID"""
    return await service.get_email_setting_by_id(email_setting_id, user_data.id)


@router.put("/{email_setting_id}", response_model=EmailSettingsDetailResponse)
async def update_email_setting(
    email_setting_id: str,
    email_setting: EmailSettingsUpdate,
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Update an email setting"""
    return await service.update_email_setting(
        email_setting_id, user_data.id, email_setting
    )


@router.patch("/{email_setting_id}/activate", response_model=EmailSettingsDetailResponse)
async def set_active_email_setting(
    email_setting_id: str,
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Set a specific email setting as active (deactivates all others)"""
    return await service.set_active_email_setting(email_setting_id, user_data.id)


@router.delete("/{email_setting_id}")
async def delete_email_setting(
    email_setting_id: str,
    service: UserEmailSettingsService = Depends(UserEmailSettingsService),
    user_data: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    """Delete an email setting"""
    return await service.delete_email_setting(email_setting_id, user_data.id)

from fastapi import HTTPException

from app.repositories.user_email_settings_repository import UserEmailSettingsRepository
from app.schemas.user_mail_settings import (
    EmailSettings,
    EmailSettingsDetailResponse,
    EmailSettingsListResponse,
    EmailSettingsUpdate,
)


class UserEmailSettingsService:
    def __init__(self):
        self.repository = UserEmailSettingsRepository()

    async def create_email_setting(
        self, user_id: str, email_setting: EmailSettings
    ) -> EmailSettingsDetailResponse:
        """Create a new email setting for a user"""
        data = await self.repository.create_email_setting(user_id, email_setting)
        return {
            "success": True,
            "message": "Email setting created successfully",
            "data": data,
        }

    async def get_email_settings(self, user_id: str) -> EmailSettingsListResponse:
        """Get all email settings for a user"""
        data = await self.repository.get_email_settings(user_id)
        return {
            "success": True,
            "message": "Email settings retrieved successfully",
            "data": data,
        }

    async def get_email_setting_by_id(
        self, email_setting_id: str, user_id: str
    ) -> EmailSettingsDetailResponse:
        """Get a specific email setting by ID"""
        data = await self.repository.get_email_setting_by_id(email_setting_id, user_id)
        if not data:
            raise HTTPException(status_code=404, detail="Email setting not found")
        return {
            "success": True,
            "message": "Email setting retrieved successfully",
            "data": data,
        }

    async def get_active_email_setting(
        self, user_id: str
    ) -> EmailSettingsDetailResponse:
        """Get the active email setting for a user"""
        data = await self.repository.get_active_email_setting(user_id)
        if not data:
            raise HTTPException(status_code=404, detail="No active email setting found")
        return {
            "success": True,
            "message": "Active email setting retrieved successfully",
            "data": data,
        }

    async def update_email_setting(
        self, email_setting_id: str, user_id: str, email_setting: EmailSettingsUpdate
    ) -> EmailSettingsDetailResponse:
        """Update an email setting"""
        data = await self.repository.update_email_setting(
            email_setting_id, user_id, email_setting
        )
        if not data:
            raise HTTPException(status_code=404, detail="Email setting not found")
        return {
            "success": True,
            "message": "Email setting updated successfully",
            "data": data,
        }

    async def delete_email_setting(self, email_setting_id: str, user_id: str) -> dict:
        """Delete an email setting"""
        deleted = await self.repository.delete_email_setting(email_setting_id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Email setting not found")
        return {
            "success": True,
            "message": "Email setting deleted successfully",
        }

    async def set_active_email_setting(
        self, email_setting_id: str, user_id: str
    ) -> EmailSettingsDetailResponse:
        """Set a specific email setting as active"""
        data = await self.repository.set_active_email_setting(email_setting_id, user_id)
        if not data:
            raise HTTPException(status_code=404, detail="Email setting not found")
        return {
            "success": True,
            "message": "Email setting activated successfully",
            "data": data,
        }

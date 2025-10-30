from app.repositories.notification_preference_repository import (
    NotificationPreferenceRepository,
)
from app.schemas.notification_preference import (
    NotificationPreference,
    NotificationPreferenceDetailResponse,
)


class NotificationPreferenceService:
    def __init__(self):
        self.repository = NotificationPreferenceRepository()

    async def create_or_update_notification_preference(
        self, user_id: str, notification_preference: NotificationPreference
    ):
        await self.repository.create_or_update_notification_preference(
            user_id, notification_preference
        )
        return {
            "success": True,
            "message": "Notification preference created or updated successfully",
        }

    async def get_notification_preference(
        self, user_id: str
    ) -> NotificationPreferenceDetailResponse:
        data = await self.repository.get_notification_preference(user_id)
        if not data:
            await self.repository.create_default_notification_preference(user_id)
            data = await self.repository.get_notification_preference(user_id)
        return {
            "success": True,
            "data": data,
            "message": "Notification preference retrieved successfully",
        }

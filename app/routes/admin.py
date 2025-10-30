from fastapi import APIRouter, Depends

from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
async def get_stats(service: AdminService = Depends(AdminService)):
    return await service.get_stats()

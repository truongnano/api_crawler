from fastapi import APIRouter
from api.endpoints.douyin import web as DouyinWeb

router = APIRouter()

# Douyin routers
router.include_router(DouyinWeb.router, prefix="/douyin/web", tags=["Douyin-Web-API"])
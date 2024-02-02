from fastapi import APIRouter

from app.api.v1.users import router  as users_router
from app.api.v1.login import router as login_router

router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(login_router)


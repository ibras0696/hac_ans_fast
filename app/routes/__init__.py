from .user import router as user_rout
from .auth import router as auth_rout
from .moderator import router as moderator_rout


from fastapi import APIRouter


router = APIRouter()

router.include_router(user_rout, prefix="/user")

router.include_router(auth_rout, prefix="/auth")

router.include_router(moderator_rout, prefix="/moderator")

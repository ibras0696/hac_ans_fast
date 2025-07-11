from aiogram import Router

from .admin import router as admin


router = Router()

router.include_router(admin)
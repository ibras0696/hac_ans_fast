from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from ..config import ADMIN_ID


class AdminTypeFilter(BaseFilter):
    def __init__(self):
        self.ADMIN_ID = ADMIN_ID

    async def __call__(self, message: Message):
        return True if message.chat.id == self.ADMIN_ID else False


class AdminCallBackFilter(BaseFilter):
    def __init__(self):
        self.ADMIN_ID = ADMIN_ID

    async def __call__(self, call_back: CallbackQuery):
        if not call_back.message:
            return False
        return call_back.message.chat.id == self.ADMIN_ID

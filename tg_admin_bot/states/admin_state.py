from aiogram.fsm.state import StatesGroup, State


# Состояние добавление Модератора
class NewModerState(StatesGroup):
    user_name = State()

# Состояние изменения роли Модер
class RedactModerState(StatesGroup):
    user_name = State()
    moder_status = State()
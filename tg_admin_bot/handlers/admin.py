from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters import AdminTypeFilter, AdminCallBackFilter

from keyboards import kb_ad, redact_moder_kb, admin_start_kb, inline_keyboard_buttons

from states import NewModerState, RedactModerState

from database import CrudUser

router = Router()


@router.message(Command('start'), AdminTypeFilter())
async def admin_start_cmd(message: Message, state: FSMContext):
    # Очистка состояний
    await state.clear()

    await message.answer(
        "👋 Добро пожаловать в Админ-Панель!\n\n"
        "Здесь вы можете:\n"
        "• Управлять ролями модераторов\n"
        "• Контролировать доступ и права модератора\n\n", reply_markup=redact_moder_kb
    )


@router.callback_query(F.data, AdminCallBackFilter())
async def call_admin_start_cmd(call_back: CallbackQuery, state: FSMContext):
    dt_call = call_back.data
    users = await CrudUser().list_users()

    is_not_moders = []
    is_moders = []

    for user in users:
        if user.is_moderator:
            is_moders.append(user.username)
        else:
            is_not_moders.append(user.username)


    match dt_call:
        case 'moder_delete_moder':
            await state.set_state(RedactModerState.moder_status)
            await state.update_data(moder_status=False)
            kb = inline_keyboard_buttons(
                buttons_dct={
                    username: f'add_{username}' for username in is_moders
                },
                adjust=3
            )
            await call_back.message.answer('Выберите Модера которого хотите убрать', reply_markup=kb)

        case 'moder_new_moder':
            await state.set_state(RedactModerState.moder_status)
            await state.update_data(moder_status=True)
            kb = inline_keyboard_buttons(
                buttons_dct={
                    username: f'add_{username}' for username in is_not_moders
                },
                adjust=3
            )
            await call_back.message.answer('Выберите Пользователя которого хотите сделать модератором', reply_markup=kb)


@router.callback_query(F.data.startswith('add_'), RedactModerState.moder_status)
async def add_moder_cmd(call_back: CallbackQuery, state: FSMContext):
    try:
        user_name = call_back.data.replace('add_', '')
        #await CrudUser().set_moderator_status(username=user_name, is_moderator=True)

        await call_back.message.answer(f'Пользователь: {user_name} добавлен в роли модера')
    except Exception as ex:
        await call_back.message.answer(f'Ошибка: {ex}')
    finally:
        await state.clear()

@router.callback_query(F.data.startswith('del_'), RedactModerState.moder_status)
async def del_mode_cmd(call_back: CallbackQuery, state: FSMContext):
    try:
        user_name = call_back.data.replace('del_', '')
        #await CrudUser().set_moderator_status(username=user_name, is_moderator=False)


        await call_back.message.answer(f'Пользователь: {user_name} удален из роли модера')
    except Exception as ex:
        await call_back.message.answer(f'Ошибка: {ex}')
    finally:
        await state.clear()
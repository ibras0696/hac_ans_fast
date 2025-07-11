# Кнопки пользователей
import asyncio

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Inline Keyboard
def inline_keyboard_buttons(buttons_dct: dict, starts: str='', adjust: int=2, url_btn: bool= False) -> InlineKeyboardMarkup:
    '''
    Функция возвращает несколько кнопок
    :param buttons_dct: Словарь {кнопка: ссылка или callback}
    :param starts: Начало callback
    :param adjust: общий ряд сколь кнопок должно быть в ряд
    :param url_btn: Если поставить True передаваться будут ссылки
    :return: InlineKeyboardMarkup
    '''
    try:
        if url_btn:
            kb = InlineKeyboardBuilder()
            for key, value in buttons_dct.items():
                kb.add(InlineKeyboardButton(text=key, url=value))
            return kb.adjust(adjust).as_markup()
        else:
            kb = InlineKeyboardBuilder()
            for key, value in buttons_dct.items():
                kb.add(InlineKeyboardButton(text=key, callback_data=f'{starts}{value}'))
            return kb.adjust(adjust).as_markup()
    except Exception as ex:
        raise f'Ошибка при создании кнопок: {ex}'


#  Стартовая клавиатура админа
admin_start_kb = 1#inline_keyboard_buttons(
#     buttons_dct={
#         'Изменение Роль Модератора': 'redact_moder',
#     },
#     starts='start_',
#     adjust=1
# )


# Изменение роли модератора
redact_moder_kb = inline_keyboard_buttons(
    buttons_dct={
        'Снять Роль модератора': 'moder_delete_moder',
        'Сделать Модератором': 'moder_new_moder',
    },
    starts='',
    adjust=2
)

# # Кнопка назад
# admin_back_kb = inline_keyboard_buttons(
#     buttons_dct={
#
#     }
# )
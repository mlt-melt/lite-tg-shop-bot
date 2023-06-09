from typing import Dict
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageNotModified
import random
from markups import rules_mkp
from config import db


class Captcha:
    """
    Сreates a captcha, which you need to click on a certain element to pass
    Developed by: https://github.com/mrskyguy
    Callback data which using for Captcha will be look like "_Captcha{captcha_id}..."
    """

    captcha_id = 0
    passed_captcha_users = set() 
    # Here will be stored information about which 
    # users have passed the captcha 
    # this information is needed so that the captcha does 
    # not come out several times in a row
    # Before launching the captcha, specify the condition: 
    #   if message.from_user.id not in Captcha.passed_captcha_users:
    #       captcha = Captcha()
    #       ...

    def __init__(self, choices: Dict[str, str] = None) -> None:
        if choices and isinstance(choices, dict):
            self.choices = choices
        else:
            self.choices = {
                "яблоко": "🍎",
                "автомобиль": "🚗",
                "собаку": "🐶",
                "дерево": "🌳",
                "радугу": "🌈",
                "банан": "🍌",
            }
        self.correct_choice = random.choice(list(self.choices.keys()))

        # ID for captcha needs for creating unique callback_data for keyboard
        Captcha.captcha_id += 1
        self.captcha_id = Captcha.captcha_id
        self.callback_name = f"_Captcha{self.captcha_id}"

        self.captcha_passed = False

    def get_captcha_keyboard(self) -> InlineKeyboardMarkup:
        captcha_keyboard = InlineKeyboardMarkup()

        for choice in random.sample(list(self.choices.keys()), len(self.choices)):
            captcha_keyboard.insert(
                InlineKeyboardButton(
                    self.choices[choice],
                    callback_data=f"{self.callback_name}_choice_"
                    + ("1" if choice == self.correct_choice else "0")
                    # 1 at the end of callback_data means, that this button is correct one
                )
            )

        return captcha_keyboard

    def get_caption(self) -> str:
        return f"Чтобы получить доступ к боту, нажмите на {self.correct_choice}"

    async def captcha_choice_handler(
        self,
        callback_query: types.CallbackQuery,
    ) -> None:
        if callback_query.data.split("_")[-1] == "0":
            self.correct_choice = random.choice(list(self.choices.keys()))
            try:
                await callback_query.message.edit_text(
                    "Неверно. Попробуйте ещё раз\n" + self.get_caption(),
                    reply_markup=self.get_captcha_keyboard(),
                )
            except MessageNotModified:
                ...
            return

        self.captcha_passed = True
        Captcha.passed_captcha_users.add(callback_query.from_user.id)

        await callback_query.message.edit_text(
            "Капча пройдена. Вам был предоставлен доступ к боту", reply_markup=None
        )
        await callback_query.message.answer(f'Правила использования бота:\n\n{db.get_rules()}', reply_markup=rules_mkp())

    def register_handlers(self, dp: Dispatcher):
        dp.register_callback_query_handler(
            self.captcha_choice_handler,
            lambda c: c.data.startswith(f"{self.callback_name}_choice_"),
        )
from config import dp
from aiogram.utils import executor
import start
import support
import admin
import userfaq
import shop
import usermenu
import review


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
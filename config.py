from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DB

admins = []                 # list of admin's IDs (for example - [345345234, 557546745, 745985797])
review_channel_url = ''     # url of the channel with feedbacks (for example:  https://t.me/+RDE2gELnj6A1NTRa)
review_channel_id = ''      # id of the channel with feedbacks (for example:   -1001627120479)
admin_ulr = ''              # admin's url

db = DB('db.db')            # database name

BOT_TOKEN = ''              # bot's token
bot = Bot(BOT_TOKEN, parse_mode='html') 

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
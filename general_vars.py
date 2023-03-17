import json

from aiogram.bot import Bot
from aiogram.dispatcher import Dispatcher


load_config = lambda: json.load(open("config.json", "r", encoding="utf-8"))
save_config = lambda config_obj: json.dump(config_obj, open("config.json", "w", encoding="utf-8"), indent=4)

config = load_config()
bot = Bot(token=config["bot_token"])
dispatcher = Dispatcher(bot=bot)

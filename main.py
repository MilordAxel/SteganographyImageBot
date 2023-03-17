import os

from aiogram import executor
from general_vars import dispatcher
from handlers.commands import welcome
from handlers.content_messages import get_image


def main():
    if not os.path.exists("input"): os.mkdir("input")
    if not os.path.exists("output"): os.mkdir("output")
    
    # For work all handlers from file just register one handler from file
    dispatcher.register_message_handler(welcome)
    dispatcher.register_message_handler(get_image)
    
    executor.start_polling(dispatcher=dispatcher, skip_updates=True)


if __name__ == "__main__":
    main()

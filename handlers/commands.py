from aiogram.types import Message
from general_vars import dispatcher, load_config, save_config


@dispatcher.message_handler(commands=["start"])
async def welcome(message: Message):
    await message.answer(text="Hello!\nI'm SteganographyImageBot, and I can hidden your message in any image\nTry me, call a command /write_text_in_image")


@dispatcher.message_handler(commands=["help"])
async def help(message: Message):
    await message.answer(text="I'm SteganographyImageBot, and I can hidden your message in any image\n\n"
                              "Commands for interaction with me:\n"
                              "/write_text_in_image - call this command for start proccess writing text in image\n"
                              "/read_text_from_image - call this command for start proccess reading text from image")


@dispatcher.message_handler(commands=["write_text_in_image"])
async def get_text(message: Message):
    """
    This handler start request neccessary resourses for writing text in image
    """
    config = load_config()
    config["users_current_command"][str(message.from_user.id)] = "write_text"   # using in get_text and download_image
                                                                                # in content_messages.py
    save_config(config)
    await message.answer(text="Please, send me text which need write to image")


@dispatcher.message_handler(commands=["read_text_from_image"])
async def read_text_from_image(message: Message):
    """
    This handler request image with text and reading text from image (only for image that was created by this bot)
    """
    config = load_config()
    config["users_current_command"][str(message.from_user.id)] = "read_text"    # using in download_image
                                                                                # in handlers/content_messages.py
    save_config(config)
    await message.answer(text="Send photo and I start read text from image")

import os

from PIL import Image
from aiogram.types import Message
from aiogram.types.input_file import InputFile
from SteganographyTools import stentools, exceptions
from general_vars import bot, dispatcher, load_config, save_config


@dispatcher.message_handler(content_types=["text"])
async def get_image(message: Message):
    """
    This handler get text for writing in image (only works after call command /write_text_in_image)
    """
    config = load_config()
    if config["users_current_command"][str(message.from_user.id)] == "write_text":
        with open(os.path.join("input", f"text_{message.from_user.id}.txt"), "w", encoding="utf-8") as file:
            file.write(message.text)
        await message.answer(text="Now send photo and I start write text in image")


@dispatcher.message_handler(content_types=["document"])
async def download_image(message: Message):
    """
    This handler download image for writing and reading text depending on the current command
    """    
    config = load_config()
    if config["users_current_command"][str(message.from_user.id)] == "write_text":        
        image_bytes = await bot.download_file_by_id(message.document.file_id)
        with open(os.path.join("input", f"image_{message.from_user.id}.png"), "wb") as file:
            file.write(image_bytes.getvalue())
        
        await message.answer(text="Starting writing text in image...")
        
        image = Image.open(os.path.join("input", f"image_{message.from_user.id}.png"))
        all_pixels = stentools.get_all_pixels(image)
        
        with open(os.path.join("input", f"text_{message.from_user.id}.txt"), encoding="utf-8") as file:
            text = file.read()
        
        try:
            pixels_with_text = stentools.write_text_to_image(text, all_pixels)
        except exceptions.TextIsTooLong as error_msg:
            os.remove(os.path.join("input", f"text_{message.from_user.id}.txt"))
            os.remove(os.path.join("input", f"image_{message.from_user.id}.png"))
            await message.answer(f"{error_msg}. Send other text and send again image")
            return
        except exceptions.TextLenghtIsBiggerSizeImage as error_msg:
            os.remove(os.path.join("input", f"image_{message.from_user.id}.png"))
            await message.answer(f"{error_msg}. Send a bigger image please")
            return
        
        image_with_text = Image.new("RGB", (image.width, image.height))
        stentools.put_all_pixels(image_with_text, pixels_with_text)
        image_with_text.save(os.path.join("output", f"image_text_{message.from_user.id}.png"))
        
        image_text = InputFile(os.path.join("output", f"image_text_{message.from_user.id}.png"))
        await bot.send_document(chat_id=message.chat.id, document=image_text)
        
        os.remove(os.path.join("input", f"text_{message.from_user.id}.txt"))
        os.remove(os.path.join("input", f"image_{message.from_user.id}.png"))
        os.remove(os.path.join("output", f"image_text_{message.from_user.id}.png"))
        config["users_current_command"][str(message.from_user.id)] = ""
    
    elif config["users_current_command"][str(message.from_user.id)] == "read_text":
        image_bytes = await bot.download_file_by_id(message.document.file_id)
        with open(os.path.join("input", f"image_text_{message.from_user.id}.png"), "wb") as file:
            file.write(image_bytes.getvalue())
        
        await message.answer(text="Starting reading text from image...")
        
        image = Image.open(os.path.join("input", f"image_text_{message.from_user.id}.png"))
        all_pixels = stentools.get_all_pixels(image)
        
        text_from_image = stentools.read_text_from_image(all_pixels)
        await message.answer("Text from image: " + text_from_image)
        
        os.remove(os.path.join("input", f"image_text_{message.from_user.id}.png"))
        config["users_current_command"][str(message.from_user.id)] = ""
    save_config(config)

import os
from PIL import Image,ImageFilter
import requests
import tracemoepy
from app.database.bot_base import *
from aiogram.enums import ParseMode

lux_channel_id = -1001686147209

def image_making(file_path):

    logo = 'media/logo.png'
    info = 'mediainfo.png'

    logo = Image.open(logo, 'r')
    info = Image.open(info, 'r')

    background_image = file_path

    original_image = Image.open(background_image)

    new_width = 1920
    new_height = 1080

    scaled_image = original_image.resize((new_width, new_height))
    scaled_image.save('media/anime.jpg')

    bg = Image.open(background_image, 'r')
    bg = bg.filter(ImageFilter.BoxBlur(4))
    bg.save('media/blured.jpg')
    bg = Image.open("media/blured.jpg", 'r')

    text_img = Image.new('RGB', (1920,1080), (0, 0, 0))
    text_img.paste(bg, (0,0))
    text_img.paste(logo, (650,270), mask=logo)
    text_img.paste(info, (0,900), mask=info)
    text_img.save("media/output.jpg")

    os.remove("media/blured.jpg")
    os.remove("media/anime.jpg")

    return "media/output.jpg"

async def searching_anime_by_image(image_path):
    try:
        tracemoe = tracemoepy.tracemoe.TraceMoe()
        resp = tracemoe.search(image_path,upload_file=True)
        os.remove(image_path)

        return resp
    except:
        os.remove(image_path)
        return "Error"


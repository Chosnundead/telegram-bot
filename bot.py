from tkinter import image_names
import telebot
from google_images_search import GoogleImagesSearch
from telebot import types
import re
import os
import wikipediaapi

# Keys
bot = telebot.TeleBot("5655783257:AAGU6Mq_EAVMPTojKN8x2OnUjkCNHPMzzxI")
gis = GoogleImagesSearch("AIzaSyBcs9pkCQgKOmBcuV6Jte9V4JBgbsnEV4g", "8503f6ad0de1e4fa2")

# Constants
PATH_TO_DIR = "{}temp\\".format(re.sub(r"bot.py", "", __file__))

searchParams = {
    "q": "!default!",
    "num": 0,
    "safe": "off",
    "fileType": "jpg",
    "imgSize": "xlarge",
}
isFirst = True
userFirstMessage = None


@bot.message_handler(content_types=["text", "document", "audio"])
def start(message):

    global isFirst, userFirstMessage
    if isFirst:
        bot.send_message(message.from_user.id, "Hello, I'm your bot:)")
        userFirstMessage = message
        isFirst = False

    menu(message)


def menu(message):
    keyboard = types.InlineKeyboardMarkup()
    key_image = types.InlineKeyboardButton(text="Image search", callback_data="image")
    keyboard.add(key_image)
    key_wiki = types.InlineKeyboardButton(text="Wikipedia search", callback_data="wiki")
    keyboard.add(key_wiki)
    bot.send_message(
        message.from_user.id, "Select a function from below.", reply_markup=keyboard
    )


def get_query_for_image(message):
    bot.send_message(message.from_user.id, "Write your query...")
    bot.register_next_step_handler(message, get_amount_for_image)


def get_query_for_wiki(message):
    bot.send_message(message.from_user.id, "Write your query...")
    bot.register_next_step_handler(message, show_wiki)


def show_wiki(message):
    mask = r"[А-Яа-яЁё]{1,}"  # russian check
    wiki = None

    if re.fullmatch(mask, message.text):
        wiki = wikipediaapi.Wikipedia("ru")
    else:
        wiki = wikipediaapi.Wikipedia("en")

    page = wiki.page(message.text)
    if page.exists():
        bot.send_message(message.from_user.id, page.summary)
    else:
        bot.send_message(message.from_user.id, "Page didn't.")
    menu(message)


def get_amount_for_image(message):

    global searchParams
    searchParams["q"] = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="1", callback_data="image1")
    keyboard.add(key_1)
    key_5 = types.InlineKeyboardButton(text="5", callback_data="image5")
    keyboard.add(key_5)
    key_10 = types.InlineKeyboardButton(text="10", callback_data="image10")
    keyboard.add(key_10)
    key_20 = types.InlineKeyboardButton(text="20", callback_data="image20")
    keyboard.add(key_20)
    key_50 = types.InlineKeyboardButton(text="50", callback_data="image50")
    keyboard.add(key_50)
    key_100 = types.InlineKeyboardButton(text="100", callback_data="image100")
    keyboard.add(key_100)
    bot.send_message(
        message.from_user.id, "Select amount of images...", reply_markup=keyboard
    )


def show_images(message):
    global searchParams, PATH_TO_DIR
    gis.search(search_params=searchParams, path_to_dir=PATH_TO_DIR)

    for image in gis.results():
        with open(image.path, "rb") as file:
            bot.send_photo(message.from_user.id, file)
        if os.path.exists(image.path):
            os.remove(image.path)
            print(
                "Image was sended and removed from temp storage: {}".format(image.path)
            )
    menu(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global searchParams, userFirstMessage
    if userFirstMessage == None:
        pass
    elif call.data == "image":
        get_query_for_image(userFirstMessage)
    elif call.data.find("image") != -1 and searchParams.get("q") != "!default!":
        amount = int(re.sub(r"image", "", call.data))
        searchParams["num"] = amount
        show_images(userFirstMessage)
    elif call.data == "wiki":
        get_query_for_wiki(userFirstMessage)


bot.polling(none_stop=True, interval=0)
print("Start working!")

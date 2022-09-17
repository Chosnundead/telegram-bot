import telebot
import re
import os
import wikipediaapi
import sqlite3 as sq
import pathlib
import json

# import random

from telebot import types
from google_images_search import GoogleImagesSearch

# import modules.tic_tac_toe as game

# Keys
bot = telebot.TeleBot("5655783257:AAGU6Mq_EAVMPTojKN8x2OnUjkCNHPMzzxI")
gis = GoogleImagesSearch("AIzaSyBcs9pkCQgKOmBcuV6Jte9V4JBgbsnEV4g", "8503f6ad0de1e4fa2")

# Constants
PATH_TO_TEMP = "{}temp\\".format(re.sub(r"bot.py", "", __file__))
PATH_TO_DB = "{}\\db\\users.db".format(pathlib.Path(__file__).parents[0])
DEFAULT_QUERYS = {
    "imageSearch": {
        "q": "!default!",
        "num": 0,
        "safe": "off",
        "fileType": "jpg",
        "imgSize": "xlarge",
    },
    "wikiSearch": "!default!",
    # "ticTacToe": {
    #     "state": False,
    #     "field": [[str(i + 3 * j) for i in range(1, 4)] for j in range(3)],
    #     "turn": 1,
    # },
}

# Create db if not exests
with sq.connect(PATH_TO_DB) as db:
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY,
        query TEXT
    )"""
    )


@bot.message_handler(content_types=["text", "document", "audio"])
def start(message):
    with sq.connect(PATH_TO_DB) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE id == {message.from_user.id}")
        user = cur.fetchone()
        if user == None:
            bot.send_message(message.from_user.id, "Hello, I'm your bot:)")
            cur.execute(
                "INSERT INTO users VALUES (?, ?)",
                (int(message.from_user.id), json.dumps(DEFAULT_QUERYS)),
            )
    menu(message)


def menu(message):
    key_image = types.InlineKeyboardButton(text="Image search", callback_data="image")
    key_wiki = types.InlineKeyboardButton(text="Wikipedia search", callback_data="wiki")
    # key_tic_tac_toe = types.InlineKeyboardButton(
    #     text="Tic Tac Toe", callback_data="ttt"
    # )
    keyboard = (
        types.InlineKeyboardMarkup()
        .add(key_image)
        .add(key_wiki)  # .add(key_tic_tac_toe)
    )
    bot.send_message(
        message.from_user.id, "Select a function from below.", reply_markup=keyboard
    )


def get_query_for_image(message):
    msg = bot.send_message(message.from_user.id, "Write your query...")
    bot.register_next_step_handler(msg, get_amount_for_image)


def get_query_for_wiki(message):
    msg = bot.send_message(message.from_user.id, "Write your query...")
    bot.register_next_step_handler(msg, show_wiki)


def show_wiki(message):
    with sq.connect(PATH_TO_DB) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE id == {message.from_user.id}")
        user = cur.fetchone()
        query = json.loads(user[1])
        query["wikiSearch"] = message.text
        cur.execute("REPLACE INTO users VALUES (?, ?)", (user[0], json.dumps(query)))
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
    with sq.connect(PATH_TO_DB) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE id == {message.from_user.id}")
        user = cur.fetchone()
        query = json.loads(user[1])
        query["imageSearch"]["q"] = message.text
        cur.execute("REPLACE INTO users VALUES (?, ?)", (user[0], json.dumps(query)))

    key_1 = types.InlineKeyboardButton(text="1", switch_inline_query_current_chat="1")
    key_5 = types.InlineKeyboardButton(text="5", switch_inline_query_current_chat="5")
    key_10 = types.InlineKeyboardButton(
        text="10", switch_inline_query_current_chat="10"
    )
    key_20 = types.InlineKeyboardButton(
        text="20", switch_inline_query_current_chat="20"
    )
    key_50 = types.InlineKeyboardButton(
        text="50", switch_inline_query_current_chat="50"
    )
    key_100 = types.InlineKeyboardButton(
        text="100", switch_inline_query_current_chat="100"
    )
    keyboard = (
        types.ReplyKeyboardMarkup()
        .row(key_1, key_5, key_10)
        .row(key_20, key_50, key_100)
    )
    bot.send_message(
        message.from_user.id, "Select amount of images...", reply_markup=keyboard
    )
    bot.register_next_step_handler(message, show_images)


def show_images(message):
    with sq.connect(PATH_TO_DB) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE id == {message.from_user.id}")
        user = cur.fetchone()
        query = json.loads(user[1])
        query["imageSearch"]["num"] = int(message.text)
        cur.execute("REPLACE INTO users VALUES (?, ?)", (user[0], json.dumps(query)))

        gis.search(search_params=query["imageSearch"], path_to_dir=PATH_TO_TEMP)

        for image in gis.results():
            with open(image.path, "rb") as file:
                bot.send_photo(message.from_user.id, file)
            if os.path.exists(image.path):
                os.remove(image.path)
                print(
                    "Image was sended and removed from temp storage: {}".format(
                        image.path
                    )
                )
    menu(message)


# def tic_tac_toe(call):
#     ttt = game.Game()
#     with sq.connect(PATH_TO_DB) as db:
#         cur = db.cursor()
#         cur.execute(f"SELECT * FROM users WHERE id == {call.from_user.id}")
#         user = cur.fetchone()
#         query = json.loads(user[1])
#         ttt.field = query["ticTacToe"]["field"]
#         if query["ticTacToe"]["turn"] % 2 == 0:
#             stop = False
#             while not stop:
#                 number = random.randint(1, 9)
#                 for arr in ttt.field:
#                     for item in arr:
#                         if item == str(number):
#                             item = str(number)
#                             stop = True
#                             break
#                     if stop:
#                         break
#             query["ticTacToe"]["turn"] += 1
#             if ttt.check() != "-" or query["ticTacToe"]["turn"] == 9:
#                 bot.send_message(call.from_user.id, ttt.check())
#                 menu(call)
#         elif query["ticTacToe"]["turn"] % 2 != 0:
#             stop = False
#             for arr in ttt.field:
#                 for item in arr:
#                     try:
#                         if item == call.text:
#                             item = call.text
#                             stop = True
#                             break
#                     except Exception:
#                         stop = True
#                 if stop:
#                     break
#             query["ticTacToe"]["turn"] += 1
#             if ttt.check() != "-" or query["ticTacToe"]["turn"] == 9:
#                 bot.send_message(call.from_user.id, ttt.check())
#                 menu(call)
#         keyboard = types.ReplyKeyboardMarkup()
#         for arr in ttt.field:
#             for item in arr:
#                 key = types.InlineKeyboardButton(
#                     text=item, switch_inline_query_current_chat=item
#                 )
#                 keyboard.add(key)
#             keyboard.row()
#         cur.execute("REPLACE INTO users VALUES (?, ?)", (user[0], json.dumps(query)))
#     msg = bot.send_message(call.from_user.id, "Your turn.", reply_markup=keyboard)
#     bot.register_next_step_handler(msg, tic_tac_toe)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    with sq.connect(PATH_TO_DB) as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE id == {call.from_user.id}")
        user = cur.fetchone()
        if user == None:
            pass
        elif call.data == "image":
            get_query_for_image(call)
        elif call.data == "wiki":
            get_query_for_wiki(call)
        # elif call.data == "ttt":
        #     tic_tac_toe(call)


bot.polling(none_stop=True, interval=0)

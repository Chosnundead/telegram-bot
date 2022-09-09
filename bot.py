import telebot
from google_images_search import GoogleImagesSearch

bot = telebot.TeleBot("5655783257:AAGU6Mq_EAVMPTojKN8x2OnUjkCNHPMzzxI")

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch("AIzaSyBcs9pkCQgKOmBcuV6Jte9V4JBgbsnEV4g", "8503f6ad0de1e4fa2")

# define search params
# option for commonly used search param are shown below for easy reference.
# For param marked with '##':
#   - Multiselect is currently not feasible. Choose ONE option only
#   - This param can also be omitted from _search_params if you do not wish to define any value
# _search_params = {
#     "q": "...",
#     "num": 10,
#     "fileType": "jpg|gif|png",
#     "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
#     "safe": "active|high|medium|off|safeUndefined",  ##
#     "imgType": "clipart|face|lineart|stock|photo|animated|imgTypeUndefined",  ##
#     "imgSize": "huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined",  ##
#     "imgDominantColor": "black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined",  ##
#     "imgColorType": "color|gray|mono|trans|imgColorTypeUndefined",  ##
# }

# this will only search for images:
# gis.search(search_params=_search_params)

# this will search and download:
# gis.search(search_params=_search_params, path_to_dir="/path/")

# this will search, download and resize:
# gis.search(search_params=_search_params, path_to_dir="/path/", width=500, height=500)

# search first, then download and resize afterwards:
# gis.search(search_params=_search_params)
# for image in gis.results():
# image.url # image direct url

# image.referrer_url  # image referrer url (source)

# image.download("/path/")  # download image
# image.resize(500, 500)  # resize downloaded image

# image.path  # downloaded local file path

searchParams = {"q": "...", "num": 0, "safe": "off", "fileType": "jpg"}
isFirst = True


@bot.message_handler(content_types=["text", "document", "audio"])
def start(message):
    # if message.text == "Привет":
    #     bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    # elif message.text == "/help":
    #     bot.send_message(message.from_user.id, "Напиши привет")
    # else:
    #     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    global isFirst
    if isFirst:
        bot.send_message(
            message.from_user.id,
            "Hello, I'm your search-pic bot. Write your requst...",
        )
        isFirst = False
    else:
        bot.send_message(message.from_user.id, "Write your requst...")

    bot.register_next_step_handler(message, get_request)


def get_request(message):
    global searchParams
    searchParams["q"] = message.text
    bot.send_message(message.from_user.id, "Write amount of images...")
    bot.register_next_step_handler(message, get_amount)


def get_amount(message):
    # keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    #   key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    #   keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    #   key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    #   keyboard.add(key_no);
    #   question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
    #   bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    global searchParams
    try:
        searchParams["num"] = int(message.text)
    except:
        bot.send_message(message.from_user.id, "Please, write a NUMBER.")
        bot.register_next_step_handler(message, get_request)
    else:
        gis.search(search_params=searchParams)
        for image in gis.results():
            bot.send_message(message.from_user.id, image.url)
        bot.register_next_step_handler(message, start)


bot.polling(none_stop=True, interval=0)

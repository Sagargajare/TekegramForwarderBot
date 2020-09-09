import pickle
import re
from pprint import pprint

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN, adminId


def add_channel(name, id):
    with open("channel1.pickle", "rb") as file:
        data = pickle.load(file)
    data[id] = name
    with open("channel1.pickle", "wb") as file:
        pickle.dump(data, file)


def add_record(mod):
    if "src-" in mod:
        mod = re.findall(r"(-[0-9]+)", mod)[0]
        print(mod)

        with open("src.pkl", "rb") as file:
            data = pickle.load(file)
        data.append(mod)
        with open("src.pkl", 'wb') as file:
            pickle.dump(data, file)
        res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={adminId}&text=New Source added")
    if "des-" in mod:
        mod = re.findall(r"(-[0-9]+)", mod)[0]
        print(mod)

        with open("des.pkl", "rb") as file:
            data = pickle.load(file)
        data.append(mod)
        with open("des.pkl", 'wb') as file:
            pickle.dump(data, file)
        res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={adminId}&text=New Destination added")


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def custom_message(update, context):
    update.message.reply_text(
        'custom_message')


def add_source(update, context):
    update.message.reply_text(
        'add_source')


def add_destination(update, context):
    update.message.reply_text(
        'add_destination')


def destinations(update, context):
    with open("des.pkl", 'rb') as file:
        des_ids = pickle.load(file)
    data1 = []
    with open("channel1.pickle", "rb") as file1:
        channel_dict = pickle.load(file1)
    print(channel_dict)
    for i in des_ids:
        print(i)
        data1.append(channel_dict[int(i)])

    msg = "\n".join(data1)
    data1 = []
    update.message.reply_text(
        msg)


def sources(update, context):
    with open("src.pkl", 'rb') as file:
        src_ids = pickle.load(file)
    data1 = []
    with open("channel1.pickle", "rb") as file1:
        channel_dict = pickle.load(file1)
    print(channel_dict)
    for i in src_ids:
        print(i)
        data1.append(channel_dict[int(i)])

    msg = "\n".join(data1)
    data1 = []
    update.message.reply_text(
        msg)


def forwarder(update, context):
    print(update)
    if update["channel_post"]:
        id = update["channel_post"]["chat"]["id"]
        with open('des.pkl', "rb") as file:
            des = pickle.load(file)
            # print(des)
        with open('src.pkl', "rb") as file:
            src = pickle.load(file)
            # print(src)
        if id not in des and f'{id}' not in src:
            print("not found")
            title = update["channel_post"]["chat"]["title"]
            alert = f'''{title} is not configured with 
                    any source or destination having id {id}
                    to add it as source send "src{id}" to bot
                    to add it destination send "des{id}" to bot'''
            add_channel(id, title)
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={adminId}&text={alert}")
            print("msg sent")
            return

        msg = update["channel_post"]["text"]

        print(update)
        for i in des:
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={i}&text={msg}")
    if update["message"] and str(update["message"]["chat"]["id"]) == adminId:
        modifiaction = update["message"]["text"]
        a = add_record(modifiaction)
        print(modifiaction)


# https://api.telegram.org/bot1317360640:AAG0DJ80ycM0UwpCkgxoIsW9NVlKby5C6GU/sendMessage?chat_id=-1001278649804&text=forwarded
updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('custom_message', custom_message))
updater.dispatcher.add_handler(CommandHandler('add_source', add_source))
updater.dispatcher.add_handler(CommandHandler('add_destination', add_destination))
updater.dispatcher.add_handler(CommandHandler('destinations', destinations))
updater.dispatcher.add_handler(CommandHandler('sources', sources))
updater.dispatcher.add_handler(MessageHandler(Filters.all, forwarder))
updater.start_polling()
updater.idle()

from glob import glob
from random import choice
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def get_contact(bot, update,user_data):
    print(update.message.contact)
    

def get_location(bot, update,user_data):
    print(update.message.location)
    

def change_avatar(bot, update,user_data):
    if 'emo' in user_data:
        del user_data['emo']
    update.message.reply_text(f'Готово, {get_user_emo(user_data)}')


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def send_cat(bot, update, user_data):
    cat_list = glob('cats/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())
    print(cat_pic)


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку'],
                                       [contact_button, location_button]
                                       ], resize_keyboard=True
                                     )
    return my_keyboard
    

def greet_user(bot, update, user_data):
    update.message.reply_text(f'Привет {get_user_emo(user_data)}', reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f"Привет! {update.message.chat.first_name} {emo} Ты написал: {update.message.text}"
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Бот запущен')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()

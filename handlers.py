from glob import glob
from random import choice
import logging

from utils import get_keyboard, get_user_emo


def get_contact(bot, update,user_data):
    print(update.message.contact)
    

def get_location(bot, update,user_data):
    print(update.message.location)
    

def change_avatar(bot, update,user_data):
    if 'emo' in user_data:
        del user_data['emo']
    update.message.reply_text(f'Готово, {get_user_emo(user_data)}')

                
def send_cat(bot, update, user_data):
    cat_list = glob('cats/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())
    print(cat_pic)


def greet_user(bot, update, user_data):
    update.message.reply_text(f'Привет {get_user_emo(user_data)}', reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f"Привет! {update.message.chat.first_name} {emo} Ты написал: {update.message.text}"
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')
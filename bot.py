import telebot
import lang
import random
from telebot import types as tgp
from config import TOKEN

user_messanger = {}
user_find = []

bot = telebot.TeleBot(TOKEN)

def find_user():
	if len(user_find) == 0:
		return [False, 0]
	return [True, random.choice(user_find)]

def connection_user(chat_user1, chat_user2):
	bot.send_message(chat_id=chat_user1,text=lang.CONNECTION)
	bot.send_message(chat_id=chat_user2,text=lang.CONNECTION)
	user_messanger[chat_user1] = chat_user2
	user_messanger[chat_user2] = chat_user1
	user_find.remove(chat_user2)

def disconnection_user(chat_user1):
	chat_user2 = user_find[chat_user1]
	bot.send_message(chat_id=chat_user1, text=lang.DISCONNECTION_YOU)
	bot.send_message(chat_id=chat_user2, text=lang.DISCONNECTION_USER)
	user_messanger.pop(chat_user1)
	user_messanger.pop(chat_user2)


def keyboard_gen(buttons: list) -> tgp.ReplyKeyboardMarkup:
    markup = tgp.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for button in buttons: markup.add(tgp.KeyboardButton(button))
    return markup

@bot.message_handler(commands=["start"])
def send_hello(message: tgp.Message):
        bot.send_message(chat_id=message.chat.id, text=lang.GREETINGS, reply_markup=keyboard_gen([lang.FIND_BUTTON]))

@bot.message_handler(commands=["find"])
def send_find(message: tgp.Message):
	bot.send_message(chat_id=message.chat.id, text=lang.FIND_USER, reply_markup=ReplyKeyboardRemove())
	find_results = find_user()
	if find_results[0]:
		connection_user(message.chat.id, find_results[1])
	else:
		user_find.append(message.chat.id)

@bot.message_handler(content_types=["text"])l
def event_detector_text(message: tgp.Message):
	if message.text == lang.FIND_BUTTON:
		send_find(message)
		return
	if message.text == lang.DISCONNECTION_BUTTON:
		disconnection_user(message.chat.id)
		return
	if message.chat.id in user_messanger:
		bot.send_message(chat_id=user_messanger[message.chat.id], text=message.text, reply_markup=keyboard_gen([lang.DISCONNECTION_BUTTON]))

bot.polling()

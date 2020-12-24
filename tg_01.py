# coding=UTF-8

import telebot
import telegram
import json
from collections import Counter
import os
import time

bot = telebot.TeleBot('1438173397:AAFHadsCXIkxJt_bRq0z97gK4uDkFwgOVgo')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('/Hosts', '/Добавить', '/Назад')
keyboard1.row('/start', '/info', '/Hosts')

host_list = []

#Обработка ошибки считывания ID пользователя из файла
try:
	with open('personID') as idset:
		person_id = idset.readline()
except Exception:
	with open('personID', 'w') as idset:
		person_id = 0

#Функция для работы с хостами
def rewr(a):
	with open('host_list') as hosts:
		for host in hosts:
			a.append(host.strip())

# Перезапись списка host_list из файла
rewr(host_list)

#Получение ID пользователя для его последующей передачи файлу personID
def getid(a):
	global person_id
	if person_id != a.chat.id:
		with open('personID', 'w') as setter:
			setter.write(str(a.chat.id))
		person_id = a.chat.id

@bot.message_handler(commands=['start'])
def start_message(message):
	getid(message)
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start, а значит ты готов опробовать новую крутую приложуху от офигенской команды инфобезников из ГЭУ.', reply_markup=keyboard1)
	print(message)

@bot.message_handler(commands=['info'])
def info_message(message):
	getid(message)
	bot.send_message(message.chat.id, 'Бот позволяет получать информацию об открытых портах на твоём компьютере, а так же отслеживать изменения, связанные со списокм открытых портов на конкретный хост :)', reply_markup=keyboard1)
	print(message)

#Вывод списка хостов, переключение на вторую вкладку кнопок (с возможностью добавления хоста)
@bot.message_handler(commands=['Hosts'])
def HostList_hosts(message):
	getid(message)
	host_list = []
	rewr(host_list)
	s = ''
	for i in host_list:
		s+=i+'\n'
	bot.send_message(message.chat.id, f'Твой хост лист: \n{s}', reply_markup=keyboard2)
	print(message)

#Переход со второй вкладки кнопок на первую
@bot.message_handler(commands=['Назад'])
def HostList_back(message):
	getid(message)
	bot.send_message(message.chat.id, 'Назад', reply_markup=keyboard1)
	# print(message)

@bot.message_handler(commands=['Добавить'])
def HostList_change(message):
	getid(message)
	bot.send_message(message.chat.id, 'Введи новый хост: или напиши "Отмена"')
	print(message)

# Обработка сообщений: порт (для добавления в список портов), "Хост "порт"" - для выбора хоста как отслеживаемого, обработка некорректного ввода через else
@bot.message_handler(content_types=['text'])
def common_text(message):
	getid(message)
	# print(str(message.text[:5]), message.text[5:], end='\n')
	rewr(host_list)
	if message.text.count('.') == 3 and message.text.count(' ') == 0:
		c = Counter(host_list)
		d = dict(c)
		if message.text in d.keys() and d[message.text] >= 1:
			bot.send_message(message.chat.id, 'А хост уже есть в этом списке...', reply_markup=keyboard2)
			print(message)
		else:
			with open('host_list', 'a') as hosts:
				hosts.write('\n')
				hosts.write(message.text)
			bot.send_message(message.chat.id, 'Готово!', reply_markup=keyboard2)
			print(message)

	elif message.text == "Отмена":
		bot.send_message(message.chat.id, 'Окей, отменим ввод...')
		print(message)

	else:
		bot.send_message(message.chat.id, 'Так, я не понял, чего ты хотел...Может ты попробуешь написать "Отмена" или почитать, что требуется от тебя в текущий момент?')
		print(message)

if __name__ == "__main__":
	bot.polling(none_stop=True, timeout=500)

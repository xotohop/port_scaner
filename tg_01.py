import telebot
import telegram
import json
import os
import time

bot = telebot.TeleBot('')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('/Hosts', '/Добавить', '/Назад')
keyboard1.row('/start', '/info')
keyboard1.row('/Hosts', '/Отслеживать')
host_list = []
port_list = []
person_id = 1

#Функция для работы с хостами
def rewr(a):
	with open('host_list') as hosts:
		for host in hosts:
			a.append(host.strip())
#Функция для работы с портами (пока не используется)
def rewrp(a):
	with open('port_list') as ports:
		for port in ports:
			a.append(port.strip())

rewr(host_list)
# rewrp(port_list)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, 'Привет, ты написал мне /start, а значит ты готов опробовать новую крутую приложуху от офигенской команды инфобезников из ГЭУ.', reply_markup=keyboard1)
    print(message)

@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, 'Ох...ну, если коротко, то бот позволяет получать информацию об открытых портах на твоём компьютере, а так же отслеживать изменения, связанные со списокм открытых портов на конкретный хост :)', reply_markup=keyboard1)
    print(message)

#Вывод списка хостов, переключение на вторую вкладку кнопок (с возможностью добавления хоста)
@bot.message_handler(commands=['Hosts'])
def HostList_hosts(message):
	host_list = []
	rewr(host_list)
	s = ''
	for i in host_list:
		s+=i+'\n'
	bot.send_message(message.chat.id, f'Твой хост лист: \n{s}', reply_markup=keyboard2)
	print(message)

# Пока неиспользуемая команда на работу со списком портов
'''
@bot.message_handler(commands=['Ports'])
def HostList_hosts(message):
	port_list = []
	rewrp(port_list)
	s = ''
	for i in port_list:
		s += i+'\n'
	bot.send_message(
		message.chat.id, f'Твой порт лист: \n{s}', reply_markup=keyboard3)
	print(message)
'''

#Переход со второй вкладки кнопок на первую
@bot.message_handler(commands=['Назад'])
def HostList_back(message):
	bot.send_message(message.chat.id, 'Назад', reply_markup=keyboard1)
	# print(message)

@bot.message_handler(commands=['Добавить'])
def HostList_change(message):
	bot.send_message(message.chat.id, 'Окей, введи новый хост: или напиши "Отмена"')
	print(message)


# Пока неиспользуемая функция добавления порта
'''
@bot.message_handler(commands=['Добавить порт'])
def HostList_change(message):
	bot.send_message(
		message.chat.id, 'Окей, введи слово "порт", а потом - номер интересующего тебя порта. Или напиши "Отмена"')
	print(message)
'''

#Заготовка неработающей функции (пока что реализуется в файле scan_threading.py)
def sendinfo(s: str):
	bot.send_message(message.chat.id, 'Обновилась инфа по отслеживаемому хосту! \n{s}')
	print(message)

# Функция для получения ID, пользователя, которому будет отправляться информация об изменении
def getmsgid():
	return person_id


@bot.message_handler(commands=['Отслеживать'])
def set_target(message):
	person_id = message.chat.id
	bot.send_message(message.chat.id, 'Окей, введи сначала слово "Хост" а потом его номер, через пробел или напиши "Отмена" (вводимый хост должен быть в списке хостов! (клавиша Host -> Добавить)', reply_markup=keyboard1)
	print(message)

# Обработка сообщений: порт (для добавления в список портов), "Хост "порт"" - для выбора хоста как отслеживаемого, обработка некорректного ввода через else
@bot.message_handler(content_types=['text'])
def HostList_text(message):
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

	elif message.text[:5] == 'Хост ' and message.text[5:] in host_list:
		with open('f_host', 'w') as host:
			host.write(f'{message.chat.id} {message.text[5:]}\n')
		bot.send_message(message.chat.id, 'Готово!', reply_markup=keyboard1)
		print(message)

	elif message.text[:5] == 'Хост ' and message.text[5:] not in host_list:
		bot.send_message(message.chat.id, 'Я понял, чего ты хочешь, но у тебя проблема с хостом: его или нет в списке хостов, или ты неверно его ввёл...', reply_markup=keyboard1)
		print(message)

	else:
		bot.send_message(message.chat.id, 'Так, я не понял, чего ты хотел...Может ты попробуешь написать "Отмена" или почитать, что требуется от тебя в текущий момент?')
		print(message)

if __name__ == "__main__":
	bot.polling(none_stop=True, timeout=500)

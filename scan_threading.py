# coding=UTF-8

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import sys
import time
import telebot
import os
import argparse
from datetime import datetime
from dbHelper import ScansDatabase

bot = telebot.TeleBot('1438173397:AAFHadsCXIkxJt_bRq0z97gK4uDkFwgOVgo')

# сохраняем вывод по-умолчанию (т.е. в консоль)
stdout_fileno = sys.stdout
# переводим вывод в файл output
sys.stdout = open('output_temp', 'w')


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostlist', default='host_list', type=open)
    parser.add_argument('-P', '--portlist', default='port_list', type=open)
    return parser


# параметры: time, host, port
def scan(t, h, p):
    try:
        # создаем IP/TCP сокет
        sock = socket(AF_INET, SOCK_STREAM)
        # время попытки соединения - 0.5 сек
        sock.settimeout(0.5)
    # ошибка возникает в случе нехватки ресурсов для потоков
    except OSError:
        pass
    else:
        try:
            conn = sock.connect((h, int(p)))
            print(t, end=',')
            print(h, end=',')
            print(p, end='\n')
            conn.close()
        # не удалось подключится или время истекло
        except Exception:
            pass


now = str(datetime.now())

database = ScansDatabase()

parser = createParser()
namespace = parser.parse_args()

host_list = []
port_list = []

for host in namespace.hostlist:
    host_list.append(host.strip())

for port in namespace.portlist:
    port_list.append(port.strip())

# закрываем файлы со списками хостов и портов
namespace.hostlist.close()
namespace.portlist.close()

for h in host_list:
    for p in port_list:
        # создаем и запускаем потоки
        thread = Thread(target=scan, kwargs=({'t': now, 'h': h, 'p': p}))
        thread.start()

# ждем завершения работы всех потоков
thread.join()

# закрываем файл output
sys.stdout.close()
# возвращаем вывод в консоль
sys.stdout = stdout_fileno

curr_data = [[now, '1', -1]]

with open('output_temp') as output:
    for line in output:
        lst = line.split(sep=',', maxsplit=3)
        curr_data.append([lst[0], lst[1], int(lst[2].strip())])

for host in host_list:
    print('Хост:', host)
    tmp_data = []
    for item in curr_data:
        if host in item:
            tmp_data.append(item)
    print(database.compare(host, tmp_data))
    print()


#Получение из файла ID пользователя, формирование сообщений об изменении портов с последней работы скрипта, отправка в чат-бот
def SendNotification():
	with open('personID') as ff:
		PersonID = ff.readline()
	bot.send_message(PersonID, 'Обновилась информация по отслеживаемым хостам:')
	a = ''
	for i in host_list:
		a = str(f'Хост {i}:\n' + database.compare(i, [b for b in curr_data if curr_data[1] == i]))
		bot.send_message(PersonID, a)
		time.sleep(1)

SendNotification()

database.insertData(curr_data)

os.remove('output_temp')

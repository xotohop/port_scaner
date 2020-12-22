# coding=UTF-8

from socket import *
from threading import *
import sys
import time
import telebot
import os
from tg_01 import sendinfo, getmsgid
import argparse
from datetime import datetime
import sqlite3
import dbHelper

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
        # создаем
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

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()
dbHelper.createDB(c, conn)

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

# data = dbHelper.getData(c, conn)

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
    print(dbHelper.compare(c, conn, host, tmp_data))
    print()


# новый, добавленный и УЖЕ работющий кусок кода, для отправки сообщения
def SendNotification():
	with open('f_host') as ff:
		PersonID = ff.readline()
	bot.send_message(PersonID, 'Подъехала инфа по твоим хостам, суччара! :D')
	a = ''
	for i in host_list:
		a = str(f'Хост {i}:\n' + dbHelper.compare(c, conn, i, [b for b in curr_data if curr_data[1] == i]))
		bot.send_message(PersonID, a)
		time.sleep(1)

SendNotification()

dbHelper.insertData(c, conn, curr_data)

os.remove('output_temp')

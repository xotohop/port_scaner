import socket
import threading
import sys
import telebot
import os
from tg_01 import sendinfo, getmsgid
from datetime import datetime
import sqlite3
import dbHelper

bot = telebot.TeleBot('1438173397:AAHA9tBrGDzxFfb5cgNT47Qd7ED1c4ID000')
stdout_fileno = sys.stdout # сохраняем вывод по-умолчанию
sys.stdout = open('output_temp', 'w') # переводим вывод в файл output

def scan(time, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5) # время попытки соединения - 0.5 сек
    try:
        conn = sock.connect((host, int(port)))
        print(time, end = ',')
        print(host, end = ',')
        print(port, end = '\n')
        conn.close()
    except:
        pass

now = str(datetime.now())

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()
dbHelper.createDB(c, conn)

host_list = []

with open('host_list') as hosts:
    for host in hosts:
        host_list.append(host.strip())

for host in host_list:
    with open('port_list') as ports:
        for port in ports:
            thread = threading.Thread(target = scan, kwargs = ({'time': now, 'host': host.strip(), 'port': port.strip()})) # создаем и
            thread.start()                                                                                                 # запускаем потоки
thread.join() # ждем завершения работы всех потоков

sys.stdout.close() # закрываем файл output
sys.stdout = stdout_fileno # возвращаем вывод в консоль

# data = dbHelper.getData(c, conn)

curr_data = [[now, '1', -1]]

with open('output_temp') as output:
    for line in output:
        lst = line.split(sep = ',', maxsplit = 3)
        curr_data.append([lst[0], lst[1], int(lst[2].strip())])

for host in host_list:
    # print('Хост:', host)
    tmp_data = []
    for item in curr_data:
        if host in item:
            tmp_data.append(item)
    # print(dbHelper.compare(c, conn, host, tmp_data))
    # print()


#Новый, добавленный и пока не работющий кусок кода, для отправки сообщения
def SendNotification():
	with open('f_host') as f:
		for line in f:
			if line.split() != '':
				target = line
	tt = target.split(' ')[1]
	# print(target.split(' '))
	b = [i for i in curr_data if i[1] == tt]
	a = dbHelper.compare(c, conn, tt, b)

	# print(a)
	# if a!='\nИзменений с последнего сканирования не обнаружено.':
	bot.send_message(target.split(' ')[0], a)
SendNotification()
dbHelper.insertData(c, conn, curr_data)
os.remove('output_temp')

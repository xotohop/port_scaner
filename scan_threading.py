# coding=UTF-8

import socket
import threading
import sys
import os
import argparse
from datetime import datetime
import sqlite3
import dbHelper

stdout_fileno = sys.stdout  # сохраняем вывод по-умолчанию
sys.stdout = open('output_temp', 'w')  # переводим вывод в файл output


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostlist', default='host_list')
    parser.add_argument('-P', '--portlist', default='port_list')
    return parser


def scan(time, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  # время попытки соединения - 0.5 сек
    try:
        conn = sock.connect((host, int(port)))
        print(time, end=',')
        print(host, end=',')
        print(port, end='\n')
        conn.close()
    except:
        pass


now = str(datetime.now())

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()
dbHelper.createDB(c, conn)

parser = createParser()
namespace = parser.parse_args()

host_list = []

with open('{}'.format(namespace.hostlist)) as hosts:
    for host in hosts:
        host_list.append(host.strip())

for host in host_list:
    with open('{}'.format(namespace.portlist)) as ports:
        for port in ports:
            thread = threading.Thread(target=scan, kwargs=({'time': now, 'host': host.strip(), 'port': port.strip()}))  # создаем потоки
            thread.start()  # запускаем потоки
thread.join()  # ждем завершения работы всех потоков

sys.stdout.close()  # закрываем файл output
sys.stdout = stdout_fileno  # возвращаем вывод в консоль

data = dbHelper.getData(c, conn)

curr_data = [[now, '1', -1]]

with open('output_temp') as output:
    for line in output:
        lst = line.split(sep=',', maxsplit=3)
        curr_data.append([lst[0], lst[1], int(lst[2].strip())])

for host in host_list:
    print('host:', host)
    tmp_data = []
    for item in curr_data:
        if host in item:
            tmp_data.append(item)
    print(dbHelper.compare(c, conn, host, tmp_data))
    print()

dbHelper.insertData(c, conn, curr_data)

os.remove('output_temp')

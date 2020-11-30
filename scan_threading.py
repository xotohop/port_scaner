import socket
import threading
import sys
import os
from datetime import datetime
import sqlite3
import dbHelper

sys.stdout = open('output', 'w')

def scan(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        conn = sock.connect((host, port))
        print(host + ':' + str(port))
        conn.close()
    except:
        pass

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()
dbHelper.createDB(c, conn)

now = str(datetime.now())

with open('host_list') as hosts:
    for host in hosts:
        with open('port_list') as ports:
            for port in ports:
                thread = threading.Thread(target=scan, kwargs=({'host': host.strip(), 'port': int(port.strip())}))
                thread.start()

sys.stdout.close()

with open('output') as output:
    for line in output:
        dbHelper.insertData(c, conn, [[now, line.strip()]])

os.remove('output')

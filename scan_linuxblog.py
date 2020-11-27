import socket
import threading
from datetime import datetime

def scan(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        conn = sock.connect((host, port))
        print(port, ' open')
        conn.close()
    except:
        pass

start = datetime.now()

host1 = '127.0.0.1' # localhost

host2 = '45.33.32.156' # scanme.nmap.org

ports = []

for port in range(65536):
    ports.append(port)

for port in ports:
    thread = threading.Thread(target=scan, kwargs=({'host': host2, 'port': port}))
    thread.start()

ends = datetime.now()
print('Time: {}'.format(ends - start))

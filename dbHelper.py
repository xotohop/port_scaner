import sqlite3
from datetime import datetime

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()

# в БД сохраняются только время и открытые порты.
def createDB(c, conn):
    c.execute('''CREATE TABLE IF NOT EXISTS scans (date DATE, host TEXT, port INTEGER, PRIMARY KEY (date, host, port));''')
    conn.commit()

def getData(c, conn, startDate: str = '2000', endDate: str = '5000', hosts: list = [], ports: list = []):
    print('\n***Открытые порты***\n')
    if (ports != []):
        portsList = f' AND port in ({", ".join(str(k) for k in ports)})'
    else:
        portsList = ''

    if (hosts != []):
        hostList = ' AND host in (' + ", ".join("'{}'".format(k) for k in hosts) + ')'
    else:
        hostList = ''
    
    return c.execute(f'SELECT * FROM scans WHERE {startDate} <= date <= {endDate}{hostList}{portsList};')


# При добавленнии надо сделать первый элемент списка с текущим временем и портом -1. Так можно понять, что в это время было сканирование.
# Это на случаи, если при сканировании не будет открытых портов (вернется пустой список -> ничего не добавится в БД), но не было открытых портов.
def insertData(c, conn, listOfData: list):
    for item in listOfData:
        c.execute("insert OR REPLACE into scans values (?, ?, ?);", (item[0], item[1], item[2]))
    conn.commit()

def compare(c, conn, host: str, listOfData: list):
    chages = []
    c.execute(f"""SELECT * FROM scans WHERE date = (SELECT MAX(date) FROM scans GROUP BY host HAVING date = '{host}') AND host = '{host}';""")
    previousData = c.fetchall()
    for item in previousData:
        # print(list(item))
        if (list(item) in listOfData):
            listOfData.remove(list(item))
        else:
            chages.append(list(item))
    if (chages == [] and listOfData == []):
        return f'\nИзменений с последнего сканирования не обнаружено.'
    if (chages != [] and listOfData != []):
        return f'\nСписок портов, которые открылись после прошлого сканирования:\n{listOfData}.\nСписок портов которые закрылись после прошлого сканирования:\n{chages}.'
    if(listOfData != []):
        return f'\nСписок портов, которые были закрыты при прошлом сканировании:\n{listOfData}.'
    else:
        return f'\nСписок портов которые закрылись после прошлого сканирования:\n{chages}.'


# Пример использования
# createDB(c, conn)

# now = str(datetime.now())[:10]

# insertData(c, conn, [[now, '1', -1], [now, '45.33.32.1576', 1], [now, '45.33.32.156', 2], [now, '216.58.210.174', 3], [now, '45.33.32.156', 4]]) ###Не забывать добавлять значение -1 после каждого сканирования

# data = getData(c, conn, ports=[1, 2, 3, 5], hosts=['45.33.32.156', '216.58.210.174', '45.33.32.1576'], startDate="2020-12-02", endDate="2020-12-03") #Время не получается сравнить ((((

# for item in data:
#     print(item)


# data2 = compare(c, conn, host='45.33.32.156', listOfData=[[now, '45.33.32.156', 2]])

# print(data2)
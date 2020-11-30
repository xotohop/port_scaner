import sqlite3
from datetime import datetime

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()

# в БД сохраняются только время и открытые порты.
def createDB(c, conn):
    c.execute('''CREATE TABLE IF NOT EXISTS scans
            (date DATETIME, ports TEXT)''')
    conn.commit()

def getData(c, startDate: str = '2000', endDate: str = '5000'):
    print('\n***Открытые порты***\n')
    return c.execute(f'SELECT * FROM scans WHERE {startDate} <= date <= {endDate}')

def getPortInfo(c, port: int, startDate: str = '2000', endDate: str = '5000'):
    print(f'\n***Информация о порте №{port}***\n')
    return c.execute(f'SELECT * FROM scans WHERE {startDate} <= date <= {endDate} AND port = {port}')

# При добавленнии надо сделать первый элемент списка с текущим временем и портом -1. Так можно понять, что в это время было сканирование.
# Это на случаи, если при сканировании не будет открытых портов (вернется пустой список -> ничего не добавится в БД), но не было открытых портов.
def insertData(c, conn, listOfData: list):
    for item in listOfData:
        c.execute("insert into scans values (?, ?)", (item[0], item[1]))
    conn.commit()


# Пример использования
    # createDB(c, conn)

    # now = str(datetime.now())

    # insertData([[now, -1], [now, 1], [now, 2], [now, 3], [now, 4]]) ###Не забывать добавлять значение -1 после каждого сканирования

    # data = getData()

    # for item in data:
    #     print(item)


    # data2 = getPortInfo(100)

    # for item in data2:
    #     print(item)

conn.close()
import sqlite3
from datetime import datetime

class ScansDatabase():
    # Инициализация
    def __init__(self):
        self.connection = sqlite3.connect('scan_results.db')
        self.cur = self.connection.cursor()
        # При каждой инициализации будет вызван метод create_table(), который предотвратит ошибку, если таблица со сканами
        # удалена или еще не была создана
        self.create_table()

    # Создать таблицу со сканами
    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS scans (
                            date DATETIME, 
                            host TEXT, 
                            port INTEGER, 
                            PRIMARY KEY (date, host, port))''')
        self.connection.commit()

    # Получить данные из таблицы. Можно получить информациюю за определенную 
    # дату или по определенным хостам / портам
    def getData(self, 
                startDate: str = '2000', 
                endDate: str = '5000', 
                hosts: list = [], 
                ports: list = []):
        if (ports != []):
            portList = f' AND port in ({", ".join(str(k) for k in ports)})'
        else:
            portList = ''

        if (hosts != []):
            hostList = ' AND host in (' + ", ".join("'{}'".format(k) for k in hosts) + ')'
        else:
            hostList = ''
        return self.cur.execute(f"""SELECT * FROM scans 
                                    WHERE datetime('{startDate}') <= date <= datetime('{endDate}')
                                    {hostList}{portList};""")

    # Запись данных в БД
    def insertData(self, listOfData: list):
        for item in listOfData:
            self.cur.execute("insert OR REPLACE into scans values (?, ?, ?);", (item[0], item[1], item[2]))
        self.connection.commit()

    # сравнение текущих данных с последней записью в БД
    def compare(self, host: str, currentData: list):
        chages = []
        self.cur.execute(f"""SELECT host, port FROM scans 
                            WHERE date = (SELECT MAX(date) FROM scans WHERE host = '{host}') 
                            AND host = '{host}';""")
        previousData = self.cur.fetchall()
        for item in previousData:
            flag = False
            for i in currentData:
                if (i[1:] == list(item)):
                    flag = True
                    currentData.remove(i)
            if (flag == False):
                chages.append(list(item))
        if (chages == [] and currentData == []):
            return f'\nИзменений с последнего сканирования не обнаружено.'

        if (chages != [] and currentData != []):
            return f'''\nСписок портов, которые открылись после прошлого сканирования:\n{currentData}.
                        \nСписок портов которые закрылись после прошлого сканирования:\n{chages}.'''

        if(currentData != []):
            return f'\nСписок портов, которые были закрыты при прошлом сканировании:\n{currentData}.'

        else:
            return f'\nСписок портов которые закрылись после прошлого сканирования:\n{chages}.'

    def __del__(self):
        self.close()

    #Закрытие соединения с БД
    def close(self):
        self.connection.close()


# Пример:

db = ScansDatabase()

now = str(datetime.now())

db.insertData([[now, '1', -1], [now, '45.33.32.1576', 1], [now, '45.33.32.156', 2], [now, '216.58.210.174', 3], [now, '45.33.32.156', 4]])

print(db.compare(host='45.33.32.156', currentData=[[now, '45.33.32.156', 2], [now, '45.33.32.156', 13]]))

print()
for i in db.getData():
    print(i)

# Список портов, которые открылись после прошлого сканирования:
# [['2020-12-24 15:51:04.002335', '45.33.32.156', 13]].
# Список портов которые закрылись после прошлого сканирования:
# [['45.33.32.156', 4]].

# ('2020-12-24 15:49:55.129851', '1', -1)
# ('2020-12-24 15:49:55.129851', '45.33.32.1576', 1)
# ('2020-12-24 15:49:55.129851', '45.33.32.156', 2)
# ('2020-12-24 15:49:55.129851', '216.58.210.174', 3)
# ('2020-12-24 15:49:55.129851', '45.33.32.156', 4)

import sqlite3
import dbHelper


conn = sqlite3.connect('scan_results.db')
c = conn.cursor()
dbHelper.createDB(c, conn)
data = dbHelper.getData(c, conn, ports=[1, 2, 3, 5], hosts=['45.33.32.156', '216.58.210.174', '45.33.32.1576'], startDate="2020-12-03 17:45:46.797540", endDate="2020-12-03 17:45:46.797540")

for i in data:
	print(i)

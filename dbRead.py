import sqlite3
import dbHelper


conn = sqlite3.connect('scan_results.db')
c = conn.cursor()

dbHelper.createDB(c, conn)

data = dbHelper.getData(c, conn)
for item in data:
    print(item)


import sqlite3
import dbHelper

conn = sqlite3.connect('scan_results.db')
c = conn.cursor()

data = dbHelper.getData(c)
for item in data:
    print(item)
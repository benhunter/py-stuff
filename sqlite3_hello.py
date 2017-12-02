# Testing sqlite3 module

import sqlite3, csv

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS routes ('
               'airline, '
               'airline_id, '
               'source_airport, '
               'source_airport_id, '
               'destination_airport, '
               'destination_airport_id, '
               'codeshare, '
               'stops, '
               'equipment)')

path = 'c:/data/datasets/OpenFlights.org/routes.dat'
file = open(path, 'r')
iter = csv.reader(file)

for row in iter:
#     print(row)
    cursor.execute('INSERT INTO routes VALUES (?,?,?,?,?,?,?,?,?)', row)

# cursor.executemany('INSERT INTO routes VALUES (:values)', {"values": iter})

all = cursor.execute('SELECT DISTINCT airline FROM routes')
# print(all)
print(len(all.fetchall()))

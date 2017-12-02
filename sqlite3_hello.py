# Testing sqlite3 module

import sqlite3, csv

# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('openflight.db')
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

pathRoute = 'c:/data/datasets/OpenFlights.org/routes.dat'
file = open(pathRoute, 'r')
csvReader = csv.reader(file)

for row in csvReader:
    cursor.execute('INSERT INTO routes VALUES (?,?,?,?,?,?,?,?,?)', row)
conn.commit()
print("Done with routes...")

# Load Airports.dat into database
cursor.execute('CREATE TABLE IF NOT EXISTS airports ('
               'airport_id, '
               'name, '
               'city, '
               'country, '
               'iata, '
               'icao, '
               'latitude, '
               'longitude, '
               'altitude, '
               'timezone, '
               'dst, '
               'tz_database, '
               'type, '
               'source)')

pathAirports = 'c:/data/datasets/OpenFlights.org/airports.dat'
file = open(pathAirports, 'r', encoding='utf-8')
csvReader = csv.reader(file)

for row in csvReader:
    cursor.execute('INSERT INTO airports VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
    # print(row)
conn.commit()
print("Done with airports...")



all = cursor.execute('SELECT DISTINCT country FROM airports')
# print(all)
print(len(all.fetchall()))

conn.commit()
conn.close()

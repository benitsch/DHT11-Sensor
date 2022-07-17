import time, os, time, adafruit_dht
import sqlite3
from sqlite3 import Error
from datetime import datetime, time as t

def create_db_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def insert_values(conn, values):
	sql = "INSERT INTO value(celsius,humidity) VALUES(?,?)"
	cur = conn.cursor()
	cur.execute(sql, values)
	conn.commit()

def insert_error(conn, value):
	sql = "INSERT INTO error(reason) VALUES(?)"
	cur = conn.cursor()
	cur.execute(sql, value)
	conn.commit()

def main():
	database = r"/home/admin/Projects/weather-station/weather.db"

	conn = create_db_connection(database)
	if conn != None:
		dht_device = adafruit_dht.DHT22(4)
		nowTime = datetime.now().time()

		while True:
			try:
				temperature = dht_device.temperature
				humidity = dht_device.humidity
				# Quick fix to solve unsigned int values from adafruit for negative temperatures
				if temperature == -0.0:
					temperature = -0.1
				elif temperature < 0:
					temperature = round(-temperature - 3276.9, 1)

				if temperature > 60 or temperature < -30 or humidity > 100 or humidity < 0:
					insert_error("Wrong values with temperature: {} and humidity: {}".format(temperature, humidity))
					continue

				values = (temperature, humidity)
				insert_values(conn, values)
				
				# At night, it is not necessary to check the temperature & humidity each 30 sec.
				if nowTime >= t(23,30) or nowTime <= t(5,00):
					time.sleep(60)
				else:
					time.sleep(30)
			except RuntimeError as e:
				insert_error(str(e))

if __name__ == '__main__':
	main()

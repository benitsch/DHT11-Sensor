import time, adafruit_dht, os, time
from datetime import datetime, time as t

dht_device = adafruit_dht.DHT22(4)

while True:
	now = datetime.now()
	nowTime = now.time()
	dayStr = now.strftime("%Y_%m_%d")
	filename = '/var/www/html/tempdata/' + dayStr + '.txt'

	try:
		temperature = dht_device.temperature
		humidity = dht_device.humidity

        # Quick fix to solve unsigned int values for negative temperatures from adafruit
		if temperature == -0.0:
			temperature = -0.1
		elif temperature < 0:
			temperature = round(-temperature - 3276.9, 1)
		values = "{}: Temperature = {} Humidity = {}".format(now.strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity)

		if os.path.exists(filename):
			append_write = 'a'
		else:
			append_write = 'w'

		file = open(filename, append_write)
		file.write(values + '\n')
		file.close()

	except RuntimeError as e:
		error = "{}: ERROR: {}".format(now.strftime("%Y-%m-%d %H:%M:%S"), e)
		errorFileName = '/var/www/html/tempErr.txt'
		if os.path.exists(errorFileName):
			app_w = 'a'
		else:
			app_w = 'w'

		file = open(errorFileName, app_w)
		file.write(error + '\n')
		file.close()

	if nowTime >= t(23,30) or nowTime <= t(5,00):
		time.sleep(60)
	else:
		time.sleep(15)

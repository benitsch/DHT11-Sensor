# DHT11-Sensor
Read values (temperature and humidity) from DHT11-Sensor on a raspberry pi and write into a SQLite database.

## Development
- Ensure you have the latest LTS version of Python installed
- Install dependencies
	- Run `sudo apt install python3-pip`
	- Run `pip3 install adafruit-circuitpython-dht`
	- Run `sudo apt-get install libgpiod2`
 	- Run `sudo apt install sqlite3`

 ## Database creation
 - Run `sqlite3 weather.db`
 - Create db tables with the following command:

```sql
CREATE TABLE value(id INTEGER PRIMARY KEY AUTOINCREMENT, celsius REAL, humidity REAL, created_at DATETIME DEFAULT (datetime('now','localtime')));
CREATE TABLE error(id INTEGER PRIMARY KEY AUTOINCREMENT, reason TEXT, created_at DATETIME DEFAULT (datetime('now','localtime')));
```

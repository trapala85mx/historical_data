# Summary
This is a script for retrieving crypto historical data from Futures BinanceAPI
It uses the python-binance library from sammchardy among other libraries

# About this version
This is still a preeliminar version but it is functional

# Requirements
- Python 3.11
- PostgreSql 15. If you want to use another DataBase you need
  to modify database/connection_db.py
- clone repository
- move to historical_data foler
```Shell
cd historical_data
```
- Install requirements
```Shell
pip install -r requirements.txt
```
- execute
```shell
python main.py -a <symbol> -t <timeframe>
```
if something goes wrong mayb eyou need to execute from parent folder, so you need to
```shell
cd ..
python historical_data/main.py -a <symbol> -t <timeframe>
```
The timeframes availables are:
1m, 3m, 5m, 15m, 1h, 4h, 1d
If you want to add more timeframes ypu should add it int extraction/extrac_data.py line 8 according to the
BinanceAPI Documentation in the General Info Section - Public Endpoints info - Kline/Candlestick chart intervals

# Configuration
For this script to work, you need to create the .env file that will be used by python-decouple library.

Inside historical_data folder execute:
```shell
touch .env
```
Inside this file you need theese variables:
```shell
DB_NAME = "your database name"
DB_USER = "your user"
DB_PASSWORD = "your password"
DB_HOST = "your host"
DB_PORT = your port for Postgres Database, default 5432
```
# Example

Getting btc historical data for 15 minutes timeframe
```Shell
python historical_data/main.py -a btcusdt -t 15m
```
# Summary
This is a script for retrieving crypto historical data from Futures BinanceAPI
It uses the python-binance library from sammchardy among other libraries

# About this version
This is still a preeliminar version but it is functional
To select the crypto to retrieve data ypu shoul write the ticker symbol in lowercase with the "usdt"
int he line 21 and the timeframe on main.py

In coming versions will automatically donwload and update all ticker symbols in Binance Futures

# Requirements
It is made on Python 3.11
For running use terminal 
1. Create you virtual environment and activate it
2. Locate in historical_data folder and execute 
```Shell
pip install -r requirements.txt
```
3. Change the ticker symbol in line 21 in main.py and the timeframe
4. run main file
```shell
python main.py
```
This script uses implements postgres connection

# Configuration
For this script to work, you need to create the .env file that will be used by python-decouple library
inside historical_data folder execute:
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

# Nest Updates
For the next updates will be automatically download and update the data just by running main.py
And the las update will be for store the script in a server to automatically search for updated and new cryptos every day
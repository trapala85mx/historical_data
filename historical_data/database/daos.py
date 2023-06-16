from typing import List
import pandas as pd
from models.candle import Candle
from database.connection_db import DatabaseConnection
import psycopg2
from decouple import config
class TableDAO:
    
    def __init__(self, asset :str, interval:str):
        self._asset = asset.lower()
        self._interval = interval
        self._table_name = f"{self._asset}_{self._interval}"
        self._connection = DatabaseConnection().get_database_connection()
    
    
    def exists(self) -> bool:
        query = f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='{self._table_name}' and table_schema='public');"
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when fetching tables for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in {self._asset.upper()}")
            print(e)
    
    
    def drop_table(self) -> bool:
        query = f"""DROP TABLE IF EXISTS {self._table_name};"""
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            self._connection.commit()
            return True 
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when deleting table for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in drop_able for {self._asset.upper()}")
            print(e)

    
    def create_table(self) -> bool:
        query = f"""CREATE TABLE IF NOT EXISTS {self._table_name} (
                open_time TIMESTAMP PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume FLOAT,
                tstamp BIGINT 
            );"""
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            self._connection.commit()
            return True
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when creating table for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in create_table for {self._asset.upper()}")
            print(e)
    
    
    def insert_data(self, values:List[tuple]) -> bool:
        query = f"INSERT INTO {self._table_name} (tstamp, open, high, low, close, volume, open_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor = self._connection.cursor()
            cursor.executemany(query, values)
            self._connection.commit()
            return True
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when inserting data for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in insert_data for {self._asset.upper()}")
            print(e)
    
    
    def get_last_data(self) -> Candle | None:
        query = f"SELECT * FROM {self._table_name}_{self._interval} ORDER BY open_time DESC LIMIT 1;"
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"SELECT * FROM {self._table_name} ORDER BY tstamp DESC LIMIT 1;")
            last_data = cursor.fetchone()
            
            if last_data:
                candle = Candle(
                    open_time=last_data[0],
                    op=last_data[1],
                    high=last_data[2],
                    low=last_data[3],
                    clse=last_data[4],
                    volume=last_data[5],
                    tstamp=last_data[6]
                )
                return candle
            else:
                return None
        
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when fetching last data for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in get_last_data for {self._asset.upper()}")
            print(e)


class DataBaseDAO:
    
    def __init__(self, asset:str, interval:str):
        self._asset = asset.lower()
        self._interval = interval
        self._database_name = config('DB_NAME')
        self._connection = DatabaseConnection().get_database_connection()
    
    
    def exists(self):
        query = f"SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname = '{self._database_name}';"
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result
        except psycopg2.OperationalError as e:
            print(f"Something went wrong when fetching database for {self._asset.upper()}")
            print(e)
        except psycopg2.Error as e:
            print(f"Error in exists for {self._asset.upper()}")
            print(e)
    
if __name__ == '__main__':
    pass
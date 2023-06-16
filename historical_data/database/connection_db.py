import psycopg2
from decouple import config
from decorators.singleton import singleton

@singleton
class DatabaseConnection(object):
    
    def __init__(self) -> None:
        db_name = config("DB_NAME")
        user = config("DB_USER")
        passw = config("DB_PASSWORD")
        host = config("DB_HOST")
        port = config("DB_PORT")
        
        try:
            self.__connection = psycopg2.connect(f"postgres://{user}:{passw}@{host}:{port}/{db_name}")
        except psycopg2.Error as e:
            print("Could not stablish connection to database")
            print(e)
        
    def get_database_connection(self):
        return self.__connection
    
    
    def close_connection(self):
        self.__connection.close()

if __name__ == '__main__':
    pass
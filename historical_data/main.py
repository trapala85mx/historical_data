from datetime import datetime
from database.daos import TableDAO
from database.daos import DataBaseDAO
from database.connection_db import DatabaseConnection
from processing.clean import data_for_database
from extraction.extrac_data import get_exchange_info
from extraction.extrac_data import get_historical_data
from extraction.extrac_data import update_historical_data
from extraction.extrac_data import get_last_data_updateable


def difference_between_times(last_posible_update , last_data):
    last_posible_update_dt = datetime.fromtimestamp(last_posible_update / 1000)
    last_data_dt = datetime.fromtimestamp(last_data / 1000)
    diferencia_minutos = (last_posible_update_dt - last_data_dt).total_seconds() / 60
    return diferencia_minutos

def run():
    try:
        # Daos de moneda
        symbol = "cfxusdt"
        timeframe = "15m"
        exchange_info = get_exchange_info()
        # TO DO: 
        #       Crear una nueva funcionalidad y base de datos para obtener y actualizar
        #       la fecha de on_board, la precisión del precio y la precisión de la cantidad
        #       Y otros datos de la moneda que nos pueda hacer de utilidad
        database_dao = DataBaseDAO(asset=symbol, interval=timeframe)
        
        
        if not database_dao.exists():
            raise Exception("No database")
    
    except Exception as e:
        print(e)
    
    else:
        table_dao = TableDAO(asset=symbol, interval=timeframe)
        
        if not table_dao.exists():
            table_dao.create_table()
        
        last_data = table_dao.get_last_data()
        
        print("Extrayendo datos")
        if last_data is None: # Si la tabla no tiene datos 
            # Extraemos desde inicios
            print("Extrayendo desde inicio de tiempos")
            data = get_historical_data(asset=symbol, timeframe=timeframe, exchange_info=exchange_info)
            
            data = data_for_database(data)
            data.pop()
            table_dao.insert_data(data)
            print("Data Guardada Satisfactoriamente")
        
        else: # Si la tabla tiene datos
            print("Actualizando data")
            last_posible_update = get_last_data_updateable(15)
            timedelta = difference_between_times(last_posible_update, last_data.tstamp)
            
            if timedelta >= (2*15):
                data = update_historical_data(asset=symbol, timeframe=timeframe, start=last_data.tstamp, end=last_posible_update)
                data.pop(0)
                data.pop()
                data = data_for_database(data)
                table_dao.insert_data(data)
        print("Data Extradia y Guardad")
    finally:
        database_connection.close_connection()
    
if __name__ == '__main__':
    database_connection = DatabaseConnection()
    run()
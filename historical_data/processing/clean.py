# Procesamineto de datos que incluye;
# Depurar los datos y solo quedarnos con lo que necesitamos
# Obtener la lista de tuplas para ingresarla a la BD
import pandas as pd
from typing import List


def pass_to_dataframe(data:List[list]) -> pd.DataFrame:
    try:
        df = pd.DataFrame(data)
        df = df.iloc[:,:6]
        df.columns = ["tstamp", "open", "high", "low", "close", "volume"]
        df["tstamp"] = df.tstamp.astype("int64")
        df.open = df.open.astype("float64")
        df.high = df.high.astype("float64")
        df.low = df.low.astype("float64")
        df.close = df.close.astype("float64")
        df.volume = df.volume.astype("float64")
        df["open_time"] = pd.to_datetime(df["tstamp"], unit="ms")
        return df
    except Exception as e:
        print("Algo pasó al pasasr a DataFrame")
        print(e)


def data_for_database(data:List[list]) -> List[tuple]:
    df = pass_to_dataframe(data)
    values = [tuple(row) for row in df.values]
    return values
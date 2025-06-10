import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_yes_no_column_into_zero_one
from src.data.constants import DB_CONFIG


def transform_dataframe(df):
     rename_map = {
        "Zip Code": "ZipCode",
        "Hospital Name": "HospitalName",
        "Ambulance Available": "AmbulanceAvailable"
    }
     df.rename(columns=rename_map, inplace=True)
     df = df[list(rename_map.values())]
     df = clean_yes_no_column_into_zero_one(df,"AmbulanceAvailable","AmbulanceAvailable")
     
     return df
         
def insert_data(df):
    # Replace NaNs with None for MySQL compatibility
    # Convert string 'nan', 'NaN', etc. to actual None
    df = df.replace(to_replace=['nan', 'NaN', 'NAN', 'None', 'NONE'], value=None)

    # Ensure Pandas NaNs (np.nan) are also converted to None
    df = df.where(pd.notnull(df), None)


    try:
          conn = mysql.connector.connect(**DB_CONFIG)
          cursor = conn.cursor()
          cursor.execute("DELETE FROM hospitals_emergency_data") 
          insert_sql = """
        INSERT INTO hospitals_emergency_data (
            zipCode, HospitalName, AmbulanceAvailable
        ) VALUES (%s, %s, %s)
        """
          for idx, row in df.iterrows():
            #row = row.where(pd.notnull(row), None)
            try:
                cursor.execute(insert_sql, tuple(row))
            except Error as e:
                print(f"Failed to insert row {idx} with id={row.get('id')}: {e}")

          conn.commit()
          print("Data inserted successfully.")

    except Error as e:
          print(f"Error: {e}")
    finally:
          if conn.is_connected():
               cursor.close()
               conn.close()
         

if __name__ == "__main__":
     print("Running initialize_db.py...")
     file_path = 'data/hospitals_emergency_data.csv'
     df = pd.read_csv(file_path)
     #print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     insert_data(df_clean)
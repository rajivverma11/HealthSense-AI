import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_yes_no_column_into_zero_one
from src.data.constants import LOCAL_DB_CONFIG




def transform_dataframe(df):
     rename_map = {
        "doctor_id": "Doctor_id",
        "datetime": "Datetime",
        "is_available": "Is_available"
        
    }
     

    # Step 1: Convert 'Datetime' column to datetime object from 12-hour format
     df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %I:%M %p', errors='coerce')

    # Step 2: Convert to string in MySQL-compatible 24-hour format
     df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

     df.rename(columns=rename_map, inplace=True)
     df = df[list(rename_map.values())]
     
     return df
         
def insert_data(df):
    # Replace NaNs with None for MySQL compatibility
    # Convert string 'nan', 'NaN', etc. to actual None
    df = df.replace(to_replace=['nan', 'NaN', 'NAN', 'None', 'NONE'], value=None)

    # Ensure Pandas NaNs (np.nan) are also converted to None
    df = df.where(pd.notnull(df), None)


    try:
          conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
          cursor = conn.cursor()
          cursor.execute("DELETE FROM doctors_slots_data") 
          insert_sql = """
        INSERT INTO doctors_slots_data (
            Doctor_id, Datetime, Is_available
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
     file_path = 'data/doctors_slots_data.csv'
     df = pd.read_csv(file_path)
     #print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     insert_data(df_clean)
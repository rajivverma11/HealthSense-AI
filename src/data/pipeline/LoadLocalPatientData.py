import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_yes_no_column_into_zero_one


from dotenv import load_dotenv
import os

load_dotenv()

LOCAL_DB_CONFIG = {
    'host': os.getenv('LOCAL_DB_HOST'),
    'user': os.getenv('LOCAL_DB_USER'),
    'password': os.getenv('LOCAL_DB_PASSWORD'),
    'database': os.getenv('LOCAL_DB_NAME'),
    'port': int(os.getenv('LOCAL_DB_PORT'))  # Convert from string to int
}


def transform_dataframe(df):
     rename_map = {
        "Name": "Name",
        "Gender": "Gender",
        "Dateofbirth": "DateOfBirth",
        "Ethnicity": "Ethnicity",
        "FirstDisease": "FirstDisease",
        "SecondDisease": "SecondDisease",
        "Address": "Address",
        "State": "State",
        "ZipCode": "ZipCode"
    }

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
          cursor.execute("DELETE FROM patient_info") 
          insert_sql = """
        INSERT INTO patient_info (
            Name, Gender, DateOfBirth, Ethnicity, FirstDisease, SecondDisease, Address, State, ZipCode
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
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
     file_path = 'data/Synthetic_Patient_Data.csv'
     df = pd.read_csv(file_path)
     print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     insert_data(df_clean)
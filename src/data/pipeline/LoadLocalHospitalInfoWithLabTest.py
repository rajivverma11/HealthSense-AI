import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_emergency_services_column
from src.data.constants import LOCAL_DB_CONFIG



def transform_dataframe(df):
     rename_map = {
        "Provider ID": "ProviderID",
        "Preparation Instructions": "PreparationInstructions",
        "Diagnostic Test": "DiagnosticTest",
        "Health Package": "HealthPackage"
       
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
          cursor.execute("DELETE FROM hospital_information_with_Lab_tests") 
          insert_sql = """
        INSERT INTO hospital_information_with_Lab_tests (
            ProviderID, PreparationInstructions, DiagnosticTest, HealthPackage
        ) VALUES (%s, %s, %s, %s)
        """
          for idx, row in df.iterrows():
            #row = row.where(pd.notnull(row), None)
            try:
                cursor.execute(insert_sql, tuple(row))
            except Error as e:
                print(f"Failed to insert row {idx} with ProviderID={row.get('ProviderID')}: {e}")

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
     file_path = 'data/Hospital_Information_with_Lab_Tests.csv'
     df = pd.read_csv(file_path)
     #print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     insert_data(df_clean)
     
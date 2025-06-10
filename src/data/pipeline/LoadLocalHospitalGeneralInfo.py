import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_emergency_services_column
from src.data.constants import LOCAL_DB_CONFIG


def transform_dataframe(df):
     rename_map = {
        "Provider ID": "ProviderID",
        "Hospital Name": "HospitalName",
        "Address": "Address",
        "City": "City",
        "State": "State",
        "ZIP Code": "ZipCode",
        "County Name": "CountyName",
        "Phone Number": "PhoneNumber",
        "Hospital Type": "HospitalType",
        "Hospital Ownership": "HospitalOwnership",
        "Emergency Services": "EmergencyServices",
        "Hospital overall rating": "HospitalRating",
        "Mortality national comparison": "MortalityNationalComparison",
        "Safety of care national comparison": "SafetyCareNationalComparison",
        "Readmission national comparison": "ReadmissionNationalComparison",
        "Patient experience national comparison": "PatientExperienceNationalComparison",
        "Effectiveness of care national comparison": "NationalComparisonEffectiveness",
        "Timeliness of care national comparison": "CareTimelinesNationalComparison",
        "Efficient use of medical imaging national comparison": "EfficientMedicalImagingNationalComparison"
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
          cursor.execute("DELETE FROM hospital_general_information") 
          insert_sql = """
        INSERT INTO hospital_general_information (
            ProviderID, HospitalName, Address, City, State, ZipCode, CountyName,
            PhoneNumber, HospitalType, HospitalOwnership, EmergencyServices,
            HospitalRating, MortalityNationalComparison, SafetyCareNationalComparison,
            ReadmissionNationalComparison, PatientExperienceNationalComparison,
            NationalComparisonEffectiveness, CareTimelinesNationalComparison,
            EfficientMedicalImagingNationalComparison
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
          for idx, row in df.iterrows():
            row = row.where(pd.notnull(row), None)
            #print(row)
            #print(tuple(row))
            try:
                cursor.execute(insert_sql, tuple(row))
            except Error as e:
                print(f"❌ Failed to insert row {idx} with ProviderID={row.get('ProviderID')}: {e}")

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
     file_path = 'data/Hospital_General_Information.csv'
     df = pd.read_csv(file_path)
     #df = df.head(3)
     #print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     #print("Columns in df_clean:",df_clean.columns.tolist())
     insert_data(df_clean)

     
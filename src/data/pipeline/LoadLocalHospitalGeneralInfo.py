import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from src.utils.cleaners import clean_emergency_services_column

LOCAL_DB_CONFIG = {
'host': 'localhost',
'user':'root',
'password':'Rajiv8777',
'database': 'HealthSenseAI',
'port': 3306
}

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
     df = clean_emergency_services_column(df)
        


     comparison_columns = [
        "MortalityNationalComparison",
        "SafetyCareNationalComparison",
        "ReadmissionNationalComparison",
        "PatientExperienceNationalComparison",
        "NationalComparisonEffectiveness",
        "CareTimelinesNationalComparison",
        "EfficientMedicalImagingNationalComparison"
    ]
     
     def map_comparison(val):
          val1 = str(val).strip().lower()
          if 'above' in val1:
               return 3
          elif 'same' in val1:
               return 2
          elif 'below' in val1:
               return 1
          else:
               return 0
     
     for col in comparison_columns:
          df.loc[:, col]  = df[col].apply(map_comparison)
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
     #print("Columns in CSV:", df.columns.tolist())

     df_clean = transform_dataframe(df)
     insert_data(df_clean)

     
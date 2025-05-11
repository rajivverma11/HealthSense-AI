import mysql.connector
from mysql.connector import Error

from src.data.constants import LOCAL_DB_CONFIG


def create_tables():
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
 
            # Create tables
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospital_general_information (
                ProviderID VARCHAR(20) PRIMARY KEY,
                HospitalName VARCHAR(255),
                Address VARCHAR(1000),
                City VARCHAR(100),
                State VARCHAR(100),
                ZipCode VARCHAR(20),
                CountyName VARCHAR(100),
                PhoneNumber VARCHAR(20),
                HospitalType VARCHAR(100),
                HospitalOwnership VARCHAR(100),
                EmergencyServices TINYINT(1) DEFAULT 1 ,
                HospitalRating FLOAT,
                MortalityNationalComparison VARCHAR(100),
                SafetyCareNationalComparison VARCHAR(100),
                ReadmissionNationalComparison VARCHAR(100),
                PatientExperienceNationalComparison VARCHAR(100),
                NationalComparisonEffectiveness VARCHAR(100),
                CareTimelinesNationalComparison VARCHAR(100),
                EfficientMedicalImagingNationalComparison VARCHAR(100)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospital_information_with_Lab_tests (
                ProviderID VARCHAR(20) PRIMARY KEY,
                PreparationInstructions VARCHAR(500),
                DiagnosticTest VARCHAR(500),
                HealthPackage VARCHAR(500)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors_info_data (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(200),
                Specialization VARCHAR(200),
                Contact VARCHAR(100)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors_slots_data (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Doctor_id VARCHAR(200),
                Datetime DATETIME NOT NULL,
                Is_available TINYINT(1) DEFAULT 1 
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals_emergency_data (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                ZipCode VARCHAR(20),
                HospitalName VARCHAR(200),
                AmbulanceAvailable TINYINT(1) DEFAULT 1 
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_info (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100),
                Dateofbirth DATETIME,
                Gender VARCHAR(10),
                Address VARCHAR(200),
                State VARCHAR(100),
                Zipcode VARCHAR(20),
                Ethnicity VARCHAR(100),
                Firstdisease VARCHAR(100),
                Seconddisease VARCHAR(100)
               
            );
              
            """)

            

            conn.commit()
            print("Tables created successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

print("Running initialize_db.py...")

if __name__ == "__main__":
    create_tables()

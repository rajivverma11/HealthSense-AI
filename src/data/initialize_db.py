import mysql.connector
from mysql.connector import Error

from src.data.constants import DB_CONFIG


def create_tables():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
 
            # Create tables
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparison_lookup (
                comparison_id TINYINT PRIMARY KEY,
                label VARCHAR(50)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospital_general_information (
                ProviderID VARCHAR(20) PRIMARY KEY,
                HospitalName VARCHAR(255),
                Address VARCHAR(1000),
                City VARCHAR(100),
                state VARCHAR(100),
                ZipCode VARCHAR(20),
                CountyName VARCHAR(100),
                PhoneNumber VARCHAR(20),
                HospitalType VARCHAR(100),
                HospitalOwnership VARCHAR(100),
                EmergencyServices TINYINT(1) DEFAULT 1 ,
                HospitalRating FLOAT,
                MortalityNationalComparison TINYINT,
                SafetyCareNationalComparison TINYINT,
                ReadmissionNationalComparison TINYINT,
                PatientExperienceNationalComparison TINYINT,
                NationalComparisonEffectiveness TINYINT,
                CareTimelinesNationalComparison TINYINT,
                EfficientMedicalImagingNationalComparison TINYINT
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
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200),
                specialization VARCHAR(200),
                contact VARCHAR(100)
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors_slots_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_id VARCHAR(200),
                datetime DATETIME NOT NULL,
                is_available TINYINT(1) DEFAULT 1 
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals_emergency_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                zipCode VARCHAR(20),
                hospitalName VARCHAR(200),
                ambulanceAvailable TINYINT(1) DEFAULT 1 
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

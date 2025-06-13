import mysql.connector
import pandas as pd
import os
from src.data.constants import LOCAL_DB_CONFIG,DB_CONFIG


def get_cloud_connection():
    return mysql.connector.connect(
        host= DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port']

    )

def get_local_connection():
    return mysql.connector.connect(
        host= LOCAL_DB_CONFIG['host'],
        user=LOCAL_DB_CONFIG['user'],
        password=LOCAL_DB_CONFIG['password'],
        database=LOCAL_DB_CONFIG['database'],
        port=LOCAL_DB_CONFIG['port']

    )


def load_hospital_dataframe() -> pd.DataFrame:
    connection = get_cloud_connection()

    query = "SELECT * FROM hospital_general_information"
    df = pd.read_sql(query, con=connection)
    connection.close()
    return df

def load_hospital_info_test_dataframe() -> pd.DataFrame:
    connection = get_cloud_connection()

    # Write the SQL query with an INNER JOIN on provider_id
    query = """
    SELECT 
        hgi.*, 
        hl.PreparationInstructions, 
        hl.DiagnosticTest,
        hl.HealthPackage
    FROM hospital_general_information AS hgi
    INNER JOIN hospital_information_with_Lab_tests AS hl
        ON hgi.ProviderID = hl.ProviderID
    """

    # Load the result into a pandas DataFrame
    df = pd.read_sql_query(query, connection)

    # Close the connection
    connection.close()
    return df


def get_mysql_uri() -> str:
    """Builds SQLAlchemy-style MySQL URI from .env"""
    # user = LOCAL_DB_CONFIG['user']
    # password = LOCAL_DB_CONFIG['password']
    # host = LOCAL_DB_CONFIG['host']
    # port = LOCAL_DB_CONFIG['port']
    # db = LOCAL_DB_CONFIG['database']

    user = DB_CONFIG['user']
    password = DB_CONFIG['password']
    host = DB_CONFIG['host']
    port = DB_CONFIG['port']
    db = DB_CONFIG['database']

    if not all([user, password, host, port, db]):
        raise ValueError("❌ Missing one or more MySQL DB environment variables.")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"


def get_patient_profile(name: str):
    #
    connection = get_cloud_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT Name, Dateofbirth, Gender, Address, State, Zipcode, Ethnicity, Firstdisease,Seconddisease
        FROM patient_info
        WHERE Name LIKE %s 
        LIMIT 1
    """

    
    cursor.execute(query, (f"%{name}%",))  # Adds wildcards

    row = cursor.fetchone()

    cursor.close()
    connection.close()
   
  
    if row:
        print("✅ One matching record found")
    else:
        print("❌ No matching record")

    return row
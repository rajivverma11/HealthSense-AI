import mysql.connector
import pandas as pd
import os
from src.data.constants import LOCAL_DB_CONFIG


def load_hospital_dataframe() -> pd.DataFrame:
    connection = mysql.connector.connect(
        host= LOCAL_DB_CONFIG['host'],
        user=LOCAL_DB_CONFIG['user'],
        password=LOCAL_DB_CONFIG['password'],
        database=LOCAL_DB_CONFIG['database'],
        port=LOCAL_DB_CONFIG['port']
    )

    query = "SELECT * FROM hospital_general_information"
    df = pd.read_sql(query, con=connection)
    connection.close()
    return df

def get_mysql_uri() -> str:
    """Builds SQLAlchemy-style MySQL URI from .env"""
    user = LOCAL_DB_CONFIG['user']
    password = LOCAL_DB_CONFIG['password']
    host = LOCAL_DB_CONFIG['host']
    port = LOCAL_DB_CONFIG['port']
    db = LOCAL_DB_CONFIG['database']

    if not all([user, password, host, port, db]):
        raise ValueError("❌ Missing one or more MySQL DB environment variables.")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

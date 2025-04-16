import pytest
import mysql.connector
import pandas as pd

@pytest.fixture(scope = "session")
def db_connect():

    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        database = 'practice',
        password = 'password'
    )

    cursor = conn.cursor()
    yield cursor

    cursor.close()
    conn.close()

@pytest.fixture(scope="session")
def source():
    df_source = pd.read_csv("source_data.csv")
    return df_source

@pytest.fixture(scope="session")
def target():
    df_target =  pd.read_csv("target_data.csv")
    return df_target



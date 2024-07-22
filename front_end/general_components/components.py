import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

class GeneralComponents:
    def __init__(self):
        self.mysql_username=st.secrets["mysql_db_credentials"]["MYSQL_USERNAME"]
        self.mysql_password=st.secrets["mysql_db_credentials"]["MYSQL_PASSWORD"]
        self.mysql_host=st.secrets["mysql_db_credentials"]["MYSQL_HOST"]
        self.mysql_port=st.secrets["mysql_db_credentials"]["MYSQL_PORT"]
        self.mysql_database_name=st.secrets["mysql_db_credentials"]["MYSQL_DB_NAME"]


    def create_mysql_engine(self):
        engine=create_engine(f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}@" \
                             f"{self.mysql_host}:{self.mysql_port}/" \
                                f"{self.mysql_database_name}")
        connected_engine=engine.connect()

        return connected_engine


    def execute_sql_to_df(self, sql_query, date_column=None):
        mysql_engine=self.create_mysql_engine()

        if date_column is None:
            df=pd.read_sql(sql_query, 
                           con=mysql_engine)
            
        elif date_column is not None:
            df=pd.read_sql(sql_query, 
                           con=mysql_engine,
                           parse_dates={f"{date_column}": "%Y-%m-%d"})

        return df

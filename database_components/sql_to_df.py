import pandas as pd

from database_components.db_engines import DatabaseMYSQLEngine

class SQLToDataframe:
    def __init__(self, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):
        self.mysql_username=mysql_username
        self.mysql_password=mysql_password
        self.mysql_host=mysql_host
        self.mysql_port=mysql_port
        self.mysql_db_name=mysql_db_name

        database_mysql_engine=DatabaseMYSQLEngine()
        self.mysql_eninge=database_mysql_engine.create_mysql_engine(mysql_username=self.mysql_username, 
                                                                    mysql_password=self.mysql_password, 
                                                                    mysql_host=self.mysql_host, 
                                                                    mysql_port=self.mysql_port, 
                                                                    mysql_db_name=self.mysql_db_name)


    def execute_sql_to_df(self, sql_query, date_column=None):
        if date_column is None:
            df=pd.read_sql(sql_query, 
                        con=self.mysql_eninge)
            
        elif date_column is not None:
            df=pd.read_sql(sql_query, 
                           con=self.mysql_eninge,
                           parse_dates={f"{date_column}": "%Y-%m-%d"})

        return df

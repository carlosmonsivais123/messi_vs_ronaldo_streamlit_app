import streamlit as st

from general_components.components import GeneralComponents


class SQLQueries:
    def __init__(self):
        self.mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"]

        self.general_components=GeneralComponents()


    def player_teams_query(self):
        player_teams_query_text=f'''SELECT DISTINCT player_name, 
                                           squad
                                    FROM {self.mysql_table_name}'''
        
        player_teams_df=self.general_components.execute_sql_to_df(sql_query=player_teams_query_text)
        
        return player_teams_df
    

    def general_competition_query(self):
        general_competition_query_text=f'''SELECT DISTINCT competition_type
                                          FROM {self.mysql_table_name}'''
        
        general_competition_df=self.general_components.execute_sql_to_df(sql_query=general_competition_query_text)
        
        return general_competition_df


    def list_filter_val(self, list_filter_value):
        filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in list_filter_value))

        return filter_text_string


    def filtered_sql_query_builder(self, messi_teams_filter, ronaldo_teams_filter, general_competition_filter, start_date, end_date):
        # Messi Filter
        if len(messi_teams_filter) > 0:
            messi_squad_formatted_string=self.list_filter_val(list_filter_value=messi_teams_filter)
            messi_squad_filter_text=f'''WHERE ((player_name='Lionel Messi' AND squad IN {messi_squad_formatted_string}) OR '''
        else:
            messi_squad_filter_text=f'''WHERE ((player_name='Lionel Messi') OR '''

        # Ronaldo Filter
        if len(ronaldo_teams_filter) > 0:
            ronaldo_squad_formatted_string=self.list_filter_val(list_filter_value=ronaldo_teams_filter)
            ronaldo_squad_filter_text=f'''(player_name='Cristiano Ronaldo' AND squad IN {ronaldo_squad_formatted_string}))'''
        else:
            ronaldo_squad_filter_text=f'''(player_name='Cristiano Ronaldo'))'''

        # Competition Type Filter
        if len(general_competition_filter) > 0:
            competition_type_filter_formatted_string=self.list_filter_val(list_filter_value=general_competition_filter)
            competition_type_filter_string=f" AND competition_type IN {competition_type_filter_formatted_string}"
        else:
            competition_type_filter_string=''

        # Date Filter
        if (start_date is None) and (end_date is None):
            date_filter_string=''
        elif (start_date is not None) and (end_date is None):
            date_filter_string=f" AND DATE(date) >= '{start_date}'"
        elif (start_date is None) and (end_date is not None):
            date_filter_string=f" AND DATE(date) <= '{end_date}'"
        elif (start_date is not None) and (end_date is not None):
            date_filter_string=f" AND (DATE(date) BETWEEN '{start_date}' AND '{end_date}')"

        combined_filter_string=messi_squad_filter_text+ronaldo_squad_filter_text+competition_type_filter_string+date_filter_string
        filtered_df_query_builder=f'''SELECT DATE(date) AS date,
                                             squad,
                                             COALESCE(goals, 0) AS goals,
                                             COALESCE(assists, 0) AS assists,
                                             competition_type,
                                             total_contributions,
                                             game_played,
                                             minutes,
                                             result,
                                             player_name
                                      FROM {self.mysql_table_name}
                                      {combined_filter_string}'''
        
        filtered_df=self.general_components.execute_sql_to_df(sql_query=filtered_df_query_builder,
                                                              date_column="date")
        
        return filtered_df

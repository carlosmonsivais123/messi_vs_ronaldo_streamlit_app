import streamlit as st

class SQLQueries:
    def __init__(self):
        self.mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"]


    def player_teams_query(self):
        player_teams_query_text=f'''SELECT DISTINCT player_name, 
                                           squad
                                    FROM {self.mysql_table_name}'''
        
        return player_teams_query_text


    def list_filter_val(self, list_filter_value):
        filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in list_filter_value))

        return filter_text_string


    def filtered_df(self, messi_teams_filter, ronaldo_teams_filter, general_competition_filter, start_date, end_date):
        query_options_dict={'Lionel Messi': {'squad': messi_teams_filter, 
                                             'competition_type': general_competition_filter, 
                                             'start_date': start_date,
                                             'end_date': end_date},

                            'Cristiano Ronaldo': {'squad': ronaldo_teams_filter, 
                                                  'competition_type': general_competition_filter, 
                                                  'start_date': start_date,
                                                  'end_date': end_date}}
        
        print(query_options_dict)

        player_query='''WHERE (player_name='Lionel Messi'
        AND squad IN {filter_text_string} 
        AND (DATE(date) BETWEEN '{start_date}' AND '{end_date}')) OR 

        (player_name='Cristiano Ronaldo' AND 
                squad IN {filter_text_string} AND 
                (DATE(date) BETWEEN '{start_date}' AND '{end_date}'))'''

        for player in ['Lionel Messi', 'Cristiano Ronaldo']:
    
            for list_filter in ['squad', 'competition_type']:
                if len(list_filter)>0:
                    filter_string=self.list_filter_val(list_filter_value=list_filter)
                    output_filter_string=f"AND {list_filter} IN {filter_string}"
                else:
                    output_filter_string=''




        #     if len(query_options_dict[player]) > 0:
        #         filter_text_string=self.list_filter_val(query_options_dict[player])
        #         player_filter_string=f"(player_name='{player}' AND squad IN {filter_text_string})"
        #     else:
        #         player_filter_string=f"(player_name='{player}')"

        # for general_filter in ['competition_type', 'start_date', 'end_date']:
        #     if general_filter is not None:
        #         general_filter_string=f"({general_filter}=)"
        #     else:
        #         pass


        # print(query_options_dict)



    def goals_scored_page_query(self, filter_1, filter_2):
        if (len(filter_1)==0) and (len(filter_2)==0):
            squad_filter_text=""

        elif (len(filter_1)>0) and (len(filter_2)>0):
            filter_text_options=filter_1+filter_2
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_text_options))
            squad_filter_text=f'''WHERE squad IN {filter_text_string}'''

        elif (len(filter_1)>0) and (len(filter_2)==0):
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_1))
            squad_filter_text=f'''WHERE (player_name='Lionel Messi' AND squad IN {filter_text_string}) OR 
                                        (player_name='Cristiano Ronaldo')'''

        elif (len(filter_1)==0) and (len(filter_2)>0):
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_2))
            squad_filter_text=f'''WHERE (player_name='Lionel Messi') OR 
                                        (player_name='Cristiano Ronaldo' AND squad IN {filter_text_string})'''

        goals_scored_page_query_text=f'''SELECT DATE(date) AS date,
                                                squad,
                                                COALESCE(goals, 0) AS goals,
                                                COALESCE(assists, 0) AS assists,
                                                competition_type,
                                                result,
                                                player_name
                                         FROM {self.mysql_table_name}
                                         {squad_filter_text}'''
        
        return goals_scored_page_query_text
    

    # def consistency_page_query(self):
    #     consistenct_page_query_text=f'''SELECT DATE(date) AS date,
    #                                            squad,
    #                                            (COALESCE(goals, 0) + COALESCE(assists, 0)) AS total_contributions,
    #                                            COALESCE(minutes, 0) AS minutes,
    #                                            competition,
    #                                            result,
    #                                            player_name
    #                                     FROM {self.table_name}'''
        
    #     return consistenct_page_query_text

    def filtered_df_query(self, filter_1, filter_2):
        if (len(filter_1)==0) and (len(filter_2)==0):
            squad_filter_text=""

        elif (len(filter_1)>0) and (len(filter_2)>0):
            filter_text_options=filter_1+filter_2
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_text_options))
            squad_filter_text=f'''WHERE squad IN {filter_text_string}'''

        elif (len(filter_1)>0) and (len(filter_2)==0):
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_1))
            squad_filter_text=f'''WHERE (player_name='Lionel Messi' AND squad IN {filter_text_string}) OR 
                                        (player_name='Cristiano Ronaldo')'''

        elif (len(filter_1)==0) and (len(filter_2)>0):
            filter_text_string='({})'.format(','.join(f"'{elem}'" for elem in filter_2))
            squad_filter_text=f'''WHERE (player_name='Lionel Messi') OR 
                                        (player_name='Cristiano Ronaldo' AND squad IN {filter_text_string})'''

        filtered_df_query_text=f'''SELECT DATE(date) AS date,
                                               squad,
                                               (COALESCE(goals, 0) + COALESCE(assists, 0)) AS total_contributions,
                                               COALESCE(minutes, 0) AS minutes,
                                               competition_type,
                                               result,
                                               player_name
                                        FROM {self.mysql_table_name}
                                        {squad_filter_text}'''
        
        return filtered_df_query_text



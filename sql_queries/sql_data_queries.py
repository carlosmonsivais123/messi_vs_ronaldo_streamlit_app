class SQLQueries:
    def __init__(self, table_name):
        self.table_name=table_name


    def player_teams_query(self):
        player_teams_query_text=f'''SELECT DISTINCT player_name, 
                                           squad
                                    FROM {self.table_name}'''
        
        return player_teams_query_text


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
                                                competition,
                                                result,
                                                player_name
                                         FROM {self.table_name}
                                         {squad_filter_text}'''
        
        return goals_scored_page_query_text
    

    def consistency_page_query(self):
        consistenct_page_query_text=f'''SELECT DATE(date) AS date,
                                               squad,
                                               (COALESCE(goals, 0) + COALESCE(assists, 0)) AS total_contributions,
                                               COALESCE(minutes, 0) AS minutes,
                                               competition,
                                               result,
                                               player_name
                                        FROM {self.table_name}'''
        
        return consistenct_page_query_text

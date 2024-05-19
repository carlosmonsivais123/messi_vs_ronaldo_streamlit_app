class SQLQueries:
    def __init__(self, table_name):
        self.table_name=table_name


    def goals_scored_page_query(self):
        goals_scored_page_query_text=f'''SELECT DATE(date) AS date,
                                                squad,
                                                COALESCE(goals, 0) AS goals,
                                                COALESCE(assists, 0) AS assists,
                                                competition,
                                                result,
                                                player_name
                                         FROM {self.table_name}
                                     '''
        
        return goals_scored_page_query_text
    
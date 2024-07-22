from general_components.components import GeneralComponents
from sql_queries.sql_data_queries import SQLQueries

class SidebarFilterValues:
    def __init__(self):
        self.sql_queries=SQLQueries()
        self.general_components=GeneralComponents()
        
        self.players=["Lionel Messi", "Cristiano Ronaldo"]


    def unique_teams_filter_options(self):
        player_teams_sql_query=self.sql_queries.player_teams_query()
        unique_player_teams=self.general_components.execute_sql_to_df(sql_query=player_teams_sql_query)

        unique_player_team_list={}
        for player in self.players:
            unique_teams_list=unique_player_teams[unique_player_teams["player_name"]==player]["squad"].unique().tolist()
            unique_player_team_list[player]=unique_teams_list

        return unique_player_team_list
    

    def competition_type_filter(self, df):
        competition_type_values=df["competition_type"].unique().tolist()
        competition_type_values=list(set(competition_type_values))

        return competition_type_values

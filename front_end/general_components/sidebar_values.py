from general_components.components import GeneralComponents
from general_components.sql_data_queries import SQLQueries


class SidebarFilterValues:
    def __init__(self):
        self.sql_queries=SQLQueries()
        self.general_components=GeneralComponents()
        self.players=["Lionel Messi", "Cristiano Ronaldo"]


    def unique_teams_filter_options(self):
        unique_player_teams_df=self.sql_queries.player_teams_query()

        unique_player_team_list={}
        for player in self.players:
            unique_teams_list=unique_player_teams_df[unique_player_teams_df["player_name"]==player]["squad"].unique().tolist()
            unique_player_team_list[player]=unique_teams_list

        return unique_player_team_list
    

    def general_competition_type_filter(self):
        general_competition_type_df=self.sql_queries.general_competition_query()
        general_competition_type_values=general_competition_type_df["competition_type"].unique().tolist()

        return general_competition_type_values

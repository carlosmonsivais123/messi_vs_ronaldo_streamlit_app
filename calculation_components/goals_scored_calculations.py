import pandas as pd

from database_components.sql_to_df import SQLToDataframe
from sql_queries.sql_data_queries import SQLQueries
from echart_graphs.echart_options import EChartGoalsScoredOptionCreation

class GoalsScoredAnalytics:
    def __init__(self, mysql_table_name, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):
        self.sql_queries=SQLQueries(table_name=mysql_table_name)
        self.sql_to_dataframe=SQLToDataframe(mysql_username=mysql_username, 
                                             mysql_password=mysql_password, 
                                             mysql_host=mysql_host, 
                                             mysql_port=mysql_port, 
                                             mysql_db_name=mysql_db_name)
        self.echart_goals_scored_option_creation=EChartGoalsScoredOptionCreation()

        goals_scored_sql_query=self.sql_queries.goals_scored_page_query()
        self.goals_scored_df=self.sql_to_dataframe.execute_sql_to_df(sql_query=goals_scored_sql_query,
                                                                     date_column="date")
        
        self.players=["Lionel Messi", "Cristiano Ronaldo"]


    def cummulative_goals_scored(self):
        cummulative_goals_df=self.goals_scored_df.groupby(["player_name", pd.Grouper(key="date", freq="D")])["goals"].sum().groupby(level=0).cumsum()
        cummulative_goals_df=cummulative_goals_df.reset_index(drop=False, inplace=False)
        cummulative_goals_df["date"]=cummulative_goals_df["date"].dt.strftime(date_format="%Y-%m-%d")

        cummulative_goal_dict=cummulative_goals_df.to_dict("records")

        cummulative_goals_graph_options=self.echart_goals_scored_option_creation.cummulative_goals_scored_line_graph(source_data=cummulative_goal_dict)

        return cummulative_goals_graph_options
    

    def goals_scored_per_year(self):
        goals_scored_per_year_df=self.goals_scored_df.groupby(["player_name", pd.Grouper(key="date", freq="YE")])["goals"].sum()
        goals_scored_per_year_df=goals_scored_per_year_df.reset_index(drop=False, inplace=False)
        goals_scored_per_year_df["date"]=goals_scored_per_year_df["date"].dt.strftime(date_format="%Y")

        goals_scored_per_year_dict=goals_scored_per_year_df.to_dict("records")

        goals_per_year_graph_options=self.echart_goals_scored_option_creation.goals_scored_per_year_bar_graph(source_data=goals_scored_per_year_dict)

        return goals_per_year_graph_options
    

    def goals_scored_and_match_outcome(self):
        goals_scored_and_match_outcome_df=self.goals_scored_df.groupby(["player_name", pd.Grouper(key="date", freq="D"), "result"])["goals"].sum()
        goals_scored_and_match_outcome_df=goals_scored_and_match_outcome_df.reset_index(drop=False, inplace=False)
        goals_scored_and_match_outcome_df["date"]=goals_scored_and_match_outcome_df["date"].dt.strftime(date_format="%Y-%m-%d")

        goals_scored_and_match_outcome_df["data"]=goals_scored_and_match_outcome_df[["date", "result" , "goals"]].values.tolist()

        player_heatmap_options_dict={}
        for player in self.players:
            goals_scored_and_match_outcome_player_df=goals_scored_and_match_outcome_df[goals_scored_and_match_outcome_df["player_name"]==player].reset_index(drop=True, inplace=False)

            heatmap_x=goals_scored_and_match_outcome_player_df["date"].values.tolist()
            heatmap_y=goals_scored_and_match_outcome_player_df["result"].unique().tolist()
            heatmap_data=goals_scored_and_match_outcome_player_df["data"].values.tolist()
            heatmap_min_value=int(goals_scored_and_match_outcome_player_df["goals"].min())
            heatmap_max_value=int(goals_scored_and_match_outcome_player_df["goals"].max())

            goals_scored_and_match_outcome_options=self.echart_goals_scored_option_creation.goals_scored_and_match_outcome_heatmap(player=player,
                                                                                                                                   series_data=heatmap_data, 
                                                                                                                                   x_axis_data=heatmap_x, 
                                                                                                                                   y_axis_data=heatmap_y,
                                                                                                                                   min_value=heatmap_min_value, 
                                                                                                                                   max_value=heatmap_max_value)
            player_heatmap_options_dict[player]=goals_scored_and_match_outcome_options


        return player_heatmap_options_dict

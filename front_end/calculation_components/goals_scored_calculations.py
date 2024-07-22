import pandas as pd

from sql_queries.sql_data_queries import SQLQueries
from echart_graphs.echart_options import EChartGoalsScoredOptionsCreation
from general_components.components import GeneralComponents

class GoalsScoredAnalytics:
    def __init__(self):
        self.sql_queries=SQLQueries()
        self.general_components=GeneralComponents()
        self.echart_goals_scored_options_creation=EChartGoalsScoredOptionsCreation()
          
        self.players=["Lionel Messi", "Cristiano Ronaldo"]


    def filtered_df_test(self, messi_teams_filter, ronaldo_teams_filter, general_competition_filter, start_date, end_date):
        test_df=self.sql_queries.filtered_df(messi_teams_filter, 
                                             ronaldo_teams_filter, 
                                             general_competition_filter, 
                                             start_date, 
                                             end_date)


    def filtered_goals_scored_df(self, messi_team_options, ronaldo_team_options):
        goals_scored_sql_query=self.sql_queries.goals_scored_page_query(filter_1=messi_team_options, 
                                                                        filter_2=ronaldo_team_options)
        


        filtered_goals_scored_df=self.general_components.execute_sql_to_df(sql_query=goals_scored_sql_query,
                                                                           date_column="date")

        return filtered_goals_scored_df


    def goals_scored_metric_value(self, df):
        total_goals_df=df.groupby("player_name")["goals"].sum()
        total_goals_dict=total_goals_df.to_dict()

        return total_goals_dict
    

    def goals_ratio_metric_value(self, df):
        goals_per_game_ratio_df=df.groupby(["player_name"], as_index=True).agg(goal_per_game_ratio=("goals", "mean"))
        goals_per_game_ratio_dict=round(goals_per_game_ratio_df["goal_per_game_ratio"], 3).to_dict()

        return goals_per_game_ratio_dict


    def cummulative_goals_scored(self, df):
        cummulative_goals_df=df.groupby(["player_name", pd.Grouper(key="date", freq="D")])["goals"].sum().groupby(level=0).cumsum()
        cummulative_goals_df=cummulative_goals_df.reset_index(drop=False, inplace=False)
        cummulative_goals_df["date"]=cummulative_goals_df["date"].dt.strftime(date_format="%Y-%m-%d")

        cummulative_goal_dict=cummulative_goals_df.to_dict("records")
        cummulative_goals_graph_options=self.echart_goals_scored_options_creation.cummulative_goals_scored_line_graph(source_data=cummulative_goal_dict)

        return cummulative_goals_graph_options
    

    def goals_scored_per_year(self, df):
        goals_scored_per_year_df=df.groupby(["player_name", pd.Grouper(key="date", freq="YE")])["goals"].sum()
        goals_scored_per_year_df=goals_scored_per_year_df.reset_index(drop=False, inplace=False)
        goals_scored_per_year_df["date"]=goals_scored_per_year_df["date"].dt.strftime(date_format="%Y")

        goals_scored_per_year_dict=goals_scored_per_year_df.to_dict("records")
        goals_per_year_graph_options=self.echart_goals_scored_options_creation.goals_scored_per_year_bar_graph(source_data=goals_scored_per_year_dict)

        return goals_per_year_graph_options
    

    def goals_per_game_by_competition_type(self, df):
        goals_per_game_by_competition_type_df=(df.groupby(["player_name", "competition_type"], as_index=False).\
                                               agg(goal_count=("goals", "sum"),
                                                   total_games=("date", "count"),
                                                   goal_per_game_ratio=("goals", "mean")))
        
        # Goals Per Game Ratio
        goals_per_game_ratio_by_competition_type_dict=goals_per_game_by_competition_type_df[["player_name", "competition_type", "goal_per_game_ratio"]].to_dict("records")
        goals_scored_per_competition_type_ratio_options=self.echart_goals_scored_options_creation.goals_scored_per_competition_type_ratio(source_data=goals_per_game_ratio_by_competition_type_dict)
        
        # Goals Per Game Sum
        goals_per_game_sum_by_competition_type_dict=goals_per_game_by_competition_type_df[["player_name", "competition_type", "goal_count"]].to_dict("records")
        goals_scored_per_competition_type_sum_options=self.echart_goals_scored_options_creation.\
            goals_scored_per_competition_type_sum(source_data=goals_per_game_sum_by_competition_type_dict)

        # Final Dictionary
        goals_per_game_by_competition_type_options={"goals_per_game_ratio": goals_scored_per_competition_type_ratio_options,
                                                    "goals_per_game_sum": goals_scored_per_competition_type_sum_options}

        return goals_per_game_by_competition_type_options


    def goals_scored_and_match_outcome(self, df):
        goals_scored_and_match_outcome_df=df.groupby(["player_name", pd.Grouper(key="date", freq="D"), "result"])["goals"].sum()
        goals_scored_and_match_outcome_df=goals_scored_and_match_outcome_df.reset_index(drop=False, inplace=False)
        goals_scored_and_match_outcome_df["date"]=goals_scored_and_match_outcome_df["date"].dt.strftime(date_format="%Y-%m-%d")

        goals_scored_and_match_outcome_df["data"]=goals_scored_and_match_outcome_df[["date", "result" , "goals"]].values.tolist()

        player_heatmap_options_dict={}
        for player in self.players:
            goals_scored_and_match_outcome_player_df=goals_scored_and_match_outcome_df[goals_scored_and_match_outcome_df["player_name"]==player].reset_index(drop=True, inplace=False)

            heatmap_x=goals_scored_and_match_outcome_player_df["date"].values.tolist()
            heatmap_y=goals_scored_and_match_outcome_player_df["result"].unique().tolist()
            heatmap_y.sort()
            heatmap_data=goals_scored_and_match_outcome_player_df["data"].values.tolist()
            heatmap_min_value=int(goals_scored_and_match_outcome_player_df["goals"].min())
            heatmap_max_value=int(goals_scored_and_match_outcome_player_df["goals"].max())

            goals_scored_and_match_outcome_options=self.echart_goals_scored_options_creation.goals_scored_and_match_outcome_heatmap(player=player,
                                                                                                                                    series_data=heatmap_data, 
                                                                                                                                    x_axis_data=heatmap_x, 
                                                                                                                                    y_axis_data=heatmap_y,
                                                                                                                                    min_value=heatmap_min_value, 
                                                                                                                                    max_value=heatmap_max_value)
            player_heatmap_options_dict[player]=goals_scored_and_match_outcome_options

        return player_heatmap_options_dict

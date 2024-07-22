import pandas as pd

from general_components.sql_data_queries import SQLQueries
from echart_graphs.echart_options import EChartConsistencyOptionsCreation
from general_components.components import GeneralComponents


class ConsistencyAnalytics:
    def __init__(self):  
        self.sql_queries=SQLQueries()
        self.echart_consistency_options_creation=EChartConsistencyOptionsCreation()
        self.general_components=GeneralComponents()


    def number_of_contributions(self, df):
        contributions_per_player_df=df.groupby("player_name")["total_contributions"].sum()
        contributions_per_player_dict=contributions_per_player_df.to_dict()

        return contributions_per_player_dict
    

    def contributions_per_game_ratio(self, df):
        contributions_per_player_ratio=df.groupby(["player_name"], as_index=True).agg(contribution_per_game_ratio=("total_contributions", "mean"))
        contributions_per_player_ratio_dict=round(contributions_per_player_ratio["contribution_per_game_ratio"], 3).to_dict()

        return contributions_per_player_ratio_dict
    

    def match_availability_ratio(self, df):
        match_availability_per_player_df=(df[df["game_played"]=="Played"].groupby(["player_name", "game_played"], as_index=False).\
                                          agg(games_played_count=("game_played", "count")))
        total_matches_per_player_df=df.groupby(["player_name"], as_index=False)["date"].count().rename(columns={"date": "total_games"})
        match_availability_ratio=pd.merge(left=match_availability_per_player_df,
                                          right=total_matches_per_player_df,
                                          how="left",
                                          on="player_name")
        match_availability_ratio["availability_ratio"]=match_availability_ratio["games_played_count"]/match_availability_ratio["total_games"]
        match_availability_ratio["availability_ratio"]=match_availability_ratio["availability_ratio"]*100
        match_availability_ratio["availability_ratio"]=round(match_availability_ratio["availability_ratio"], 2)

        match_availability_ratio=match_availability_ratio[["player_name", "availability_ratio"]]
        match_availability_ratio=match_availability_ratio.set_index("player_name")
        match_availability_ratio_dict=match_availability_ratio.to_dict()
        match_availability_ratio_dict=match_availability_ratio_dict["availability_ratio"]
        
        return match_availability_ratio_dict


    def contributions_per_game_and_contribution_per_game_ratio(self, df):
        df["num_games"]=1
        contributions_cumsum_df=df.groupby(["player_name", pd.Grouper(key="date", freq="YE")])[["total_contributions", "num_games"]].sum().\
            groupby(level=0).cumsum().reset_index()
        
        contributions_cumsum_df["contribution_ratio"]=contributions_cumsum_df["total_contributions"]/contributions_cumsum_df["num_games"]
        contributions_cumsum_df["contribution_ratio"]=contributions_cumsum_df["contribution_ratio"].round(3)

        contributions_cumsum_df["date"]=contributions_cumsum_df["date"].dt.strftime(date_format="%Y-%m-%d")
        contributions_cumsum_df=contributions_cumsum_df[["player_name", "date", "total_contributions", "contribution_ratio"]]
        contributions_cumsum_dict=contributions_cumsum_df.to_dict("records")

        contributions_per_game_ratio_options=self.echart_consistency_options_creation.\
            contribution_and_match_outcome_bar_and_line_chart(source_data=contributions_cumsum_dict)
        
        return contributions_per_game_ratio_options
    

    def minutes_played_per_year(self, df):
        minutes_played_per_year_df=df.groupby(["player_name", pd.Grouper(key="date", freq="YE")])["minutes"].mean().reset_index(drop=False, inplace=False)
        minutes_played_per_year_df["date"]=minutes_played_per_year_df["date"].dt.strftime(date_format="%Y-%m-%d")
        minutes_played_per_year_df["minutes"]=minutes_played_per_year_df["minutes"].round(2)
        minutes_played_per_year_dict=minutes_played_per_year_df.to_dict("records")

        minutes_played_per_year_options=self.echart_consistency_options_creation.minutes_played_per_year_area_chart(source_data=minutes_played_per_year_dict)

        return minutes_played_per_year_options
    

    def match_availability_per_year(self, df):
        match_availability_per_year_df=df.groupby(["player_name", pd.Grouper(key="date", freq="YE")])["game_played"].\
            value_counts(normalize=True).\
                reset_index(drop=False, inplace=False)
        
        match_availability_per_year_df=match_availability_per_year_df[match_availability_per_year_df["game_played"]=="Played"].reset_index(drop=True, inplace=False)
        match_availability_per_year_df["proportion"]=round(match_availability_per_year_df["proportion"]*100, 2)
        match_availability_per_year_df=match_availability_per_year_df.rename(columns={"proportion": "Ratio"})
        match_availability_per_year_df=match_availability_per_year_df.drop(columns=["game_played"])
        match_availability_per_year_df["date"]=match_availability_per_year_df["date"].dt.strftime(date_format="%Y-%m-%d")
        match_availability_per_year_dict=match_availability_per_year_df.to_dict("records")

        ratio_of_games_played_per_year_options=self.echart_consistency_options_creation.game_availability_per_year_bar_chart(source_data=match_availability_per_year_dict)

        return ratio_of_games_played_per_year_options

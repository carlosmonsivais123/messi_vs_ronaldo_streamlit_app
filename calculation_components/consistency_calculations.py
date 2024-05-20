import pandas as pd

from database_components.sql_to_df import SQLToDataframe
from sql_queries.sql_data_queries import SQLQueries
from echart_graphs.echart_options import EChartConsistencyOptionsCreation
from general_components.components import GeneralComponents

class ConsistencyAnalytics:
    def __init__(self, mysql_table_name, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):  
        self.sql_queries=SQLQueries(table_name=mysql_table_name)
        self.sql_to_dataframe=SQLToDataframe(mysql_username=mysql_username, 
                                             mysql_password=mysql_password, 
                                             mysql_host=mysql_host, 
                                             mysql_port=mysql_port, 
                                             mysql_db_name=mysql_db_name)
        self.echart_consistency_options_creation=EChartConsistencyOptionsCreation()
        self.general_components=GeneralComponents()


    def consistency_data_df(self):
        consistency_page_sql_query=self.sql_queries.consistency_page_query()
        consistency_df=self.sql_to_dataframe.execute_sql_to_df(sql_query=consistency_page_sql_query,
                                                               date_column="date")
        
        competition_type_function=self.general_components.competition_type_dictionary_argcontains
        consistency_df["competition_type"]=consistency_df["competition"].map(competition_type_function)
        
        return consistency_df


    def competition_type_filter(self, df):
        competition_type_values=df["competition_type"].unique().tolist()
        competition_type_values=list(set(competition_type_values))

        return competition_type_values
    

    def consistency_data_df_filtered(self, df, competition_type_filters):
        if len(competition_type_filters) > 0:
            df=df[df["competition_type"].isin(competition_type_filters)]
            df=df.reset_index(drop=True, inplace=False)

        elif len(competition_type_filters) > 0:
            pass

        return df


    def number_of_contributions(self, df):
        contributions_per_player_df=df.groupby("player_name")["total_contributions"].sum()
        contributions_per_player_dict=contributions_per_player_df.to_dict()

        return contributions_per_player_dict
    

    def contributions_per_game_ratio(self, df):
        contributions_per_player_ratio=df.groupby(["player_name"], as_index=True).agg(contribution_per_game_ratio=("total_contributions", "mean"))
        contributions_per_player_ratio_dict=round(contributions_per_player_ratio["contribution_per_game_ratio"], 3).to_dict()

        return contributions_per_player_ratio_dict
    

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


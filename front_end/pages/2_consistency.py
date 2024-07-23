import streamlit as st
from streamlit_echarts import st_echarts

from calculation_components.consistency_page_calculations import ConsistencyAnalytics
from general_components.sidebar_values import SidebarFilterValues
from general_components.sql_data_queries import SQLQueries

sql_queries=SQLQueries()
consistency_analytics=ConsistencyAnalytics()
sidebar_filter_values=SidebarFilterValues()

# Page Title and Layout
st.set_page_config(page_title="Consistency", layout="wide")
st.markdown("<h1 style='text-align: center;'>Consistency</h1>", unsafe_allow_html=True)

# Sidebar Filters
unique_team_filters=sidebar_filter_values.unique_teams_filter_options()
unique_general_competition_type_filters=sidebar_filter_values.general_competition_type_filter()
messi_team_options=st.sidebar.multiselect("Lionel Messi Teams",
                                          unique_team_filters["Lionel Messi"])
ronaldo_team_options=st.sidebar.multiselect("Cristiano Ronaldo Teams",
                                            unique_team_filters["Cristiano Ronaldo"])
general_competition_type_options=st.sidebar.multiselect("General Competition Type",
                                                        unique_general_competition_type_filters)
start_date=st.sidebar.date_input("Start Date", value=None)
end_date=st.sidebar.date_input("End Date", value=None)

# Filtered Dataframe
consistency_df_filtered=sql_queries.filtered_sql_query_builder(messi_teams_filter=messi_team_options, 
                                                      ronaldo_teams_filter=ronaldo_team_options, 
                                                      general_competition_filter=general_competition_type_options, 
                                                      start_date=start_date, 
                                                      end_date=end_date)

# Page Graph Outputs
tile_height=110

total_contributions_per_player=consistency_analytics.number_of_contributions(df=consistency_df_filtered)
contributions_per_player_ratio=consistency_analytics.contributions_per_game_ratio(df=consistency_df_filtered)
availability_per_player_ratio=consistency_analytics.match_availability_ratio(df=consistency_df_filtered)

availibility_ratio_messi=availability_per_player_ratio["Lionel Messi"]
metric_col1, metric_col2, metric_col3=st.columns(3)
tile1=metric_col1.container(height=tile_height)
tile2=metric_col2.container(height=tile_height)
tile3=metric_col3.container(height=tile_height)
tile1.metric(label="Lionel Messi Contributions", value=total_contributions_per_player["Lionel Messi"])
tile2.metric(label="Lionel Messi Contributions/Game", value=contributions_per_player_ratio["Lionel Messi"])
tile3.metric(label="Lionel Messi Match Availability", value=f"{availibility_ratio_messi}%")

availibility_ratio_cr7=availability_per_player_ratio["Cristiano Ronaldo"]
metric_col4, metric_col5, metric_col6=st.columns(3)
tile4=metric_col4.container(height=tile_height)
tile5=metric_col5.container(height=tile_height)
tile6=metric_col6.container(height=tile_height)
tile4.metric(label="Cristiano Ronaldo Contributions", value=total_contributions_per_player["Cristiano Ronaldo"])
tile5.metric(label="Cristiano Ronaldo Contributions/Game", value=contributions_per_player_ratio["Cristiano Ronaldo"])
tile6.metric(label="Cristiano Ronaldo Match Availability", value=f"{availibility_ratio_cr7}%")

contributions_per_game_ratio_options=consistency_analytics.contributions_per_game_and_contribution_per_game_ratio(df=consistency_df_filtered)
st_echarts(options=contributions_per_game_ratio_options)

graph_col1, graph_col2=st.columns(2)
minutes_played_per_year_options=consistency_analytics.minutes_played_per_year(df=consistency_df_filtered)
games_per_year_ratio=consistency_analytics.match_availability_per_year(df=consistency_df_filtered)
with graph_col1:
    st_echarts(options=minutes_played_per_year_options)
with graph_col2:
    st_echarts(options=games_per_year_ratio)

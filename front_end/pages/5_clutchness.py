import streamlit as st
from streamlit_echarts import st_echarts

from general_components.sidebar_values import SidebarFilterValues
from calculation_components.clutchness_page_calculations import ClutchnessAnalytics
from general_components.sql_data_queries import SQLQueries

sql_queries=SQLQueries()
clutchness_analytics=ClutchnessAnalytics()
sidebar_filter_values=SidebarFilterValues()

# Page Title and Layout
st.set_page_config(page_title="Clutchness", layout="wide")
st.markdown("<h1 style='text-align: center;'>Clutchness</h1>", unsafe_allow_html=True)

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
filtered_goals_scored_df=sql_queries.filtered_sql_query_builder(messi_teams_filter=messi_team_options, 
                                                                ronaldo_teams_filter=ronaldo_team_options, 
                                                                general_competition_filter=general_competition_type_options, 
                                                                start_date=start_date, 
                                                                end_date=end_date)
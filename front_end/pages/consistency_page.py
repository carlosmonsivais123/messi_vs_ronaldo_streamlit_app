import streamlit as st
from streamlit_echarts import st_echarts

from general_components.sidebar_values import SidebarFilterValues
from calculation_components.consistency_calculations import ConsistencyAnalytics

consistency_analytics=ConsistencyAnalytics(mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"], 
                                           mysql_username=st.secrets["mysql_db_credentials"]["MYSQL_USERNAME"], 
                                           mysql_password=st.secrets["mysql_db_credentials"]["MYSQL_PASSWORD"], 
                                           mysql_host=st.secrets["mysql_db_credentials"]["MYSQL_HOST"], 
                                           mysql_port=st.secrets["mysql_db_credentials"]["MYSQL_PORT"], 
                                           mysql_db_name=st.secrets["mysql_db_credentials"]["MYSQL_DB_NAME"])

sidebar_filter_values=SidebarFilterValues(mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"], 
                                           mysql_username=st.secrets["mysql_db_credentials"]["MYSQL_USERNAME"], 
                                           mysql_password=st.secrets["mysql_db_credentials"]["MYSQL_PASSWORD"], 
                                           mysql_host=st.secrets["mysql_db_credentials"]["MYSQL_HOST"], 
                                           mysql_port=st.secrets["mysql_db_credentials"]["MYSQL_PORT"], 
                                           mysql_db_name=st.secrets["mysql_db_credentials"]["MYSQL_DB_NAME"])


st.set_page_config(page_title="Consistency", layout="wide")
st.markdown("<h1 style='text-align: center;'>Consistency</h1>", unsafe_allow_html=True)


consistency_df=consistency_analytics.consistency_data_df()


# Sidebar Filters Player Teams
filter_col1, filter_col2=st.sidebar.columns(2)
unique_team_filters=sidebar_filter_values.unique_teams_filter_options()
with filter_col1:
    messi_team_options=st.sidebar.multiselect("Lionel Messi Teams",
                                    unique_team_filters["Lionel Messi"])
with filter_col2:
    ronaldo_team_options=st.sidebar.multiselect("Cristiano Ronaldo Teams",
                                        unique_team_filters["Cristiano Ronaldo"])
    

# Sidebar Filters Competition Type
unique_general_competition_type_filters=sidebar_filter_values.competition_type_filter(df=consistency_df)
general_competition_type_options=st.sidebar.multiselect("Competition Type",
                                                        unique_general_competition_type_filters)


consistency_df_filtered=consistency_analytics.consistency_data_df_filtered(df=consistency_df, 
                                                                           competition_type_filters=general_competition_type_options)

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5, metric_col6=st.columns(6)
total_contributions_per_player=consistency_analytics.number_of_contributions(df=consistency_df_filtered)
contributions_per_player_ratio=consistency_analytics.contributions_per_game_ratio(df=consistency_df_filtered)
availability_per_player_ratio=consistency_analytics.match_availability_ratio(df=consistency_df_filtered)
with metric_col1:
    st.metric(label="Lionel Messi Contributions", 
              value=total_contributions_per_player["Lionel Messi"])
with metric_col2:
    st.metric(label="Lionel Messi Contributions/Game", 
              value=contributions_per_player_ratio["Lionel Messi"])
with metric_col3:
    availibility_ratio_messi=availability_per_player_ratio["Lionel Messi"]
    st.metric(label="Lionel Messi Match Availability", 
              value=f"{availibility_ratio_messi}%")

with metric_col4:
    st.metric(label="Cristiano Ronaldo Contributions", 
              value=total_contributions_per_player["Cristiano Ronaldo"])
with metric_col5:
    st.metric(label="Cristiano Ronaldo Contributions/Game", 
              value=contributions_per_player_ratio["Cristiano Ronaldo"])
    
with metric_col6:
    availibility_ratio_cr7=availability_per_player_ratio["Cristiano Ronaldo"]
    st.metric(label="Cristiano Ronaldo Match Availability", 
              value=f"{availibility_ratio_cr7}%")
    

contributions_per_game_ratio_options=consistency_analytics.contributions_per_game_and_contribution_per_game_ratio(df=consistency_df_filtered)
st_echarts(options=contributions_per_game_ratio_options)

graph_col1, graph_col2=st.columns(2)
minutes_played_per_year_options=consistency_analytics.minutes_played_per_year(df=consistency_df_filtered)
games_per_year_ratio=consistency_analytics.match_availability_per_year(df=consistency_df_filtered)
with graph_col1:
    st_echarts(options=minutes_played_per_year_options)
with graph_col2:
    st_echarts(options=games_per_year_ratio)

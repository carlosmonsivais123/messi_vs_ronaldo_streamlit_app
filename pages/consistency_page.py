import streamlit as st
from streamlit_echarts import st_echarts

from calculation_components.consistency_calculations import ConsistencyAnalytics

consistency_analytics=ConsistencyAnalytics(mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"], 
                                            mysql_username=st.secrets["mysql_db_credentials"]["MYSQL_USERNAME"], 
                                            mysql_password=st.secrets["mysql_db_credentials"]["MYSQL_PASSWORD"], 
                                            mysql_host=st.secrets["mysql_db_credentials"]["MYSQL_HOST"], 
                                            mysql_port=st.secrets["mysql_db_credentials"]["MYSQL_PORT"], 
                                            mysql_db_name=st.secrets["mysql_db_credentials"]["MYSQL_DB_NAME"])

st.set_page_config(page_title="Consistency", layout="wide")
st.markdown("<h1 style='text-align: center;'>Consistency</h1>", unsafe_allow_html=True)

consistency_df=consistency_analytics.consistency_data_df()

unique_general_compeittion_type_filters=consistency_analytics.competition_type_filter(df=consistency_df)
general_competition_type_options=st.multiselect("Competition Type",
                                                unique_general_compeittion_type_filters)

consistency_df_filtered=consistency_analytics.consistency_data_df_filtered(df=consistency_df, 
                                                                           competition_type_filters=general_competition_type_options)

metric_col1, metric_col2, metric_col3, metric_col4=st.columns(4)
total_contributions_per_player=consistency_analytics.number_of_contributions(df=consistency_df_filtered)
contributions_per_player_ratio=consistency_analytics.contributions_per_game_ratio(df=consistency_df_filtered)
with metric_col1:
    st.metric(label="Lionel Messi Number of Contributions", 
              value=total_contributions_per_player["Lionel Messi"])
with metric_col2:
    st.metric(label="Lionel Messi Contributions Per Game", 
              value=contributions_per_player_ratio["Lionel Messi"])
with metric_col3:
    st.metric(label="Cristiano Ronaldo Number of Contributions", 
              value=total_contributions_per_player["Cristiano Ronaldo"])
with metric_col4:
    st.metric(label="Cristiano Ronaldo Contributions Per Game", 
              value=contributions_per_player_ratio["Cristiano Ronaldo"])
    

contributions_per_game_ratio_options=consistency_analytics.contributions_per_game_and_contribution_per_game_ratio(df=consistency_df_filtered)
st_echarts(options=contributions_per_game_ratio_options)

minutes_played_per_year_options=consistency_analytics.minutes_played_per_year(df=consistency_df_filtered)
st_echarts(options=minutes_played_per_year_options)


import streamlit as st
from streamlit_echarts import st_echarts

from calculation_components.goals_scored_calculations import GoalsScoredAnalytics

goals_scored_analytics=GoalsScoredAnalytics(mysql_table_name=st.secrets["mysql_db_credentials"]["MYSQL_TABLE_NAME"], 
                                            mysql_username=st.secrets["mysql_db_credentials"]["MYSQL_USERNAME"], 
                                            mysql_password=st.secrets["mysql_db_credentials"]["MYSQL_PASSWORD"], 
                                            mysql_host=st.secrets["mysql_db_credentials"]["MYSQL_HOST"], 
                                            mysql_port=st.secrets["mysql_db_credentials"]["MYSQL_PORT"], 
                                            mysql_db_name=st.secrets["mysql_db_credentials"]["MYSQL_DB_NAME"])
cummulative_goals_graph_options=goals_scored_analytics.cummulative_goals_scored()
goals_scored_per_year_graph_options=goals_scored_analytics.goals_scored_per_year()
goals_scored_and_match_outcome_options=goals_scored_analytics.goals_scored_and_match_outcome()

st.set_page_config(page_title="Goals Scored")
st.markdown("Goals Scored")

st_echarts(options=cummulative_goals_graph_options)
st_echarts(options=goals_scored_per_year_graph_options)

# Messi
st_echarts(options=goals_scored_and_match_outcome_options["Lionel Messi"])

# Ronaldo
st_echarts(options=goals_scored_and_match_outcome_options["Cristiano Ronaldo"])

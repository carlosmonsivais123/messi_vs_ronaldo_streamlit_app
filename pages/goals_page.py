import streamlit as st
from streamlit_echarts import st_echarts

from calculation_components.goals_scored_calculations import GoalsScoredAnalytics

goals_scored_analytics=GoalsScoredAnalytics()
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

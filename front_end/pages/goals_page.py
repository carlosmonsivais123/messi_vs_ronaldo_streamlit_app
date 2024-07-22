import streamlit as st
from streamlit_echarts import st_echarts

from calculation_components.goals_scored_calculations import GoalsScoredAnalytics
from general_components.sidebar_values import SidebarFilterValues


goals_scored_analytics=GoalsScoredAnalytics()
sidebar_filter_values=SidebarFilterValues()


st.set_page_config(page_title="Goals", layout="wide")
st.markdown("<h1 style='text-align: center;'>Goals</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Goals Scored</h3>", unsafe_allow_html=True)

# Sidebar Filters Player Teams
filter_col1, filter_col2=st.sidebar.columns(2)
unique_team_filters=sidebar_filter_values.unique_teams_filter_options()
with filter_col1:
    messi_team_options=st.sidebar.multiselect("Lionel Messi Teams",
                                              unique_team_filters["Lionel Messi"])
with filter_col2:
    ronaldo_team_options=st.sidebar.multiselect("Cristiano Ronaldo Teams",
                                                unique_team_filters["Cristiano Ronaldo"])
    
start_date=st.sidebar.date_input("Start Date", value=None)
end_date=st.sidebar.date_input("End Date", value=None)

print(start_date)
print(end_date)


filtered_goals_scored_df=goals_scored_analytics.filtered_goals_scored_df(messi_team_options=messi_team_options, 
                                                                         ronaldo_team_options=ronaldo_team_options)

# Sidebar Filters Competition Type
unique_general_competition_type_filters=sidebar_filter_values.competition_type_filter(df=filtered_goals_scored_df)
general_competition_type_options=st.sidebar.multiselect("General Competition Type",
                                                        unique_general_competition_type_filters)




goals_scored_analytics.filtered_df_test(messi_teams_filter=messi_team_options, 
                                        ronaldo_teams_filter=ronaldo_team_options, 
                                        general_competition_filter=general_competition_type_options, 
                                        start_date=start_date, 
                                        end_date=end_date)


metric_col1, metric_col2, metric_col3, metric_col4=st.columns(4)
goals_scored_metrics=goals_scored_analytics.goals_scored_metric_value(df=filtered_goals_scored_df)
goals_per_game_metric=goals_scored_analytics.goals_ratio_metric_value(df=filtered_goals_scored_df)
with metric_col1:
    st.metric(label="Lionel Messi Goals Scored", 
              value=goals_scored_metrics["Lionel Messi"])
with metric_col2:
    st.metric(label="Lionel Messi Goals Per Game", 
              value=goals_per_game_metric["Lionel Messi"])
with metric_col3:
    st.metric(label="Cristiano Ronaldo Goals Scored", 
              value=goals_scored_metrics["Cristiano Ronaldo"])
with metric_col4:
    st.metric(label="Cristiano Ronaldo Goals Per Game", 
              value=goals_per_game_metric["Cristiano Ronaldo"])


graph_col1, graph_col2=st.columns(2)
cummulative_goals_graph_options=goals_scored_analytics.cummulative_goals_scored(df=filtered_goals_scored_df)
goals_scored_per_year_graph_options=goals_scored_analytics.goals_scored_per_year(df=filtered_goals_scored_df)
with graph_col1:
    st_echarts(options=cummulative_goals_graph_options)
with graph_col2:
    st_echarts(options=goals_scored_per_year_graph_options)

graph_col3, graph_col4=st.columns(2)
goals_per_game_options=goals_scored_analytics.goals_per_game_by_competition_type(df=filtered_goals_scored_df)
with graph_col3:
    st_echarts(options=goals_per_game_options["goals_per_game_ratio"])
with graph_col4:
    st_echarts(options=goals_per_game_options["goals_per_game_sum"])

st.markdown("<h3 style='text-align: center;'>Goals by Match Outcome</h3>", unsafe_allow_html=True)
graph_col5, graph_col6=st.columns(2)
goals_scored_and_match_outcome_options=goals_scored_analytics.goals_scored_and_match_outcome(df=filtered_goals_scored_df)
with graph_col5:
    st_echarts(options=goals_scored_and_match_outcome_options["Lionel Messi"])
with graph_col6:
    st_echarts(options=goals_scored_and_match_outcome_options["Cristiano Ronaldo"])

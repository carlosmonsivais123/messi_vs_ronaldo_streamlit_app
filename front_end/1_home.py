import streamlit as st

from general_components.sidebar_values import SidebarFilterValues
from general_components.sql_data_queries import SQLQueries
from calculation_components.home_page_calculations import HomePageAnalytics

sql_queries=SQLQueries()
sidebar_filter_values=SidebarFilterValues()
home_page_analytics=HomePageAnalytics()

# Page Title and Layout
st.set_page_config(page_title="Home", layout="wide")
st.markdown("<h1 style='text-align: center;'>Lionel Messi vs Cristiano Ronaldo</h1>", unsafe_allow_html=True)

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
filtered_df=sql_queries.filtered_sql_query_builder(messi_teams_filter=messi_team_options, 
                                                                ronaldo_teams_filter=ronaldo_team_options, 
                                                                general_competition_filter=general_competition_type_options, 
                                                                start_date=start_date, 
                                                                end_date=end_date)

# Page Graph Outputs
general_statistics_dict=home_page_analytics.player_information_metric_values(df=filtered_df)
difference_statistics_dict=home_page_analytics.difference_values(metric_dict=general_statistics_dict)

tile_height=110
row1, row2=st.columns(2)
tile1=row1.container(height=tile_height)
tile2=row2.container(height=tile_height)
tile1.title("Lionel Messi")
tile2.title("Cristiano Ronaldo")

row3, row4, row5, row6=st.columns(4)
tile3=row3.container(height=tile_height)
tile4=row4.container(height=tile_height)
tile5=row5.container(height=tile_height)
tile6=row6.container(height=tile_height)
tile3.metric('Games Played', general_statistics_dict['Games Played']['Lionel Messi'], difference_statistics_dict['dif3'])
tile4.metric('Minutes Played', general_statistics_dict['Minutes Played']['Lionel Messi'], difference_statistics_dict['dif4'])
tile5.metric('Games Played', general_statistics_dict['Games Played']['Cristiano Ronaldo'], difference_statistics_dict['dif5'])
tile6.metric('Minutes Played', general_statistics_dict['Minutes Played']['Cristiano Ronaldo'], difference_statistics_dict['dif6'])

row7, row8, row9, row10, row11, row12=st.columns(6)
tile7=row7.container(height=tile_height)
tile8=row8.container(height=tile_height)
tile9=row9.container(height=tile_height)
tile10=row10.container(height=tile_height)
tile11=row11.container(height=tile_height)
tile12=row12.container(height=tile_height)
tile7.metric('Goals', general_statistics_dict['Goals']['Lionel Messi'], difference_statistics_dict['dif7'])
tile8.metric('Assists', general_statistics_dict['Assists']['Lionel Messi'], difference_statistics_dict['dif8'])
tile9.metric('Contributions', general_statistics_dict['Contributions']['Lionel Messi'], difference_statistics_dict['dif9'])
tile10.metric('Goals', general_statistics_dict['Goals']['Cristiano Ronaldo'], difference_statistics_dict['dif10'])
tile11.metric('Assists', general_statistics_dict['Assists']['Cristiano Ronaldo'], difference_statistics_dict['dif11'])
tile12.metric('Contributions', general_statistics_dict['Contributions']['Cristiano Ronaldo'], difference_statistics_dict['dif12'])

row13, row14, row15, row16, row17, row18=st.columns(6)
tile13=row13.container(height=tile_height)
tile14=row14.container(height=tile_height)
tile15=row15.container(height=tile_height)
tile16=row16.container(height=tile_height)
tile17=row17.container(height=tile_height)
tile18=row18.container(height=tile_height)
tile13.metric('Goals/Game', general_statistics_dict['Goals Per Game']['Lionel Messi'], difference_statistics_dict['dif13'])
tile14.metric('Assists/Game', general_statistics_dict['Assists Per Game']['Lionel Messi'], difference_statistics_dict['dif14'])
tile15.metric('Contributions/Game', general_statistics_dict['Contributions Per Game']['Lionel Messi'], difference_statistics_dict['dif15'])
tile16.metric('Goals/Game', general_statistics_dict['Goals Per Game']['Cristiano Ronaldo'], difference_statistics_dict['dif16'])
tile17.metric('Assists/Game', general_statistics_dict['Assists Per Game']['Cristiano Ronaldo'], difference_statistics_dict['dif17'])
tile18.metric('Contributions/Game', general_statistics_dict['Contributions Per Game']['Cristiano Ronaldo'], difference_statistics_dict['dif18'])

row19, row20, row21, row22, row23, row24=st.columns(6)
tile19=row19.container(height=tile_height)
tile20=row20.container(height=tile_height)
tile21=row21.container(height=tile_height)
tile22=row22.container(height=tile_height)
tile23=row23.container(height=tile_height)
tile24=row24.container(height=tile_height)
tile19.metric('Wins', general_statistics_dict['Wins']['Lionel Messi'], difference_statistics_dict['dif19'])
tile20.metric('Draws', general_statistics_dict['Draws']['Lionel Messi'], difference_statistics_dict['dif20'])
tile21.metric('Losses', general_statistics_dict['Losses']['Lionel Messi'], difference_statistics_dict['dif21'])
tile22.metric('Wins', general_statistics_dict['Wins']['Cristiano Ronaldo'], difference_statistics_dict['dif22'])
tile23.metric('Draws', general_statistics_dict['Draws']['Cristiano Ronaldo'], difference_statistics_dict['dif23'])
tile24.metric('Losses', general_statistics_dict['Losses']['Cristiano Ronaldo'], difference_statistics_dict['dif24'])

# Image
st.image('assets/images/goats.png')

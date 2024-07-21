import logging
import time

from general_components.read_vars import get_variable
from data_extraction.fbref_player_links_created import FBREFDataLinkCreation
from data_extraction.fbref_player_data_extraction import FBREFPlayerDataExtraction
from data_cleaning.clean_data import CleanData
from general_components.dataframe_concat import CombineFinalDataframes
from general_components.db_components import DatabaseComponents


# Logging setting
logging.basicConfig(level=logging.INFO)

# Classes being called
fbref_data_extraction_module=FBREFDataLinkCreation()
fbref_player_data_extraction=FBREFPlayerDataExtraction()
clean_data=CleanData()
combine_final_dataframes=CombineFinalDataframes()
database_components=DatabaseComponents(mysql_username=get_variable("MYSQL_USERNAME"),
                                       mysql_password=get_variable("MYSQL_PASSWORD"), 
                                       mysql_host=get_variable("MYSQL_HOST"), 
                                       mysql_port=get_variable("MYSQL_PORT"), 
                                       mysql_db_name=get_variable("MYSQL_DB_NAME"))

# Input values for process
players_list=[get_variable("PLAYER_1"), get_variable("PLAYER_2")]
player_dataframe_storage={}

# Data extraction process for each player
for player in players_list:
    logging.info(f'Extracting {player} Player Links')
    player_links=fbref_data_extraction_module.execute_fbref_data_link_created(player_name=player)

    logging.info(f'Requesting {player} Player Links Data')
    player_data_df=fbref_player_data_extraction.execute_fbref_data_extraction(player_links_list=player_links)

    logging.info(f'Cleaning {player} Data')
    clean_data_df=clean_data.execute_data_cleaning(df=player_data_df, player_name=player)
    player_dataframe_storage[player]=clean_data_df

    logging.info(f'Wating 10 Seconds For Next Player Request')
    time.sleep(10)

# Dataframes to MYSQL database
logging.info(f'Sending Data to MYSQL Database\n')
combined_player_dataframe=combine_final_dataframes.combine_final_dataframes_from_dict(player_data_dictionary=player_dataframe_storage)
database_components.execute_df_to_mysql_db(df=combined_player_dataframe, 
                                           output_table_name=get_variable("MYSQL_TABLE_NAME"))

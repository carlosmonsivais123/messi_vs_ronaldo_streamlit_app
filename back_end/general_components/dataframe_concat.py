import pandas as pd

class CombineFinalDataframes:
    '''
    Class to concatenate the final dataframes retrieved for each player into a single dataframe to push the data up to a single table.
    '''
    def combine_final_dataframes_from_dict(self, player_data_dictionary):
        '''
        Concatenates the dataframes retrieved from the player data extraction for each player into a single datafrrame to push up to the MYSQL 
        table as single table.

        @param player_data_dictionary: Dictionary with the key being the player's name and the value being the player's data stored as a dataframe

        @return final_df: Dataframe with the data for each player concatenated into a single table
        '''
        final_df=pd.DataFrame()
        for value in player_data_dictionary.values():
            final_df=pd.concat([final_df, value])

        final_df=final_df.drop_duplicates()
        final_df=final_df.reset_index(drop=True, inplace=False)

        return final_df

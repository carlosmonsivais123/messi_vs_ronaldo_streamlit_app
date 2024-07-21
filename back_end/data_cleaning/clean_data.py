import numpy as np
import pytz
from datetime import datetime

class CleanData:
    '''
    Class to clean the player's dataframes by formatting some values and add some features to each player's data.
    '''
    def result_splitting_formatting(self, df):
        '''
        Creates the features result and result_score where the feature result just shows whether it was a win, draw or loss and 
        the feature result_score shows gives the score of the game.

        @param df: Dataframe with the player's data

        @return df: Dataframe with the player's data with the two new features being result and result_score
        '''
        df['result_temp']=df['result'].str.split(' ', n=1).str[0].str.strip()
        df['result_score']=df['result'].str.split(' ', n=1).str[1].str.strip()

        df=df.drop(columns=['result'], inplace=False)
        df=df.rename(columns={'result_temp': 'result'})

        return df
    

    def penalty_shoot_out(self, df):
        '''
        Creates a new feature determining if the results were caused by a penalty shoot-out, and creates the features showing the score
        for and against if the game was determined by a penalty shoot-out.

        @param df: Dataframe with the player's data

        @return df: Dataframe with the player's data with the penalty-shoot out features
        '''
        penalty_shoot_out_pattern=r"^\d\s+\(\d\)"
        df['penalty_shoot_out']=df['result_score'].str.match(penalty_shoot_out_pattern)
        df['penalty_shoot_out']=df['penalty_shoot_out'].replace({False: "N",
                                                                 True: "Y"})
        
        penalty_shoot_out_score_pattern=r"\(\d+\)"
        df['penalty_shoot_out_score']=df['result_score'].str.findall(penalty_shoot_out_score_pattern)
        df['penalty_shoot_out_score']=df['penalty_shoot_out_score'].apply(lambda y: np.nan if len(y)==0 else y)
        df["penalty_shoot_out_score_for"]=df["penalty_shoot_out_score"].str[0]
        df["penalty_shoot_out_score_against"]=df["penalty_shoot_out_score"].str[1]

        penalty_shoot_out_score_values_pattern=r"\d+"
        df['penalty_shoot_out_score_for']=df['penalty_shoot_out_score_for'].str.findall(penalty_shoot_out_score_values_pattern)
        df['penalty_shoot_out_score_against']=df['penalty_shoot_out_score_against'].str.findall(penalty_shoot_out_score_values_pattern)
        df["penalty_shoot_out_score_for"]=df["penalty_shoot_out_score_for"].str[0].astype(float)
        df["penalty_shoot_out_score_against"]=df["penalty_shoot_out_score_against"].str[0].astype(float)

        df.loc[df['penalty_shoot_out_score_for']>df["penalty_shoot_out_score_against"], 'result'] = 'W'
        df.loc[df['penalty_shoot_out_score_for']<df["penalty_shoot_out_score_against"], 'result'] = 'L'

        df=df.drop(columns=['penalty_shoot_out_score', 'result_score'], inplace=False)

        return df
    

    def fill_certain_na_values(self, df):
        '''
        Filling in missing values by the selected columns

        @param df: Dataframe with the player's data

        @return df: Dataframe with the missing values filled in for the specified columns
        '''
        df['minutes']=df['minutes'].fillna(value=0)
        df['goals']=df['goals'].fillna(value=0)

        return df
    

    def player_name_formatting(self, df, player_name):
        '''
        Creating a feature where the player's name is specified and filling in all missing values with None throughout 
        the whole dataframe.

        @param df: Dataframe with the player's data
        @param player_name: String value representing the player's name

        @return df: Dataframe with the player's name as a feature and filled in missing values
        '''
        df['player_name']=player_name

        df=df.fillna(value=np.nan)
        df=df.replace({np.nan: None,
                       '': None})

        return df
    

    def competition_type_dictionary_argcontains(self, item):
        '''
        Competition type matching process based on the competition there is a general competition assigned as a feature.

        @param item: String value to be matched where the specific competition type is being matched with the general competition type

        @return i: String representing the matched general type
        '''
        competition_type_dict={"World Cup": ["World Cup"],
                               "League": ["Primeira Liga", "Premier League", "La Liga", "Serie A", "Pro League", "MLS", "Ligue 1"],
                               "Champions Lg & Europa Lg": ["Champions Lg", "UEFA Cup", "Europa Lg"],
                               "League Cups": ["Coupe de France", "Coppa Italia", "Copa del Rey", "Super Cup", "FA Cup", 
                                               "Trophée des Champions", "Supercopa de España", "Supercoppa"],
                               "Friendlies": ["Friendlies (M)"],
                               "International Tournaments": ["Copa América", "Copa América Centenario", "UEFA Nations League", 
                                                             "FIFA Confederations Cup", "UEFA Euro", "UEFA Euro Qualifying", "WCQ"]}

        for i, v in competition_type_dict.items():
            if item in v:
                return i
                    

    def create_features(self, df):
        '''
        Creates features such as the competition type being a more general competition type that can be compared between players,
        whether the player played the game or not, and the feature to show when the data was last updated.

        @parm df: Dataframe with the player's data

        @return df: Dataframe with the added features including competition_type, game_played and last_data_extract
        '''
        df["competition_type"]=df["competition"].map(self.competition_type_dictionary_argcontains)
        df['minutes']=df['minutes'].astype(float)
        df['game_played']=np.where(df["minutes"] > 0, "Played", "Not Played")

        pst_timezone=pytz.timezone('America/Los_Angeles')
        current_datetime=datetime.now(pst_timezone)
        current_date_time_str=current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        df["last_data_extract"]=current_date_time_str

        return df


    def dataframe_final_format(self, df):
        '''
        Sorts the final dataframes order by the date the game was played.

        @param df: Dataframe with the player's data

        @return df: Dataframe sorted by the date column
        '''
        df=df.sort_values(by='date', ascending=True, inplace=False)
        df=df.reset_index(drop=True, inplace=False)

        return df


    def execute_data_cleaning(self, df, player_name):
        '''
        Executes the data cleaning process including feature creation, column formatting, filling in missing values and
        sorting the dataframes final order.

        @param df: Dataframe with the player's data
        @param player_name: String value representing the player's name

        @return df_clean_6: Dataframe that has been cleaned through the data cleaning process
        '''
        df_clean_1=self.result_splitting_formatting(df=df)
        df_clean_2=self.penalty_shoot_out(df=df_clean_1)
        df_clean_3=self.fill_certain_na_values(df=df_clean_2)
        df_clean_4=self.player_name_formatting(df=df_clean_3, player_name=player_name)
        df_clean_5=self.create_features(df=df_clean_4)
        df_clean_6=self.dataframe_final_format(df=df_clean_5)

        return df_clean_6

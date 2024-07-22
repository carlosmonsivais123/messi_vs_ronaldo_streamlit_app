import pandas as pd

class HomePageAnalytics:
    def __init__(self):
        self.players=["Lionel Messi", "Cristiano Ronaldo"]


    def reformat_dataframe_to_player_level(self, df):
        df=df.transpose().\
            reset_index(drop=False, inplace=False)
        df=df.rename(columns=df.iloc[0]).drop(df.index[0])
        df=df.reset_index(drop=True, inplace=False)

        return df

    
    def player_information_metric_values(self, df):
        # Table Summary 1: Overall Averages and Sums
        table_summary_1_df=df.groupby('player_name', 
                                    as_index=False).\
                                        agg(goals_sum=('goals', 'sum'),
                                            goals_mean=('goals', 'mean'),
                                            assists_sum=('assists', 'sum'),
                                            assists_mean=('assists', 'mean'),
                                            minutes_sum=('minutes', 'sum'),
                                            total_contributions_sum=('total_contributions', 'sum'),
                                            total_contributions_mean=('total_contributions', 'mean'))
        table_summary_1_df=table_summary_1_df.rename(columns={'goals_sum': 'Goals',
                                                              'goals_mean': 'Goals Per Game',
                                                              'assists_sum': 'Assists',
                                                              'assists_mean': 'Assists Per Game',
                                                              'total_contributions_sum': 'Contributions',
                                                              'total_contributions_mean': 'Contributions Per Game',
                                                              'minutes_sum': 'Minutes Played',
                                                              'player_name': 'Statistics'})
        table_summary_1_df=self.reformat_dataframe_to_player_level(df=table_summary_1_df)

        # Table Summary 2: Games Played
        table_summary_2_df=df.groupby(['player_name', 'game_played'], 
                                      as_index=False).\
                                        agg(games=('date', 'count'))
        table_summary_2_df=table_summary_2_df[table_summary_2_df['game_played']=="Played"]
        table_summary_2_df=table_summary_2_df.rename(columns={'games': 'Games Played',
                                                              'player_name': 'Statistics'})
        table_summary_2_df=table_summary_2_df.drop(columns=["game_played"])
        table_summary_2_df=self.reformat_dataframe_to_player_level(df=table_summary_2_df)

        # Table Summary 3: Wins, Draws, Losses Count
        table_summary_3_df=df.groupby(['player_name', 'result'], 
                                      as_index=False).\
                                        agg(games=('date', 'count'))
        
        table_summary_3_df=table_summary_3_df.pivot_table(index='player_name',
                                                          columns='result',
                                                          values='games')
        table_summary_3_df=table_summary_3_df.reset_index(drop=False, inplace=False)
        table_summary_3_df=self.reformat_dataframe_to_player_level(df=table_summary_3_df)
        table_summary_3_df=table_summary_3_df.rename(columns={'player_name': 'Statistics'})
        replace_result_type={"W": "Wins", "D": "Draws", "L": 'Losses'}
        table_summary_3_df['Statistics']=table_summary_3_df['Statistics'].replace(replace_result_type, inplace=False)

        # Combine Table Summaries
        final_table_summary=pd.concat([table_summary_1_df, table_summary_2_df, table_summary_3_df], ignore_index=True)
        final_table_summary=final_table_summary.set_index("Statistics")
        final_table_summary["Cristiano Ronaldo"]=final_table_summary["Cristiano Ronaldo"].astype(float)
        final_table_summary["Lionel Messi"]=final_table_summary["Lionel Messi"].astype(float)
        final_table_summary["Cristiano Ronaldo"]=final_table_summary["Cristiano Ronaldo"].round(2)
        final_table_summary["Lionel Messi"]=final_table_summary["Lionel Messi"].round(2)
        
        # Convert to Dictionary for Metrics
        metric_values_dictionary=final_table_summary.to_dict('index')

        return metric_values_dictionary
    

    def difference_values(self, metric_dict):
        dif3=round(metric_dict['Games Played']['Lionel Messi']-metric_dict['Games Played']['Cristiano Ronaldo'], 2)
        dif4=round(metric_dict['Minutes Played']['Lionel Messi']-metric_dict['Minutes Played']['Cristiano Ronaldo'], 2)
        dif5=round(metric_dict['Games Played']['Cristiano Ronaldo']-metric_dict['Games Played']['Lionel Messi'], 2)
        dif6=round(metric_dict['Minutes Played']['Cristiano Ronaldo']-metric_dict['Minutes Played']['Lionel Messi'], 2)

        dif7=round(metric_dict['Goals']['Lionel Messi']-metric_dict['Goals']['Cristiano Ronaldo'], 2)
        dif8=round(metric_dict['Assists']['Lionel Messi']-metric_dict['Assists']['Cristiano Ronaldo'], 2)
        dif9=round(metric_dict['Contributions']['Lionel Messi']-metric_dict['Contributions']['Cristiano Ronaldo'], 2)
        dif10=round(metric_dict['Goals']['Cristiano Ronaldo']-metric_dict['Goals']['Lionel Messi'], 2)
        dif11=round(metric_dict['Assists']['Cristiano Ronaldo']-metric_dict['Assists']['Lionel Messi'], 2)
        dif12=round(metric_dict['Contributions']['Cristiano Ronaldo']-metric_dict['Contributions']['Lionel Messi'], 2)

        dif13=round(metric_dict['Goals Per Game']['Lionel Messi']-metric_dict['Goals Per Game']['Cristiano Ronaldo'], 2)
        dif14=round(metric_dict['Assists Per Game']['Lionel Messi']-metric_dict['Assists Per Game']['Cristiano Ronaldo'], 2)
        dif15=round(metric_dict['Contributions Per Game']['Lionel Messi']-metric_dict['Contributions Per Game']['Cristiano Ronaldo'], 2)
        dif16=round(metric_dict['Goals Per Game']['Cristiano Ronaldo']-metric_dict['Goals Per Game']['Lionel Messi'], 2)
        dif17=round(metric_dict['Assists Per Game']['Cristiano Ronaldo']-metric_dict['Assists Per Game']['Lionel Messi'], 2)
        dif18=round(metric_dict['Contributions Per Game']['Cristiano Ronaldo']-metric_dict['Contributions Per Game']['Lionel Messi'], 2)

        dif19=round(metric_dict['Wins']['Lionel Messi']-metric_dict['Wins']['Cristiano Ronaldo'], 2)
        dif20=round(metric_dict['Draws']['Lionel Messi']-metric_dict['Draws']['Cristiano Ronaldo'], 2)
        dif21=round(metric_dict['Losses']['Lionel Messi']-metric_dict['Losses']['Cristiano Ronaldo'], 2)
        dif22=round(metric_dict['Wins']['Cristiano Ronaldo']-metric_dict['Wins']['Lionel Messi'], 2)
        dif23=round(metric_dict['Draws']['Cristiano Ronaldo']-metric_dict['Draws']['Lionel Messi'], 2)
        dif24=round(metric_dict['Losses']['Cristiano Ronaldo']-metric_dict['Losses']['Lionel Messi'], 2)

        difference_values_dict={'dif3': dif3, "dif4": dif4, "dif5": dif5, "dif6": dif6,
                                'dif7': dif7, 'dif8': dif8, "dif9": dif9, 'dif10': dif10, 'dif11': dif11, 'dif12': dif12,
                                'dif13': dif13, 'dif14': dif14, 'dif15': dif15, 'dif16': dif16, 'dif17': dif17, 'dif18': dif18,
                                'dif19': dif19, 'dif20': dif20, 'dif21': dif21, 'dif22': dif22, 'dif23': dif23, 'dif24': dif24}
        
        return difference_values_dict
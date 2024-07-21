import requests
from bs4 import BeautifulSoup
import re
import time

class FBREFDataLinkCreation:
    '''
    Class to create the links for the specified player that will be parsed in a later section. These links include pages
    with data regarding the seasons and international tournaments for each player.
    '''
    def format_player_name_for_link(self, player_name):
        '''
        Formats the player's name to fit the links that will be created by replacing white-space ' ' values with dash values '-'.

        @param player_name: String value representing the player's name

        @return player_name_formatted: String with the re-formatted player name
        '''
        player_name_formatted=player_name.replace(" ", "-")

        return player_name_formatted

        
    def player_unique_link_code_search(self, player_name):
        '''
        Searches for the unique player code needed to search the player on the FBREF website, this is a unique identifier each
        player name must have when web scraping the player information.

        @param player_name: String of the formatted player name

        @return player_unique_identifier: String of unique numerical identifier for each player
        '''
        first_two_letters=player_name.split("-")[1][0:2].lower().strip()

        player_directory_text=requests.get(fr'https://fbref.com/en/players/{first_two_letters}/').text
        time.sleep(10)
        player_directory_link_text=BeautifulSoup(player_directory_text, features="html.parser")

        player_directory_link_search=player_directory_link_text.select(rf"a[href*= '/{player_name}']")
        player_directory_link=[i.attrs.get('href') for i in player_directory_link_search][0].strip()

        player_unique_identifier=player_directory_link.split('/')[3].strip()

        return player_unique_identifier


    def player_main_link_creator(self, player_name, player_unique_identifier):
        ''''
        Creates the general link directed towards the players general statistics. This link will be used to reformat it in order
        to extract the seasons and tournaments each player has played in.

        @param player_name: String of the formatted player name
        @param player_unique_identifier: String of unique numerical identifier for each player

        @return main_link: String representing the URL of the general link directed to the players general statistics
        '''
        main_link=rf"https://fbref.com/en/players/{player_unique_identifier}/all_comps/{player_name}-Stats---All-Competitions"
       
        return main_link

    
    def season_matchlog_links(self, player_name, fbref_player_url):
        '''
        Extracts the necessary links for each player at the season level which is inclusive of national team matches.

        @param player_name: String of the formatted player name
        @param fbref_player_url: String representing the URL of the general link directed to the players general statistics

        @return player_seasons_links_list_filter_5: List of player links that have been formatted to extract data from each player's season
        '''
        player_link_text=requests.get(fbref_player_url).text
        time.sleep(5)

        soup_player_link_text=BeautifulSoup(player_link_text, features="html.parser")

        player_seasons_links=soup_player_link_text.select(rf"a[href*= '/summary/{player_name}-Match-Logs']")
        player_seasons_links_list=[i.attrs.get('href') for i in player_seasons_links]

        # Removing national team stats since they are already included in season stats
        national_team_filter_regex=re.compile(r"nat\_tm")
        player_seasons_links_list_filter_1=[i for i in player_seasons_links_list if not national_team_filter_regex.search(i)]

        season_filter_regex_1=re.compile(r"matchlogs\/[0-9]{4}-[0-9]{4}\/summary")
        player_seasons_links_list_filter_2=[i for i in player_seasons_links_list_filter_1 if season_filter_regex_1.search(i)]

        season_filter_regex_2=re.compile(r"matchlogs\/[0-9]{4}\/summary")
        player_seasons_links_list_filter_3=[i for i in player_seasons_links_list_filter_1 if season_filter_regex_2.search(i)]

        player_seasons_links_list_filter_4=player_seasons_links_list_filter_2+player_seasons_links_list_filter_3

        player_seasons_links_list_filter_5=["https://fbref.com" + player_season_url for player_season_url in player_seasons_links_list_filter_4]
        player_seasons_links_list_filter_5=list(set(player_seasons_links_list_filter_5))

        return player_seasons_links_list_filter_5


    def execute_fbref_data_link_created(self, player_name):
        '''
        Executes the subprocesses to create the FBREF URL links that will be scraped for each player.

        @param player_name: String of the un-formatted player name

        @return player_season_matchlog_links: List with the URL links for each player that will be scraped
        '''
        formatted_player_name=self.format_player_name_for_link(player_name=player_name)

        player_identifier=self.player_unique_link_code_search(player_name=formatted_player_name)

        player_main_link=self.player_main_link_creator(player_name=formatted_player_name, 
                                                       player_unique_identifier=player_identifier) 
        
        player_season_matchlog_links=self.season_matchlog_links(player_name=formatted_player_name, 
                                                                fbref_player_url=player_main_link)
        
        return player_season_matchlog_links

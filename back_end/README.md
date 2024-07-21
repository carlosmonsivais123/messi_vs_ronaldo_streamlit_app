# Messi vs Ronaldo: Back End Data Extraction
## By: Carlos Monsivais

### Summary
Extracting data for Lionel Messi and Cristiano Ronaldo from [FBREF](https://fbref.com/en/) which is a website that tracks player match data and saves the values in tables. By requesting the data on these tables through CSS parsing we can create features and values that will be used in the web application to compare the two players by putting the data in a MYSQL table.

### Steps to Run
1. Create a virtual environment with the following command: `python3.10 -m venv env_name`
2. Activate the virtual environment with the following command: `source env_name/bin/activate`
3. Install the dependencies needed with the following command: `pip install -r requirements.txt`
4. Create a .env file in the location back_end/.env with the following variables:
```
###### MYSQL Database Login Information ######
MYSQL_USERNAME="db_username"
MYSQL_PASSWORD="db_password"
MYSQL_HOST="db_host"
MYSQL_PORT="db_port"
MYSQL_DB_NAME="db_name_var"
MYSQL_TABLE_NAME="output_table_name"

###### FBREF Player Names ######
PLAYER_1="Cristiano Ronaldo"
PLAYER_2="Lionel Messi"
```
5. Execute the main file with the following command: python3 main.py

### Execution Process
![back_end_data_flow](assets/images/back_end_data_flow.png)

### Output Table Data Schema
The final table output to MYSQL will have the following data columns.

| Column Name                       | Data Type                         | Description                       |
|-----------------------------------|-----------------------------------|-----------------------------------|
| day_of_the_week                   | varchar(50)                       | Day of the week match was played. (Sun, Mon, etc.)|
| competition                       | varchar(50)                       | Specific competition type for match. (Ligue1, MLS, etc.)|
| round                             | varchar(50)                       | Round of competition. (Matchweek 3, Group Stage, etc.)|
| venue                             | varchar(50)                       | Where the game was played. (Home, Away, etc.)|
| squad                             | varchar(50)                       | Team the player was playing for. (Barcelona, Juventus, etc.)|
| opponent                          | varchar(50)                       | Team the player was playing against. (Germany, Villareal, etc.)|
| game_started                      | varchar(50)                       | If the player started the match. (Y, N, etc.)|
| position                          | varchar(50)                       | Position player played. (FWD, AM, etc.)|
| result                            | varchar(50)                       | Result of match. (W, L, D, etc.)|
| penalty_shoot_out                 | varchar(50)                       | Did the match end in a penalty shoot out. (Y, N)|
| player_name                       | varchar(50)                       | Name of player. (Cristiano Ronaldo, Lionel Messi)|
| competition_type                  | varchar(50)                       | General competition type for the match. (Champions League, League, etc.)|
| last_data_extract                 | varchar(30)                       | Date the player data was last extracted. (2024-07-20 19:10:59, etc.)|
| game_played                       | varchar(15)                       | If the player had action in the match. (Played, Not Played)|
| minutes                           | int                               | Number of minutes the player played. (23, 33, etc.)|
| goals                             | int                               | Number of goals scored in the match. (1, 2, etc.)|
| assists                           | int                               | Number of assists in the match. (1, 2, etc.)|
| pens_made                         | int                               | Number of penalties scored in the match. (1, 2, etc.)|
| pens_attempted                    | int                               | Number of penalties attempted in the match. (1, 2, etc.)|
| shots_total                       | int                               | Number of shots on target in the match. (1, 2, etc.)|
| shots_on_target                   | int                               | Number of shots on target in the match. (1, 2, etc.)|
| cards_yellow                      | int                               | Number of yellow cards in the match. (0, 1)|
| cards_red                         | int                               | Number of red cards in the match. (0, 1)|
| fouls                             | int                               | Number of times player fouls in the match. (1, 2, etc.)|
| fouled                            | int                               | Number of times player got fouled in the match. (1, 2, etc.)|
| offsides                          | int                               | Number of offsides in the match. (1, 2, etc.)|
| crosses                           | int                               | Number of crosses in the match. (1, 2, etc.)|
| tackles_won                       | int                               | Number of tackles won in the match. (1, 2, etc.)|
| interceptions                     | int                               | Number of interceptions in the match. (1, 2, etc.)|
| own_goals                         | int                               | Number of own goals in the match. (1, 2, etc.)|
| touches                           | int                               | Number of touches on the ball in the match. (1, 2, etc.)|
| blocks                            | int                               | Number of blocks in the match. (1, 2, etc.)|
| shot_creating_actions             | int                               | Number of shot created actions in the match. (1, 2, etc.)|
| passes_completed                  | int                               | Number of passes completed in the match. (1, 2, etc.)|
| passes_attempted                  | int                               | Number of passes attempted in the match. (1, 2, etc.)|
| carries                           | int                               | Number of times the ball was dribbled in the match. (1, 2, etc.)|
| penalty_shoot_out_score_for       | int                               | Score for the player's team in the penalty shoot-out. (1, 2, etc.)|
| penalty_shoot_out_score_against   | int                               | Score for the opposition's team in the penalty shoot-out. (1, 2, etc.)|
| goal-creating_actions             | int                               | Number of goal creating actions in the match. (1, 2, etc.)|
| date                              | date                              | Date the match was played. (2021-02-27, 2021-03-21, etc.)|

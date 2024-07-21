from sqlalchemy import create_engine
from sqlalchemy.types import String, Date, Integer

class DatabaseComponents:
    '''
    Creates database components including connecting to a database and pushing data up to the database with a defined schema.

    @param mysql_username: String representing username for MYSQL table
    @param mysql_password: String representing password for MYSQL table
    @param mysql_host: String representing host for MYSQL table
    @param mysql_port: String representing port for MYSQL table
    @param mysql_db_name: String representing database name for MYSQL table
    '''
    def __init__(self, mysql_username, mysql_password, mysql_host, mysql_port, mysql_db_name):
        self.mysql_username=mysql_username
        self.mysql_password=mysql_password
        self.mysql_host=mysql_host
        self.mysql_port=mysql_port
        self.mysql_db_name=mysql_db_name


    def create_mysql_engine(self):
        '''
        Creates connection to database with specified credentials

        @return db_engine: sqlalchemy.engine type use to connect to the MYSQL database
        '''
        db_engine=create_engine(f"mysql+pymysql://{self.mysql_username}:" \
                                f"{self.mysql_password}@" \
                                    f"{self.mysql_host}:{self.mysql_port}/{self.mysql_db_name}")
        db_engine=db_engine.connect()

        return db_engine


    def execute_df_to_mysql_db(self, df, output_table_name):
        '''
        Executes pushing a dataframe with a specified schema to a MYSQL table.

        @param df: Dataframe with the concatenated player information
        @param output_table_name: String representing the name of the table on that will be created on the MYSQL server
        '''
        mysql_db_engine=self.create_mysql_engine()

        dtype_dict={'date': Date, 
                    'day_of_the_week': String(50), 
                    'competition': String(50), 
                    'round': String(50), 
                    'venue': String(50), 
                    'squad': String(50),
                    'opponent': String(50), 
                    'game_started': String(50), 
                    'position': String(50), 
                    'minutes': Integer(), 
                    'goals': Integer(), 
                    'assists': Integer(),
                    'pens_made': Integer(), 
                    'pens_attempted': Integer(), 
                    'shots_total': Integer(), 
                    'shots_on_target': Integer(),
                    'cards_yellow': Integer(), 
                    'cards_red': Integer(), 
                    'fouls': Integer(), 
                    'fouled': Integer(), 
                    'offsides': Integer(), 
                    'crosses': Integer(), 
                    'tackles_won': Integer(), 
                    'interceptions': Integer(), 
                    'own_goals': Integer(), 
                    'touches': Integer(), 
                    'tackle': Integer(), 
                    'blocks': Integer(), 
                    'shot_creating_actions': Integer(), 
                    'goal-creating_actions': Integer(), 
                    'passes_completed': Integer(), 
                    'passes_attempted': Integer(), 
                    'carries': Integer(), 
                    'result': String(50), 
                    'penalty_shoot_out': String(50), 
                    'penalty_shoot_out_score_for': Integer(), 
                    'penalty_shoot_out_score_against': Integer(),
                    'player_name': String(50),
                    'competition_type': String(50),
                    'game_played': String(15),
                    'last_data_extract': String(30)}

        df.to_sql(name=output_table_name, 
                  con=mysql_db_engine,
                  dtype=dtype_dict,
                  if_exists='replace', 
                  index=False)
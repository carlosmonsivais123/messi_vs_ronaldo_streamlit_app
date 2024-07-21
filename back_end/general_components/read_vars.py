import os
from dotenv import load_dotenv

load_dotenv(".env")

def get_variable(name):
    '''
    Extracts the variables needed for the .env file for use throughout the project.

    @param name: The name of the environment variable in the .env file

    @return val: The environment variable from the .env file
    '''
    val=os.environ.get(name)

    return val
# read JSON and parse into a python object 

import json 
from datetime import date 
import logging 

# Once we have imported logging, we can define a logger object and this will look as follows:
# -- This is the preferred way of handling logging in your scripts, and it is a best practice to use this
# -- module and not the Python print function.
# -- In my personal experience, I have found that I use print for troubleshooting and debugging, while
# -- I use logger in production code to output logs from Python functions.


logger = logging.getLogger(__name__)

def load_path():

    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        logger.info(f"Processing file: YT_data_{date.today()}")

        with open(file_path, "r", encoding="utf-8") as raw_data:
            data = json.load(raw_data)

            return data 
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise   


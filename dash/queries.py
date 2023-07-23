
import requests
import os 
import pandas as pd
import datetime
#import logging
from passlib.context import CryptContext
from requests.auth import HTTPBasicAuth
import json


############################################
#### DASH Data Queries #####################
# This class is query the api.##############
# to understand this class please consult :
# https://docs.google.com/spreadsheets/d/17P5CqASN3N-kALSAP4W5HMND7quHysstz8tTMghLJSA/edit?usp=sharing
############################################

###########################################
# Global variables ########################
###########################################

###########################################
## FIX ME FOR PROD WITH CONTAINER PORT
# url = "http://api:8000"
url = "http://0.0.0.0:8000"  #########
###########################################

"""
###########################################
# Set up the logger to log to a file
# Define the directory
# Define the directory
log_directory = "/Users/edouardphilippe/Documents/repo/NYT/NYT 2.2/dash/logs/dash/"
# Create the directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)
log_filename = "/app/logs/dash/dash_logs_{}.txt".format(datetime.date.today().isoformat())
logging.basicConfig(filename=log_filename, level=logging.INFO)
"""


###########################################
# Global functions ########################
###########################################

# apiCall # function #########################
def api_call(endpoint):

    """Return Dataframe from api call 
Args:
    - endpoint
Returns:
    - Dataframe
"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    username = 'dashboard'
    password = 'dst_NYT_dashboard'
    path = url + endpoint  
    print(path)
    try:
        response = requests.get(path, auth=HTTPBasicAuth(username, password))
        print(response)
        # Convert the response to JSON
        data = response.json()

        data_list = json.loads(data["data"])
        # Convert JSON to pandas DataFrame
        df = pd.DataFrame(data_list)
    
        # return DF
        return df

    except requests.exceptions.RequestException as e:
        print(e)
    # Log the error
       # logging.error("Request failed: " + str(e))


###########################################
# News ####################################
###########################################

# News - queries functions ################
###########################################

# News # bar plot 1 # Articles/Journalist #


def get_articles_per_journalist(section, time_scale):
    """Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    -  Dataframe 
"""
    endpoint=f"/news/top-journalists?section={section}&time_scale={time_scale}"
    dfRes= api_call(endpoint)
    return dfRes


# News # pie chart 2 # Articles/Section ###
def get_articles_per_section(time_scale):

    """Return sections list for dropdown/slider
Args:
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""  
    endpoint=f"/news/sections-proportions?time_scale={time_scale}"
    dfRes= api_call(endpoint)
    return dfRes
    


# News # bar plot 3 # Articles/Person ###
def get_articles_per_person(section, time_scale):
    """Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""
    endpoint=f"/news/top-persons?section={section}&time_scale={time_scale}"
    dfRes= api_call(endpoint)
    return dfRes


# News # line plot 4 # Articles/day ###
def get_articles_per_period(section, step):
    """Return sections list for dropdown/slider
Args:
    - Section - news section
    - step - scope of the search
Returns:
    - Dataframe 
"""
    endpoint=f"/news/articles-count?section={section}&step={step}"
    print(endpoint)
    dfRes= api_call(endpoint)
    return dfRes


# News # bar plot 5 # descriptions/article ##
def get_top_topics(section, time_scale):
    """Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""
    endpoint=f"/news/top-topics?section={section}&time_scale={time_scale}"
    print(endpoint)
    dfRes= api_call(endpoint)
    print(dfRes.head())
    return dfRes
""" CODE SPACE ###########################"""


###########################################
# Books ###################################
###########################################

# Books - queries functions ################
###########################################

# Books # bar plot 1 # Top NYT Bestsellers #
def get_top_topics(size):
    """Return sections list for dropdown/slider
Args:
    - Size 
Returns:
    - Dataframe 
"""
    endpoint=f"/books/top-writers?size={size}"
    print(endpoint)
    dfRes= api_call(endpoint)
    print(dfRes.head())
    return dfRes



# Books # bar plot 2 # books/ Bestseller list#
"""Return sections list for dropdown/slider
Args:
    - Size 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# Books # bar plot 3 # Articles/Person ###
"""Return sections list for dropdown/slider
Args:
    - list - (books NYT list)
    - Size 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# Books # bar plot 4 # publishers/bestsellers ##
"""Return sections list for dropdown/slider
Args:
    - Size 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

###########################################
# Movies ##################################
###########################################

# Movies - queries functions ################
###########################################

# Movies # bar plot 1 # Reviews / year ####
def get_reviews_per_year():
    """Return sections list for dropdown/slider
Args:
    - None
Returns:
    - Dataframe 
"""
    endpoint="/movies/count-per-year"
    print(endpoint)
    dfRes= api_call(endpoint)
    return dfRes





# Movies  # bar plot 2 # Top 5 most prolific Journalist#
"""Return sections list for dropdown/slider
Args:
    - year 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# Movies # bar plot 3 # top 5  MPAA Ratings of all time ###
"""Return sections list for dropdown/slider
Args:
    - None 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""
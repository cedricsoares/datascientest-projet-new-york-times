
import requests
import pandas as pd

############################################
#### DASH Data Queries #####################
# This class is query the api.##############
# to understand this class please consult :
# https://docs.google.com/spreadsheets/d/17P5CqASN3N-kALSAP4W5HMND7quHysstz8tTMghLJSA/edit?usp=sharing
############################################

###########################################
# Global functions ########################
###########################################

url = "https://localhost:"

# apiCall # function #########################
def apiCall(endpoint):

    """Return Dataframe from api call 
Args:
    - endpoint
Returns:
    - Dataframe
"""
    username = 'dashboard'
    password = 'dst_NYT_dashboard'

    path = url + endpoint
    print(path)
    response = requests.get('http://your-api-url.com', params={'username': username, 'password': password})
    # Convert the response to JSON
    data = response.json()
    # Convert JSON to pandas DataFrame
    df = pd.DataFrame(data)
    # return DF
    return df


###########################################
# News ####################################
###########################################


# News - section necessary lists ##########
###########################################

# News - sections #########################
"""Return sections list for dropdown/slider
Args:
     none
Returns:
    List of Strings
"""
""" CODE SPACE ###########################"""

# News - time-scale #######################
"""Return time scale list for dropdown/slider
Args:
     none
Returns:
    List of Strings    #### TO DOUBLE CHECK
"""
""" CODE SPACE ###########################"""

# News - size #############################
"""Return sections list for dropdown/slider
Args:
     none
Returns:
    List of Strings  #### TO DOUBLE CHECK
"""
""" CODE SPACE ###########################"""


# News - queries functions ################
###########################################

# News # bar plot 1 # Articles/Journalist #
"""Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    -  Dataframe 
"""

""" CODE SPACE ###########################"""

# News # pie chart 2 # Articles/Section ###
"""Return sections list for dropdown/slider
Args:
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# News # bar plot 3 # Articles/Person ###
"""Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# News # line plot 4 # Articles/day ###
"""Return sections list for dropdown/slider
Args:
    - Section - news section
    - step - scope of the search
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

# News # bar plot 5 # descriptions/article ##
"""Return sections list for dropdown/slider
Args:
    - Section - news section
    - timeScale - scope of the search
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""


###########################################
# Books ###################################
###########################################

# Books - queries functions ################
###########################################

# Books # bar plot 1 # Top NYT Bestsellers #
"""Return sections list for dropdown/slider
Args:
    - Size 
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

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
"""Return sections list for dropdown/slider
Args:
    - None
Returns:
    - Dataframe 
"""

""" CODE SPACE ###########################"""

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
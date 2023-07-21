
############################################
#### DASH DasboardLists ####################
# This class is to prepare data consumption#
# as needed in the dash board.##############
# to understand this class please consult :
# https://docs.google.com/spreadsheets/d/17P5CqASN3N-kALSAP4W5HMND7quHysstz8tTMghLJSA/edit?usp=sharing
############################################


###########################################
# News ####################################
###########################################

def getSectionList():
    sections=['World', 
              'U.S.', 
              'Opinion', 
              'Business', 
              'Arts', 
              'Sports',
              'New York', 
              'En español', 
              'Books', 
              'Style', 
              'Briefing',
              'Movies', 
              'Climate', 
              'Science', 
              'Technology']   
    return sections


def getTimeScaleList():
    timeScale=['yesterday',
               'week_ago', 
               'month_ago']
    return timeScale


def getStepsList():
    steps=['day',
           'week',
           'month',
           'quarter',
           'year']
    return steps


###########################################
# Books ###################################
###########################################

def getSizesList():
    sizes=[5,10,15,20]
    return sizes

def getBookLists():
    bookLists= [
    "Hardcover Fiction", 
    "Hardcover Nonfiction", 
    "Advice How-To and Miscellaneous", 
    "Young Adult Hardcover", 
    "Picture Books", 
    "Childrens Middle Grade Hardcover", 
    "Manga", 
    "Series Books", 
    "Hardcover Graphic Books", 
    "Sports", 
    "Business Books", 
    "Science", 
    "Food and Fitness", 
    "Hardcover Advice",  
    "Games and Activities", 
    "Fashion Manners and Customs", 
    "Culture", 
    "Animals", 
    "Travel", 
    "Celebrities", 
    "Religion Spirituality and Faith", 
    "Espionage", 
    "Health", 
    "Crime and Punishment", 
    "Expeditions Disasters and Adventures", 
    "Hardcover Political Books",  
    "Family", 
    "Education", 
    "Humor", 
    "Race and Civil Rights", 
    "Relationships", 
    "Indigenous Americans"
    ]

    return bookLists

###########################################
# Movies ##################################
###########################################

def getYearsList():
    yearsList=list(range(1936, 2024))
    return yearsList
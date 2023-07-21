
############################################
#### DASH DasboardLists ####################
# This class is to prepare data consumption#
# as needed in the dash board.##############
# to understand this class please consult :
# https://docs.google.com/spreadsheets/d/17P5CqASN3N-kALSAP4W5HMND7quHysstz8tTMghLJSA/edit?usp=sharing
############################################

class DashboardLists:
###########################################
# News ####################################
###########################################
    @classmethod
    def get_section_list(cls):
         return ['World', 
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
        
    @classmethod
    def get_time_scale_list(cls):
        return ['yesterday',
                'week_ago', 
                'month_ago']
        

    @classmethod
    def get_steps_list(cls):
        return ['day',
            'week',
            'month',
            'quarter',
            'year']
        
    ###########################################
    # Books ###################################
    ###########################################

    @classmethod
    def get_sizes_list(cls):
        return [5,10,15,20]

    @classmethod
    def get_books_lists(cls):
        return [
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

    ###########################################
    # Movies ##################################
    ###########################################

    @classmethod
    def get_years_list(cls):
        return list(range(1936, 2024))
     
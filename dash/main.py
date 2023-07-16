import dash
from dash import dcc,html,dash_table
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input
import dash_bootstrap_components as dbc
import transform



############################################
#### DASH app ##############################
# this app generates plotly graph and disp-#
# lay them on html pages. Our app is compos#
# ed of 4 pages, landing page, news, books,#
# and movies and available on port 0.0.0.0 #
############################################


###########################################
# Landing pages ###########################
###########################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)


###########################################
# News ####################################
###########################################

###########################################
# Books ###################################
###########################################

###########################################
# Movies ##################################
###########################################



if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")


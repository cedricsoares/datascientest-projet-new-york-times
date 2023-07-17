import dash
from dash import dcc,html,dash_table
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input
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
external_stylesheets = ['styles.css','https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'page-content')
])

landing_page = html.Div(className="landing_page", children=[
    html.Div(children=[
        html.H1("Welcome to NYT analysis App"),
        html.H4("Creators: Cedric Soares, Anna Temerko, Matthieu Lefebrve, Edouard Philippe"),
        html.Div(className="button_container", children=[
            html.Button(children=dcc.Link("News", href='/news')),
            html.Button(children=dcc.Link("Books", href='/books')),
            html.Button(children=dcc.Link("Movies", href='/movies'))
        ])
    ])
])


###########################################
# News ####################################
###########################################

news_page = html.Div([

  html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')), style={'textAlign': 'center'}),
], style = {'background-color' : 'beige','minHeight': '100vh'})


# News callback functions #################
###########################################


###########################################
# Books ###################################
###########################################

books_page = html.Div([

  html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')), style={'textAlign': 'center'}),
], style = {'background-color' : 'beige','minHeight': '100vh'})

#Books callback functions #################
###########################################

###########################################
# Movies ##################################
###########################################

movies_page = html.Div([

  html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')), style={'textAlign': 'center'}),
], style = {'background-color' : 'beige','minHeight': '100vh'})


# Movies callback functions ###############
###########################################



###########################################
# app methods #############################
###########################################




@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return landing_page;   
    elif pathname == '/news':
        return news_page
    elif pathname == '/books':
        return books_page
    elif pathname == '/movies':
        return movies_page
    else:
        return '404 Page not found'



if __name__ == '__main__':
     app.run_server(debug=True, host="0.0.0.0", dev_tools_hot_reload=True)


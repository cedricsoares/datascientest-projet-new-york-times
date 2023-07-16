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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div(style={'background-color': 'darkgrey', 'height':'100vh', 'color': 'lightblue',
                            'display': 'flex', 'flex-direction':'column','align-items': 'center', 
                            'justify-content': 'center'},children=[
    html.H1("Welcome to NYT analysis App"),
    html.H4("Creators: Cedric Soares, Anna Temerko, Matthieu Lefebrve, Edouard Philippe"),
    html.Button("News", id='btn-news', n_clicks=0, style={'margin-bottom': '10px'}),
    html.Button("Books", id='btn-books', n_clicks=0, style={'margin-bottom': '10px'}),
    html.Button("Movies", id='btn-movies', n_clicks=0)
])

@app.callback(
    dash.dependencies.Output('url', 'pathname'),
    [dash.dependencies.Input('btn-news', 'n_clicks'),
     dash.dependencies.Input('btn-books', 'n_clicks'),
     dash.dependencies.Input('btn-movies', 'n_clicks')])
def navigate_to_page(news_clicks, books_clicks, movies_clicks):
    if news_clicks > 0:
        return '/news'
    elif books_clicks > 0:
        return '/books'
    elif movies_clicks > 0:
        return '/movies'
    else:
        return '/'

###########################################
# News ####################################
###########################################

layout_news = html.Div([

  html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')), style={'textAlign': 'center'}),
], style = {'background-color' : 'beige','minHeight': '100vh'})


# News callback functions #################
###########################################


###########################################
# Books ###################################
###########################################

###########################################
# Movies ##################################
###########################################


###########################################
# app methods #############################
###########################################


app.validation_layout = html.Div([
    html.Div([dcc.Location(id='url', refresh=False)]),
    html.Div(id='page-content')
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/news':
        return news_page
    elif pathname == '/books':
        return books_page
    elif pathname == '/movies':
        return movies_page
    else:
        return app.layout



if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")


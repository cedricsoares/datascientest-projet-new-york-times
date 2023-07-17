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


######FIX ME #############################
######FAKE DATA ##########################
# Data for the charts
data = [
    {"section": "A", "time_scale": "2020", "step": 1},
    {"section": "B", "time_scale": "2020", "step": 2},
    {"section": "C", "time_scale": "2020", "step": 3},
    {"section": "D", "time_scale": "2020", "step": 4},
    {"section": "E", "time_scale": "2020", "step": 5}
]

data2 = {
    "section": ["A", "B", "C", "D", "E"],
    "time_scale": [10, 15, 8, 12, 6]
}

df = pd.DataFrame(data2)
######FAKE DATA ##########################


news_page = html.Div(children=[
    html.H1("NEWS SECTION"),
    html.Div([

        html.Div([
             
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-1',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='bar-plot-1', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Bar Plot 1")),           
            # slider
            dcc.Slider(className='slider',id='news-page-slider-plot-1',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),
            
       # Div pie chart
        html.Div([
            # dropdown
            dcc.Slider(id='news-page-slider-pie-1', className='slider',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                ),
            #bar plot 
            dcc.Graph(id='pie-chart', className="pie-chart-style-1", figure=px.pie(df, values="time_scale", title="pie chart 1")),
            
        ], className="single_plot_ctnr"),
            

       # Div chart 3
       html.Div([
        # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-2',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Bar Plot 2")),           
            # slider
            dcc.Slider(className='slider',id='news-page-slider-plot-2',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),

    ],className= "plots_ctnr"),





  html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')),className="button_container"),

], className= "pages")


# News callback functions #################
###########################################

# bar plot 1 ##############################
@app.callback(
    Output('bar-plot-1', 'figure'),
    [Input('news-page-dropdow-plot-1', 'newsSection'),
     Input('news-page-slider-plot-1', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale):
        return px.bar(df, x="section", y="time_scale", title="Bar Plot 1")
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....
        

# Pie Chart ##############################
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('news-page-slider-pie-1', 'timeScale')])
def update_news_pie_chart(timescale):
        return px.pie(df, values="time_scale", title="pie chart 1")
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# bar plot 2 ##############################
@app.callback(
    Output('bar-plot-2', 'figure'),
    [Input('news-page-dropdow-plot-2', 'newsSection'),
     Input('news-page-slider-plot-2', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale):
        return px.bar(df, x="section", y="time_scale", title="Bar Plot 1")
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....


# bar plot 3 ##############################

# bar plot 4 ##############################



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


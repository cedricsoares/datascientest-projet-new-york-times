import dash
from dash import dcc,html,dash_table
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input
import transform
import queries


############################################
#### DASH app ##############################
# this app generates plotly graph and disp-#
# lay them on html pages. Our app is compos#
# ed of 4 pages, landing page, news, books,#
# and movies and available on port 0.0.0.0 #
############################################

colors = {
    'background': '#474747',
    'text': '#26CAE9'
}



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
    
    html.Div([html.H1("NEWS SECTION"),
              html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')),className="button_container")]
              , className='title_ctnr'),

    html.Div([
        html.Div([
             
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-1',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='bar-plot-1', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="articles / journalist")),           
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
            #bar plot 
            dcc.Graph(id='pie-chart', className="pie-chart-style-1", figure=px.pie(df, values="time_scale", title="article /section")),
            # slider
            dcc.Slider(id='news-page-slider-pie-1', className='slider',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                ),
            
        ], className="single_plot_ctnr"),
            

       # Div chart 3
       html.Div([
        # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-2',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="articles / person")),           
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


  html.Div([
    # Div chart 4
       html.Div([
        # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-4',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='line-plot-4', className="bar-plots-1row", figure=px.line(df, x="section", y="time_scale", title="articles / day")),           
            # slider
            dcc.Slider(className='slider',id='news-page-slider-plot-4',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),
   

     # Div chart 5


       html.Div([
        # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdow-plot-5',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'news-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='bar-plot-5', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="descriptions / article")),           
            # slider
            dcc.Slider(className='slider',id='news-page-slider-plot-5',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),

],className= "plots_ctnr_2"),
], className= "pages")


# News callback functions #################
###########################################

# 1 # bar plot 1 ##############################
@app.callback(
    Output('bar-plot-1', 'figure'),
    [Input('news-page-dropdow-plot-1', 'newsSection'),
     Input('news-page-slider-plot-1', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale):
        fig = px.bar(df, x="section", y="time_scale", title="articles / journalist")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
     
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....
        

# 2 # Pie Chart ##############################
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('news-page-slider-pie-1', 'timeScale')])
def update_news_pie_chart(timescale):  
        fig= px.pie(df, values="time_scale", title="article /section")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig 
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# 3 # bar plot 2 ##############################
@app.callback(
    Output('bar-plot-2', 'figure'),
    [Input('news-page-dropdow-plot-2', 'newsSection'),
     Input('news-page-slider-plot-2', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale): 
        fig = px.bar(df, x="section", y="time_scale", title="articles / person")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
     
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# 4 # line plot 1 ##############################

@app.callback(
    Output('line-plot-4', 'figure'),
    [Input('news-page-dropdow-plot-4', 'newsSection'),
     Input('news-page-slider-plot-4', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale): 
        fig = px.line(df, x="section", y="time_scale", title="articles / day")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....


# 5 # bar plot 3 ##############################
@app.callback(
    Output('bar-plot-5', 'figure'),
    [Input('news-page-dropdow-plot-5', 'newsSection'),
     Input('news-page-slider-plot-5', 'timeScale')])
def update_news_bar_plot1(newsSection, timescale): 
        fig = px.bar(df, x="section", y="time_scale", title="descriptions / article")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....


###########################################
# Books ###################################
###########################################

books_page = html.Div([
    html.Div([html.H1("BOOKS SECTION"),
              html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')),className="button_container")]
              , className='title_ctnr'),

  html.Div([
     # Div chart 1
       html.Div([

            #bar plot 
            dcc.Graph(id='books-bar-plot-1', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top NYT Bestsellers")),           
            # slider
            dcc.Slider(className='slider',id='books-page-slider-plot-1',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),
   

     # Div chart 2
       html.Div([

            #bar plot 
            dcc.Graph(id='books-bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Books / Bestsellers list")),           
            # slider
            dcc.Slider(className='slider',id='books-page-slider-plot-2',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),

    ],className= "plots_ctnr_2"),

            
    html.Div([
        # Div chart 3
        html.Div([
        # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdow-plot-3',
                    options= ['world', 'us','sport'],#######FIX ME ############################# [{'label':i, 'value':i} for i in rookies],  
                    value= 'books-section'), className='dropDown'),
            #bar plot 
            dcc.Graph(id='books-bar-plot-3', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top writers / list")),           
            # slider
            dcc.Slider(className='slider',id='books-page-slider-plot-3',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),

     # Div chart 4
       html.Div([
            #bar plot 
            dcc.Graph(id='books-bar-plot-4', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title=" Publishers / bestsellers")),           
            # slider
            dcc.Slider(className='slider',id='books-page-slider-plot-4',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),

    ],className= "plots_ctnr_2"),
], className= "pages")


#Books callback functions #################
###########################################

# bar plot 1 ##############################
@app.callback(
    Output('books-bar-plot-1', 'figure'),
    [Input('books-page-slider-plot-1', 'size')])
def update_books_bar_plot1(size): 
        fig = px.bar(df, x="section", y="time_scale", title="Top NYT Bestsellers")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# bar plot 2 ##############################
@app.callback(
    Output('books-bar-plot-2', 'figure'),
    [Input('books-page-slider-plot-2', 'size')])
def update_books_bar_plot2(size): 
        fig = px.bar(df, x="section", y="time_scale", title="Books / Bestsellers list")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....


# bar plot 3 ##############################
@app.callback(
    Output('books-bar-plot-3', 'figure'),
    [Input('books-page-dropdow-plot-3', 'list'),
     Input('books-page-slider-plot-3', 'size')])
def update_books_bar_plot3(list, size): 
        fig = px.bar(df, x="section", y="time_scale", title="Top writers / list")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# bar plot 4 ##############################
@app.callback(
    Output('books-bar-plot-4', 'figure'),
     [Input('books-page-slider-plot-4', 'size')])
def update_books_bar_plot4(size): 
        fig = px.bar(df, x="section", y="time_scale", title="Publisher / list")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig



###########################################
# Movies ##################################
###########################################

movies_page = html.Div([

    html.Div([html.H1("MOVIES SECTION"),
              html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')),className="button_container")]
              , className='title_ctnr'),

html.Div([
        html.Div([
        
            #bar plot 
            dcc.Graph(id='movies-bar-plot-1', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="reviews / year")),                    
        ], className="single_plot_ctnr"),
            
       # Div Bar chart
        html.Div([          
            #bar plot 
            dcc.Graph(id='movies-bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top 5 most prolific journalists")),           
            # slider
            dcc.Slider(className='slider',id='movies-page-slider-plot-2',
                min=0,
                max=5,
                ######FIX ME #############################
                # code ex: marks={i: position for i, position in enumerate(positions_list)},
                value=3,    
                )        
        ], className="single_plot_ctnr"),            

        # Div chart 3
        html.Div([
        
            #bar plot 
            dcc.Graph(id='movies-bar-plot-3', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top 5 MPAA ratings catregories all time")),           
        ], className="single_plot_ctnr"),
    ],className= "plots_ctnr"),


], className= "pages")

# Movies callback functions ###############
###########################################

# bar plot 1 ##############################
@app.callback(
    Output('movies-bar-plot-1', 'figure'),
    Input('url', 'pathname'))
def update_movies_bar_plot1(path): 
        fig = px.bar(df, x="section", y="time_scale", title="reviews / year")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# bar plot 2 ##############################
@app.callback(
    Output('movies-bar-plot-2', 'figure'),
    [Input('movies-page-slider-plot-2', 'size')])
def update_movies_bar_plot2(size): 
        fig = px.bar(df, x="section", y="time_scale", title="Top 5 most prolific journalists")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....

# bar plot 3 ##############################
@app.callback(
    Output('movies-bar-plot-3', 'figure'),
    Input('url', 'pathname'))
def update_movies_bar_plot3(size): 
        fig = px.bar(df, x="section", y="time_scale", title="Top 5 MPAA ratings of all time")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....



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


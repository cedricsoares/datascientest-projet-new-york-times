import dash
from dash import dcc,html,dash_table
import pandas as pd
import plotly.express as px 
from dash.dependencies import Output,Input
import dashboardLists
import queries


############################################
#### DASH app ##############################
# this app generates plotly graph and disp-#
# lay them on html pages. Our app is compos#
# ed of 4 pages, landing page, news, books,#
# and movies and available on port 0.0.0.0 #
############################################


###########################################
# app necessary data and functions ########
###########################################

colors = {
    'background': '#474747',
    'text': '#26CAE9'
}


## acquire lists for dropdonw and sliders
###########################################

sectionsList = dashboardLists.DashboardLists.get_section_list() 
timeScaleList = dashboardLists.DashboardLists.get_time_scale_list()
stepsList = dashboardLists.DashboardLists.get_steps_list()
sizesList = dashboardLists.DashboardLists.get_sizes_list()
booksLists = dashboardLists.DashboardLists.get_books_lists()
yearsList = dashboardLists.DashboardLists.get_years_list()

######FAKE DATA ##########################

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

def fake_graph(title):
    """Return a fake bar plot 
Args:
    - title
Returns:
    - bar plot
"""
    fig = px.bar(df, x="section", y="time_scale", title=title)
    fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
 
    return fig


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


news_page = html.Div(children=[
    
    html.Div([html.H1("NEWS SECTION"),
              html.Div(html.Button(dcc.Link('Revenir à la page de garde', href='/')),className="button_container")]
              , className='title_ctnr'),

    html.Div([
        html.Div([          
            #bar plot 
            dcc.Graph(id='bar-plot-1', className="bar-plots-1row"),
                                         
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-sections-plot-1',
                    options= [{'label':i, 'value':i} for i in sectionsList],  
                    placeholder="Select section...",
                    value= sectionsList[0] # Set default value
                    ), className='dropDown'),
            
             # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-time_scale-plot-1',
                    options= [{'label':i, 'value':i} for i in timeScaleList ],  
                    placeholder="Select time scale...",
                    value= timeScaleList[0] # Set default value
                    ), className='dropDown'),

        
        ], className="single_plot_ctnr"),
            
       # Div pie chart
        html.Div([
            #bar plot 
            dcc.Graph(id='pie-chart', className="pie-chart-style-1", figure=px.pie(df, values="time_scale", title="article /section")),
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-time_scale-plot-2',
                    options= [{'label':i, 'value':i} for i in timeScaleList ],  
                    placeholder="Select time scale...",
                    value= timeScaleList[0] # Set default value
                    ), className='dropDown'),
            
        ], className="single_plot_ctnr"),
            

       # Div chart 3
       html.Div([
               
            #bar plot 
            dcc.Graph(id='bar-plot-3', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="articles / person")),           
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-sections-plot-3',
                    options= [{'label':i, 'value':i} for i in sectionsList],  
                    placeholder="Select section...",
                    value= sectionsList[0] # Set default value
                    ), className='dropDown'),
            
             # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-time_scale-plot-3',
                    options= [{'label':i, 'value':i} for i in timeScaleList ],  
                    placeholder="Select time scale...",
                    value= timeScaleList[0] # Set default value

                    ), className='dropDown'),     
        ], className="single_plot_ctnr"),
    ],className= "plots_ctnr"),


  html.Div([
    # Div chart 4
       html.Div([

            #line plot 
            dcc.Graph(id='line-plot-4', className="bar-plots-1row", figure=px.line(df, x="section", y="time_scale", title="articles / day")),           
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-sections-plot-4',
                    options= [{'label':i, 'value':i} for i in sectionsList],  
                    placeholder="Select section...",
                    value= sectionsList[0] # Set default value
                    ), className='dropDown'),
            
             # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-steps-plot-4',
                    options= [{'label':i, 'value':i} for i in stepsList ],  
                    placeholder="Select  step...",
                    value= stepsList[0] # Set default value
            ), className='dropDown')

        ], className="single_plot_ctnr"),
   

     # Div chart 5


       html.Div([
             
            #bar plot 
            dcc.Graph(id='bar-plot-5', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="descriptions / article")),           
        
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-sections-plot-5',
                    options= [{'label':i, 'value':i} for i in sectionsList],  
                    placeholder="Select section...",
                    value= sectionsList[0] # Set default value
                    ), className='dropDown'),
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'news-page-dropdown-time_scale-plot-5',
                    options= [{'label':i, 'value':i} for i in timeScaleList ],  
                    placeholder="Select time scale...",
                    value= timeScaleList[0] # Set default value
                    ), className='dropDown'),

        ], className="single_plot_ctnr"),

],className= "plots_ctnr_2"),
], className= "pages")


# News callback functions #################
###########################################

# 1 # bar plot 1 ##############################
@app.callback(
    Output('bar-plot-1', 'figure'),
    [Input('news-page-dropdown-sections-plot-1', 'value'),
     Input('news-page-dropdown-time_scale-plot-1', 'value')])
def update_news_bar_plot1(newsSection, timescale):   

    if newsSection is None or newsSection not in sectionsList and timescale is None or timescale not in timeScaleList:   
        # return a fake graph in case there is a bad connection
        fake_graph('articles / journalist')
        
    else:
        # query API to get dataframe
        queriedDf = queries.get_articles_per_journalist(newsSection,timescale)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="articles / journalist",labels={"key": "journalist", "doc_count": "articles"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig
        

# 2 # Pie Chart ##############################
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('news-page-dropdown-time_scale-plot-2', 'value')])
def update_news_pie_chart(timescale):  
  
    if timescale is None or timescale not in timeScaleList: 
        # return a fake graph in case there is a bad connection
        fake_graph('articles / section')
    
    else: 
        # query API to get dataframe
        queriedDf = queries.get_articles_per_section(timescale)
        queriedDf.head()
        fig = px.pie(queriedDf, values='doc_count', names='key', title="article /section")
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig
        
        

# 3 # bar plot 2 ##############################
@app.callback(
    Output('bar-plot-3', 'figure'),
    [Input('news-page-dropdown-sections-plot-3', 'value'),
     Input('news-page-dropdown-time_scale-plot-3', 'value')])
def update_news_bar_plot1(newsSection, timescale): 

    # return a fake dataframe
    if newsSection is None or newsSection not in sectionsList and timescale is None or timescale not in timeScaleList: 
        # return a fake graph in case there is a bad connection
        fake_graph('articles / person')

    else:
        # query API to get dataframe
        queriedDf = queries.get_articles_per_person(newsSection,timescale)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="articles / person",labels={"key": "person", "doc_count": "articles"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig

# 4 # line plot 1 ##############################

@app.callback(
    Output('line-plot-4', 'figure'),
    [Input('news-page-dropdown-sections-plot-4', 'value'),
     Input('news-page-dropdown-steps-plot-4', 'value')])
def update_news_bar_plot1(newsSection, step): 
       

    # return a fake dataframe
    if newsSection is None or newsSection not in sectionsList and step is None or step not in stepsList: 
        # return a fake graph in case there is a bad connection
        fake_graph('articles / period')
        
    else:
        # query API to get dataframe
        queriedDf = queries.get_articles_per_period(newsSection,step)
        queriedDf.head()
        fig = px.line(queriedDf, x="key_as_string", y="doc_count", title="articles / period",labels={"key_as_string": "steps", "doc_count": "articles"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])

        return fig
        ######FIX ME #############################
        #### FIX ME INCLUDE QUERY LOGIC ....


# 5 # bar plot 3 ##############################
@app.callback(
    Output('bar-plot-5', 'figure'),
    [Input('news-page-dropdown-sections-plot-5', 'value'),
     Input('news-page-dropdown-time_scale-plot-5', 'value')])
def update_news_bar_plot1(newsSection, timescale): 
     # return a fake dataframe
    if newsSection is None or newsSection not in sectionsList and timescale is None or timescale not in timeScaleList: 
        # return a fake graph in case there is a bad connection
        fake_graph('top topics')

    else:
        # query API to get dataframe
        queriedDf = queries.get_top_topics(newsSection,timescale)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="top topics",labels={"key": "person", "doc_count": "articles"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig


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
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdown-sizes-plot-1',
                    options= [{'label':i, 'value':i} for i in sizesList],  
                    placeholder="Select step...",
                    value= sizesList[3] # Set default value
                    ), className='dropDown'),

        ], className="single_plot_ctnr"),
   

     # Div chart 2
       html.Div([

            #bar plot 
            dcc.Graph(id='books-bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Books / Bestsellers list")),           
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdown-sizes-plot-2',
                    options= [{'label':i, 'value':i} for i in sizesList],  
                    placeholder="Select step...",
                    value= sizesList[3] # Set default value
                    ), className='dropDown'),  

        ], className="single_plot_ctnr"),

    ],className= "plots_ctnr_2"),

            
    html.Div([
        # Div chart 3
        html.Div([
              
            #bar plot 
            dcc.Graph(id='books-bar-plot-3', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top writers / list")),           
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdown-lists-plot-3',
                    options= [{'label':i, 'value':i} for i in booksLists],  
                    placeholder="Select a list...",
                    value= booksLists[0] # Set default value
                    ), className='dropDown'),

            # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdown-sizes-plot-3',
                    options= [{'label':i, 'value':i} for i in sizesList],  
                    placeholder="Select step...",
                    value= sizesList[3] # Set default value
                    ), className='dropDown'),        

        ], className="single_plot_ctnr"),

     # Div chart 4
       html.Div([
            #bar plot 
            dcc.Graph(id='books-bar-plot-4', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title=" Publishers / bestsellers")),           
            
            # dropdown
            html.Div(dcc.Dropdown(id = 'books-page-dropdown-sizes-plot-4',
                    options= [{'label':i, 'value':i} for i in sizesList],  
                    placeholder="Select step...",
                    value= sizesList[3] # Set default value
                    ), className='dropDown'), 

        ], className="single_plot_ctnr"),

    ],className= "plots_ctnr_2"),
], className= "pages")


#Books callback functions #################
###########################################

# bar plot 1 ##############################
@app.callback(
    Output('books-bar-plot-1', 'figure'),
    [Input('books-page-dropdown-sizes-plot-1', 'value')])
def update_books_bar_plot1(size): 

    if size is None or size not in sizesList: 
        # return a fake graph in case there is a bad connection
        fake_graph('Top writers')
        
    else:
        # query API to get dataframe
        queriedDf = queries.get_top_writers(size)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="top topics",labels={"key": "person", "doc_count": "books"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig




# bar plot 2 ##############################
@app.callback(
    Output('books-bar-plot-2', 'figure'),
   [Input('books-page-dropdown-sizes-plot-2', 'value')])
def update_books_bar_plot2(size): 
    
    if size is None or size not in sizesList: 
        # return a fake graph in case there is a bad connection
        fake_graph('Count by book lists')
        
    else:
        # query API to get dataframe
        queriedDf = queries.get_count_by_lists(size)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="Count by book lists",labels={"key": "person", "doc_count": "books"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig



# bar plot 3 ##############################
@app.callback(
    Output('books-bar-plot-3', 'figure'),
    [Input('books-page-dropdown-lists-plot-3', 'value'),
     Input('books-page-dropdown-sizes-plot-3', 'value')])
def update_books_bar_plot3(list, size): 
    # return a fake dataframe
    if list is None or list not in booksLists and size is None or size not in sizesList: 
        # return a fake graph in case there is a bad connection
        fake_graph('top writers by book lists')

    else:
        # query API to get dataframe
        queriedDf = queries.get_top_writers_by_lists(list,size)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="top writers by book lists",labels={"key": "person", "doc_count": "books"})
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
        return fig

# bar plot 4 ##############################
@app.callback(
    Output('books-bar-plot-4', 'figure'),
    [Input('books-page-dropdown-sizes-plot-4', 'value')])
def update_books_bar_plot4(size): 
    if size is None or size not in sizesList: 
        # return a fake graph in case there is a bad connection
        fake_graph('top publishers')
        
    else:
        # query API to get dataframe
        queriedDf = queries.get_top_publishers(size)
        queriedDf.head()
        fig = px.bar(queriedDf, x="key", y="doc_count", title="top publishers",labels={"key": "person", "doc_count": "books"})
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
            dcc.Graph(id='movies-bar-plot-1', className="bar-plots-1row"),                    
        ], className="single_plot_ctnr"),
            
       # Div Bar chart
        html.Div([          
            #bar plot 
            dcc.Graph(id='movies-bar-plot-2', className="bar-plots-1row", figure=px.bar(df, x="section", y="time_scale", title="Top 5 most prolific journalists")),           
           
            #slider output
            html.Div(id='slider-output-container', className= 'sliderOutput'), 
            # slider
            dcc.Slider(className='slider',id='movies-page-slider-plot-2',
                min=min(yearsList),
                max=max(yearsList),
                marks= {year: str(year) for year in [1936, 1950, 1970, 1990, 2010, 2023]},
                value=1990,
                step=1    
                ), 
                       
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
        
        # query API to get dataframe
    queriedDf = queries.get_reviews_per_year()
    queriedDf.head()
    fig = px.bar(queriedDf, x="section", y="time_scale", title="articles / journalist")
    fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        
    return fig

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

@app.callback(
    Output('slider-output-container', 'children'),
    Input('movies-page-slider-plot-2', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)


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


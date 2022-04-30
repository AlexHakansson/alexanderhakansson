from dash import Dash, dcc, html,dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import neo4j_handler as nj
import mongo_handler as mh
import SQL_handler as sh


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
print("making neo4j obj")

db_info = pd.read_csv("db_info.txt",index_col=0)
nb = nj.neob(db_info.loc["neo4j_uri","value"],db_info.loc["neo4j_user","value"],db_info.loc["neo4j_password","value"])  


unv_neo_init = "University of illinois at Urbana Champaign"
kw_neo_init = "data mining"

df = nj.univ_keyword_pub_comp(nb.session,unv_neo_init,kw_neo_init)
df = df.head(10)
df.columns = ["Name","Pub_Count"]
"""
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
"""
print("making mongo ob")

mb = mh.mongoob(db_info.loc["mongo_db_host","value"],db_info.loc["mongo_db_port","value"])

print("making sql ob")
sql_ob = sh.sql_ob(db_info.loc["sql_user","value"],db_info.loc["sql_password","value"],db_info.loc["sql_host","value"])

print("making neo fig")
fig = px.bar(df, x="Name", y="Pub_Count", barmode="group",
            labels={"Name": "Faculty Name",
                     "Pub_Count": "Number of publications"},
            title = "University Faculty Comparison" )
 
key_init = "data mining"    
df_allk = sql_ob.select_top_faculty_by_keyword(key_init) 

print("making sql fig")
fig2 = px.bar(df_allk, x="name", y="score", barmode="group",
            labels={"name": "Faculty Name",
                     "score": "keyworod score"},
            title = "Top 10 Faculty interested in " + key_init)
            
fac_init = "Michael Franklin"
df_fac10 = sql_ob.select_top_keyword_by_faculty(fac_init)           
fig3 = px.bar(df_fac10, x="keyword", y="score", barmode="group",
            labels={"keyword": "Keyword",
                     "score": "keyworod score"},
            title = "Top 10 Keywords " +fac_init + "interested in " )

print("make favs")
fav = sql_ob.create_favorites_2()  

df_fav_empty = pd.DataFrame(columns = ["name","score"])
fig4 = px.bar(df_fav_empty, x="name", y="score", barmode="group",
            labels={"name": "Faculty Name",
                     "score": "keyworod score"},
            title = "Favorite Faculty Interest in " + key_init)

def generate_table(dataframe, max_rows=30):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

fav_tbl = generate_table(fav.iloc[:,1:6].fillna("NA"))
    
            
print("doing other stuff")          

app.layout = html.Div([
    html.Div(children=[
        #html.H1(children='Faculty of Interest Dash Board'),
        html.H1(children='Publications by Faculty'),
        #html.Div(children='''
       #     Publications by Faculty.
       # '''),

        dcc.Graph(
            id='fac-pub-neo',
            figure=fig
        ),
        
        html.Div([
            "University: ",
            dcc.Dropdown(nb.universities,id='neo_unv')  
        ]),
        html.Div([
            "Keyword: ",
            dcc.Dropdown(nb.keywords,id='neo_kw')  
        ])
    ]),  
    html.Div(children=[
        #html.Div(children='''
        #    Faculty Spotlight.
       # '''),
        html.H1(children='Faculty Spotlight'),
        html.Div([
            "Faculty: ",
            dcc.Dropdown(mb.profs,id='mb_prof')  
        ]),
        
    html.Img(id='prof_image'),
    html.Br(),
    html.Div(id='prof-unv'),
    html.Div(id='prof-pos'),
    html.Div(id='prof-ci'),
    html.Div(id='prof-pub'),
    ], style={'padding': 10, 'flex': 1}),
    
    # sql all keyword score
    html.Div(children=[
        html.H1(children='Top Faculty Anywhere for Keyword'),
        dcc.Graph(
            id='fac-key-sql',
            figure=fig2
        ),
        
        html.Div([
            "Keyword: ",
            dcc.Dropdown(sql_ob.key_nm,id='key-sql')
        ]),
    ]),
    
    html.Div(children=[
        html.H1(children='Top 10 Keywords for Faculty'),
        dcc.Graph(
            id='fac-top-key-sql',
            figure=fig3
        ),
        
        html.Div([
            "Faculty: ",
            dcc.Dropdown(sql_ob.fac_nm,id='fac-sql')
        ]),
    ]),

    html.Div([
        html.H1(children='Favorites Table'),
        dash_table.DataTable(id='fav-table'),
        html.Div([
            "Add Favorite: ",
            dcc.Dropdown(sql_ob.fac_nm,id='new-fav'), 
            "Remove Favorite: ",
            dcc.Dropdown(sql_ob.fac_nm,id='not-fav')
        ]),
     ]),
     
     
    html.Div(children=[
        html.H1(children='Favorite Faculty by Keyword'),
        dcc.Graph(
            id='fav-sql-fig',
            figure=fig4
        ),
        
        html.Div([
            "Keyword: ",
            dcc.Dropdown(sql_ob.key_nm,id='fav-key-sql')
        ]),
    ]),
])

@app.callback(
    Output('fac-pub-neo', 'figure'),
    Input('neo_unv', 'value'),
    Input('neo_kw', 'value'))
def update_neo_figure(neo_unv,neo_kw=""):
    df = nj.univ_keyword_pub_comp(nb.session,neo_unv,neo_kw)
    df = df.head(10)
    df.columns = ["Name","Pub_Count"]
    new_title = "Top 10 " + neo_unv + " Faculty in the Field of " + neo_kw

    fig = px.bar(df, x="Name", y="Pub_Count", barmode="group",
                 labels={"Name": "Faculty Name",
                     "Pub_Count": "Number of publications"},
                 title = new_title)

    fig.update_layout(transition_duration=500)

    return fig
    
@app.callback(
    Output('prof_image', 'src'),
    Output('prof-unv', 'children'),
    Output('prof-pos', 'children'),
    Output('prof-ci', 'children'),
    Output('prof-pub', 'children'),
    Input('mb_prof', 'value'))
def update_image_src(value):
    prof_info = mh.get_prof_info(mb.db,value)
    prof_info= prof_info.fillna("NA")
    unv = u'''
        University: {} 
    '''.format(prof_info.loc[0,"Unv"])
    
    pos = u'''
        Position: {} 
    '''.format(prof_info.loc[0,"position"])
    
    con_inf = u'''
        Contact info| Email: {} | Phone: {}
    '''.format(prof_info.loc[0,"email"],prof_info.loc[0,"phone"])
    
    pub1 =  u'''
        Most Cited Paper Published {} with {} Citations: {} 
    '''.format(prof_info.loc[0,"year"],prof_info.loc[0,"citations"],prof_info.loc[0,"title"])
    return(prof_info.loc[0,"photo_url"],unv,pos,con_inf,pub1)


@app.callback(
    Output('fac-key-sql', 'figure'),
    Input('key-sql', 'value'))
def update_sql_figure(key_sql):
    df_allk = sql_ob.select_top_faculty_by_keyword(key_sql,lim=10)
    print("key_sql_update")
    fig2 = px.bar(df_allk, x="name", y="score", barmode="group",
            labels={"name": "Faculty Name",
                     "score": "keyworod score"},
            title = "Top 10  Faculty interested in " + key_sql) 

    fig2.update_layout(transition_duration=500)

    return fig2   

@app.callback(
    Output('fac-top-key-sql', 'figure'),
    Input('fac-sql', 'value'))
def update_top_10_sql_figure(fac_sql):
    df_fac10 = sql_ob.select_top_keyword_by_faculty(fac_sql,lim=10)

    fig3 = px.bar(df_fac10, x="keyword", y="score", barmode="group",
            labels={"keyword": "Keyword",
                     "score": "keyworod score"},
            title = "Top 10 Keywords " +fac_sql + " interested in" )
    return fig3
    
@app.callback(Output('fav-table', 'data'),
              Output('fav-table', 'columns'),
              Input('new-fav', 'value'),
              Input('not-fav', 'value'))
def add_favorites(new_fav,not_fav):
   
    print ("New favorite is" +new_fav)
    fav2 = sql_ob.read_fav_table()
    names = list(fav2.loc[:,"f_name"])
    names = set(names+[new_fav])
    names = names-set([not_fav])
    
    #print(names)
    fav2 = sql_ob.create_favorites_2(names)  
    
    #print(fav2.columns)
    #print(fav2.loc[:,"f_name"])
    fav2.columns = ["Name","University","Position","Email","Phone"]
    
    return fav2.to_dict('records'), [{"name": i, "id": i} for i in fav2.columns]
    

@app.callback(
    Output('fav-sql-fig', 'figure'),
    Input('fav-key-sql', 'value'))
def fav_sql_figure(key_sql):
    df_favk = sql_ob.compare_favorites(key_sql,lim=10)
    print("key_sql_update")
    fig4 = px.bar(df_favk, x="name", y="score", barmode="group",
            labels={"name": "Faculty Name",
                     "score": "keyworod score"},
            title = "Favorite Faculty Interested in " + key_sql) 

    fig4.update_layout(transition_duration=500)

    return fig4
    
    return fav2.to_dict('records'), [{"name": i, "id": i} for i in fav2.columns]
if __name__ == '__main__':
    app.run_server(debug=False)
    
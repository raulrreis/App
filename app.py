import dash 
from dash import dcc, html
from dash.dependencies import Input, Output

#--------------------------
from numpy import corrcoef, linalg, dot,around,transpose
from pandas import DataFrame
from requests import get
from scipy.stats import genpareto
def Zscores(x):
    x_mean = x.mean()
    x_std = x.std()
    return (x)/x_std

def fPCA1(x):
    x_corr = corrcoef(transpose(x))
    x_value,x_vector = linalg.eig(x_corr)
    return dot(x,x_vector[:,0])

def nba_api(x = '2022-23'):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'College': '',
        'Conference': '',
        'Country': '',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'DraftPick': '',
        'DraftYear': '',
        'GameScope': '',
        'GameSegment': '',
        'Height': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': {x},
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': '',
        'Weight': '',
    }

    response = get('https://stats.nba.com/stats/leaguedashplayerstats', params=params, headers=headers)
    r_json = response.json()
    columns = r_json['resultSets'][0]['headers']
    league_df = DataFrame(r_json['resultSets'][0]['rowSet'],columns = columns)
    df=league_df.loc[league_df.GP >= 40]
    columns_x = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FTM', 'FTA', 'OREB', 'DREB', 'REB','AST','STL', 'BLK', 'TOV','PTS']
    PCA1 = fPCA1(Zscores(df[columns_x]))
    modelo = genpareto.fit(PCA1)
    shape,loc,scale = modelo
    df['SCORES'] = around(genpareto.cdf(PCA1,shape, loc,scale)*100,2)
    y_df = df[['PLAYER_ID','PLAYER_NAME','PTS','FG_PCT','REB','FG3M','AST','FTM','SCORES']].sort_values(by = 'SCORES',ascending=False)
    y_df['POSITION'] = list(range(1,df.shape[0]+1))
    return y_df
#------------------------------


app =  dash.Dash(__name__,external_stylesheets=['style.css'])
app.layout = html.Div([
    html.Header([
        html.Div(className='container',children=[
            html.Div(children=[
                html.A(className='logo-text',children = dcc.Markdown('StatN **Scores**'),href='#')]),
            html.Div([
                html.Img(id = 'img-player')
                ]),
            html.Nav([
                html.Ul([
                    html.Li(html.A(href="#",children="Home")),
                    html.Li(html.A(href="#",children="Modelo")),
                    html.Li(html.A(href="#",children="Sobre")),
                    html.Li(html.A(href="#",children="Contato"))
                ])
            ])
        ])
    ]),
    html.Section(className='section-container',children=[
        html.Div(className='container',children=[
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('POSITION'),
                        html.H3(id = 'position')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('SCORES'),
                        html.H3(id = 'scores')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('PTS'),
                        html.H3(id = 'pts')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('FG PCT'),
                        html.H3(id = 'fg_pct')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('AST'),
                        html.H3(id = 'ast')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('REB'),
                        html.H3(id = 'reb')
                    ])
                ])
            ]),
            html.Div(className='card-container',children=[
                html.Div(className='card',children=[
                    html.Div([
                        html.P('FG3M'),
                        html.H3(id = 'fg3m')
                    ])
                ])
            ])
        ])
    ]),
    html.Div(className='filter-width',children=[
        html.Div(className='container',children=[
            html.Div(className='filter-container',children=[
                html.Div(className='filter',children=[
                    html.P('Select'),
                    dcc.Dropdown(
                        id = 'select-player',
                        value = 'LeBron James'
                    )
                ])
            ]),
            html.Div(className='filter-container',children=[
                html.Div(className='filter',children=[
                    html.P('Select'),
                    dcc.Dropdown(
                        id = 'select-season',
                        value =  '2022-23'
                    )
                ])
            ])
        ])
    ]),
    html.Div(className='table-width',children=[
        html.Div(className='container',children=[
            html.Div(className='table',children=[
                dash.dash_table.DataTable(
                    id = 'data_table',
                    style_table={'height':'325px','overflowY':'auto','font-family': 'Times New Roman'},
                    style_data=  {'border':'0px','border-bottom': '1px solid #C7CDCD'},
                    style_cell = {'padding':'7px'},
                    fixed_rows={'headers':True},
                    style_header={'backgroundColor': ' #3B8BB6','padding':'auto','textAlign':'center','color':'#fff','border':'0px','border-bottom':'1px solid #C7CDCD'},
                    style_cell_conditional=[
                        {
                            'if':{'column_id':c},'textAlign':'left'
                        } for c in ['PLAYER_NAME']
                    ],
                    style_data_conditional=[
                        {
                            'if':{'filter_query':'{POSITION} > 3'},
                            'color':'#5C5C5C'
                        }
                    ]
                )
            ])
        ])
    ]),
    html.Footer([
        html.Div(className='container',children=[
            html.Nav([
                html.Ul([
                    html.Li(html.P('Endereço: Teresina, PI')),
                    html.Li(html.P('Telefone: (89) 98139-6510')),
                    html.Li(html.P('E-mail: raulrreis007@gmail.com'))
                ])
            ]),
            html.Div([
                html.P(className='copy-p',children=dcc.Markdown('&copy; 2023 Todos os direitos reservados'))
            ])
        ])
    ])
])



@app.callback(
    [
        Output('data_table','data'),
        Output('data_table','columns'),
        Output('select-season','options'),
        Output('select-player','options'),
        Output('position','children'),
        Output('scores','children'),
        Output('pts','children'),
        Output('fg_pct','children'),
        Output('ast','children'),
        Output('reb','children'),
        Output('fg3m','children'),
        Output('img-player','src')
    ],
    [
        Input('select-player','value'),
        Input('select-season','value')
    ]     	
)

def ftable(player,season):
    df = nba_api(season) 
    season = ['2019-20','2020-21','2021-22','2022-23']
    player_name = df.PLAYER_NAME.unique()
    y = df.loc[df.PLAYER_NAME==player].iloc[0]
    img_player = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{y.PLAYER_ID}.png'
    dfx = df.drop(labels='PLAYER_ID',axis=1)

    return (dfx.to_dict('records'),[{'id': c, 'name': c,'type': 'numeric', 'format':{'specifier': '.2%'}} if c == 'FG_PCT' 
                else {'id':c,'name':c, 'type':'numeric','format':{'specifier':'.2f'}} if c != 'PLAYER_NAME' and c!= 'POSITION' 
                else {'id':c, 'name':c,'type':'numeric','format':{'specifier':'.0f'}} if c == 'POSITION' else {'id':c,'name':c}  for c in dfx.columns],season,player_name,f'{y.POSITION}°',
            f'{y.SCORES:.2f}',f'{y.PTS:.2f}',f'{y.FG_PCT:.2%}',f'{y.AST:.2f}',f'{y.REB:.2f}',f'{y.FG3M:.2f}',img_player)



if __name__ == '__main__':
    app.run_server(debug = False)
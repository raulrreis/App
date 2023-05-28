import dash 
from dash import dcc, html
from dash.dependencies import Input, Output
from pandas import read_csv

app =  dash.Dash(__name__,external_stylesheets=['style.css'])
server = app.server 
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
    dd = read_csv('nba.csv',sep = ';',decimal=',')
    seasons = dd.SEASON.unique()
    df = dd.loc[dd.SEASON == season]
    player_name = df.PLAYER_NAME.unique()
    y = df.loc[df.PLAYER_NAME==player].iloc[0]
    img_player = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{y.PLAYER_ID}.png'
    dfx = df.drop(labels=['PLAYER_ID','SEASON'],axis=1)

    return (dfx.to_dict('records'),[{'id': c, 'name': c,'type': 'numeric', 'format':{'specifier': '.2%'}} if c == 'FG_PCT' 
                else {'id':c,'name':c, 'type':'numeric','format':{'specifier':'.2f'}} if c != 'PLAYER_NAME' and c!= 'POSITION' 
                else {'id':c, 'name':c,'type':'numeric','format':{'specifier':'.0f'}} if c == 'POSITION' else {'id':c,'name':c}  for c in dfx.columns],seasons,player_name,f'{y.POSITION}°',
            f'{y.SCORES:.2f}',f'{y.PTS:.2f}',f'{y.FG_PCT:.2%}',f'{y.AST:.2f}',f'{y.REB:.2f}',f'{y.FG3M:.2f}',img_player)



if __name__ == '__main__':
    app.run_server(debug = False)

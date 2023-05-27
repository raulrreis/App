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

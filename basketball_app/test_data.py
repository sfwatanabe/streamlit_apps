import pandas as pd
import numpy as np



url = f"https://www.basketball-reference.com/leagues/NBA_2020_per_game.html"
html = pd.read_html(url, header=0)
df = html[0]
df = df.drop(df[df.Age == 'Age'].index)
print(df.isnull().sum())
df[df.filter(regex=('\w+[%]')).columns] = df[df.filter(regex=('\w+[%]')).columns].fillna(12345)
cols = ['Rk', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
       '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
       'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']


print(df.isnull().sum())


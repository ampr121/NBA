from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# NBA season we will be analyzing
year = 2019
# URL page we will scraping (see image above)
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_minute.html".format(year)
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

# use findALL() to get the column headers
soup.findAll('tr', limit=2)
# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]

# avoid the first header row
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

stats = pd.DataFrame(player_stats, columns = headers)
stats = stats[pd.notnull(stats['PTS'])]
stats[['PTS','G']] = stats[['PTS','G']].apply(pd.to_numeric, errors='coerce').fillna(0)
stats['PTS'] = stats['PTS'].clip(10.0,50.0)
stats = stats[stats['G'] > 20]
stats = stats.sort_values(['PTS','G'], ascending=False)
stats['Player'] = stats['Player'].drop_duplicates(keep='first')
stats = stats[pd.notnull(stats['Player'])]
stats = stats.drop(['Pos','Age','G','GS','FGA','FG','2P','2PA','3P','3PA','ORB','DRB','FT','MP','STL','BLK','TOV','PF', 'FTA', 'FT%'], axis=1)
stats = stats.reset_index(drop=True)
stats[['FG%','3P%','2P%','TRB','AST']] = stats[['FG%','3P%','2P%','TRB','AST']].apply(pd.to_numeric, errors='coerce').fillna(0)
stats = stats[stats['FG%'] > 0.40]
stats = stats[stats['3P%'] > 0.32]
stats = stats[stats['2P%'] > 0.45]
stats = stats[stats['TRB'] > 5.0]
stats = stats[stats['AST'] > 5.0]
stats = stats.reset_index(drop=True)
print(stats)

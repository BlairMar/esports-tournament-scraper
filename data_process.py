import json
from re import A
from numpy import NaN
import pandas as pd
from json import encoder
import datetime
import pymysql 
import psycopg2
from sqlalchemy import column, create_engine
import tabloo
from pprint import pprint as pp
from pandasgui import show

# details to connect to the rds my sql database
host='esports-scraper.cb01bw8mxu9w.eu-west-1.rds.amazonaws.com'
port=int(5432)
user="postgres"
passw=""                    
database="postgres"

# import all .json files to clean
tournaments_dataframe = pd.read_json('tournaments.json')
steam_charts_dataframe = pd.read_json('steamdata.json')
wow_subs_dataframe = pd.read_json('wowsubs.json')
active_players_dataframe = pd.read_json('activeplayers.json')
league_players = pd.read_json('leagueplayers.json')

steam_charts_dataframe = steam_charts_dataframe.rename(columns={'G,a,m,e' : 'Game'}) 
steam_charts_col_names = steam_charts_dataframe.columns.tolist()        

league_players.drop(league_players.loc[league_players['Month'] == "Last 30 Days"].index, inplace=True)
league_players['Month'] = pd.to_datetime(league_players.Month, format="%B %d, %Y").dt.strftime('%m-%Y')
league_players = league_players.rename(columns={'Average Monthly Players' : 'Avg. Players', 'Peak Players In a Day' : 'Peak Players', 'Monthly Gain / Loss' : 'Gain', 'Monthly Gain / Loss %' : 'Gain %'})
league_players['Avg. Players'] = league_players['Avg. Players'].str.replace(r'\D+', '')
league_players['Peak Players'] = league_players['Peak Players'].str.replace(r'\D+', '')
league_players = league_players.replace({'League of Legends' : 'LoL'})

active_players_dataframe['Peak Players In a Day'] = active_players_dataframe['Peak Players In a Day'].astype(str) + active_players_dataframe['Max Players in a Day'].astype(str) + active_players_dataframe['Max Player in a Day'].astype(str)
active_players_dataframe = active_players_dataframe.rename(columns={'G,a,m,e' : 'Game'})             # remove unneeded columns                                                              # set the columns to the steamchart data columns to the tables can be easily appended
active_players_dataframe = active_players_dataframe.drop([0])
active_players_dataframe = active_players_dataframe.drop(columns=['Max Players in a Day', 'Max Player in a Day']) 
active_players_dataframe.columns = steam_charts_col_names  
active_players_dataframe.drop(active_players_dataframe.loc[active_players_dataframe['Month'] == "Last 30 Days"].index, inplace=True)
active_players_dataframe.drop(active_players_dataframe.loc[active_players_dataframe['Month'] == " "].index, inplace=True)
active_players_dataframe['Avg. Players'] = active_players_dataframe['Avg. Players'].str.replace(r'\D+', '')
active_players_dataframe['Peak Players'] = active_players_dataframe['Peak Players'].str.replace(r'\D+', '')
active_players_dataframe['Month'] = pd.to_datetime(active_players_dataframe.Month, format="%B %d, %Y").dt.strftime('%m-%Y')

active_players_dataframe = active_players_dataframe.replace({'Fornite' : 'Fortnite', 'Garena Free Fire' : 'Free Fire', 'Arena of Valor' : 'KoG', "Overwatch" : "OW"})

#steam_charts_dataframe['Game'] = steam_charts_dataframe['Game'].map(lambda x: x.lstrip("['").rstrip("']"))                      # remove unnecessary brackets and quotes from the steamcharts Game column
steam_charts_dataframe = steam_charts_dataframe.drop([0])                                                                       
steam_charts_dataframe.drop(steam_charts_dataframe.loc[steam_charts_dataframe['Month'] == "Last 30 Days"].index, inplace=True)
steam_charts_dataframe['Avg. Players'] = steam_charts_dataframe['Avg. Players'].str.replace(r'\D+', '')
steam_charts_dataframe['Peak Players'] = steam_charts_dataframe['Peak Players'].str.replace(r'\D+', '') 
steam_charts_dataframe['Month'] = pd.to_datetime(steam_charts_dataframe.Month, format="%B %Y").dt.strftime('%m-%Y')
steam_charts_dataframe = steam_charts_dataframe.replace({'Rocket League' : 'RL', 'Counter-Strike: Global Offensive' : 'CS:GO', "PLAYERUNKNOWN\'S BATTLEGROUNDS" : 'PUBG', "Tom Clancy\'s Rainbow Six Siege" :  'R6', 'EA SPORTS™ FIFA 21' : 'FIFA'})

# pivot on the Game column cause I made a mess of the .json tournament data and didn't want to rescrape lol
tournaments_dataframe = tournaments_dataframe.melt(['Start Date','End Date', 'Prize Pool', 'Location'], var_name='Game')  
tournaments_dataframe = tournaments_dataframe.rename(columns={'value' : 'Tournament Name'})
tournaments_dataframe = tournaments_dataframe[['Game', 'Tournament Name', 'Location', 'Start Date', 'End Date', 'Prize Pool']]
tournaments_dataframe['Prize Pool'] = tournaments_dataframe['Prize Pool'].str.replace(r'\D+', '') 
tournaments_dataframe.drop(tournaments_dataframe.loc[tournaments_dataframe['End Date'] == "Not ended"].index, inplace=True)
tournaments_dataframe['Start Date'] = pd.to_datetime(tournaments_dataframe['Start Date'], format="%d.%m.%Y").dt.strftime('%m-%Y')
tournaments_dataframe['End Date'] = pd.to_datetime(tournaments_dataframe['End Date'], format="%d.%m.%Y").dt.strftime('%m-%Y')
tournaments_dataframe['End Date'] = pd.to_datetime(tournaments_dataframe['End Date'])
tournaments_dataframe['Start Date'] = pd.to_datetime(tournaments_dataframe['Start Date'])
tournaments_dataframe['Tour date'] = (tournaments_dataframe['End Date'] - tournaments_dataframe['Start Date']).dt.days    
tournaments_dataframe = tournaments_dataframe.dropna()   
tournaments_dataframe.drop(tournaments_dataframe.loc[tournaments_dataframe.Game.isin(['HotS', 'Valorant', 'SC', 'SCII', 'Smash', 'CoD', ''])].index, inplace=True)      
tournaments_dataframe.drop(tournaments_dataframe.loc[tournaments_dataframe['Prize Pool'] == ''].index, inplace=True)  
tournaments_dataframe = tournaments_dataframe.replace({'PUBG Mobile' : 'PUBG'})   
#tournaments_dataframe.drop(tournaments_dataframe.loc[pd.to_datetime(tournaments_dataframe['Start Date']) <= '01-2019'].index, inplace=True)                                
tournaments_dataframe["Prize Pool"] = tournaments_dataframe["Prize Pool"].str.replace(r'\D+', '')

# append all the tournament 
total_players_df = active_players_dataframe.append(steam_charts_dataframe)
total_players_df = total_players_df.append(league_players)
total_players_df['Month'] = pd.to_datetime(total_players_df['Month'])

final_frame = pd.merge(total_players_df, tournaments_dataframe, left_on=["Game", "Month"], right_on=["Game","Start Date"])
final_frame = final_frame.drop(columns=['% Gain', 'Gain', 'Gain %', 'Location']) 
final_frame.replace("", NaN, inplace=True)
final_frame['Tour date'] = final_frame['Tour date'].replace(0,1)
final_frame = final_frame.dropna()


d_types = {'Game' : 'str', 'Avg. Players' : int, 'Peak Players' : int, 'Tournament Name' : 'str', 'Prize Pool': int}
final_frame['End Date'] = pd.to_datetime(final_frame['End Date'])
final_frame['Start Date'] = pd.to_datetime(final_frame['Start Date'])
final_frame['Month'] = pd.to_datetime(final_frame['Month'])
final_frame = final_frame.astype(d_types)
game_types = {'SMITE' : 'MOBA', 
            'Fortnite' : 'Battle Royale', 
            'Lol' : 'MOBA', 
            'R6' : 'FPS', 
            'RL' : 'Sports', 
            'FIFA' : 'Sports', 
            'LoL' : 'MOBA', 
            'OW' : 'FPS', 
            'CS:GO' : 'FPS', 
            'Hearthstone' : 'Strategy',
            'PUBG' : 'Battle Royale',
            'KoG' : 'MOBA',
            'Free Fire' : 'Battle Royale',
            'Dota 2' : 'Moba' }

final_frame['Game Type'] = final_frame['Game'].map(game_types)

#final_frame['No. tour days'] = final_frame['End Date'] - final_frame['Start Date']



# mydb = create_engine('postgresql+psycopg2://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=True)  #create string to send the data to the database on RDS
# # covert the dataframes to sql and use the create_engine string to send to AWS
# tournaments_dataframe.to_sql(name="Tournament_Data", con=mydb, if_exists = 'replace', index=True)                                   
# total_players_df.to_sql(name="Player_Data", con=mydb, if_exists = 'replace', index=True)
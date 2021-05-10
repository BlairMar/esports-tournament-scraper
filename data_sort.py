import json
import pandas as pd
from json import encoder
import datetime
import pymysql
from sqlalchemy import create_engine

host=’deneme.cykgvlpxbgsw.us-east-2.rds.amazonaws.com’
port=int(3306)
user=”admin”
passw=”Ethan105”
database=”scraper”

tournaments_dataframe = pd.read_json('tournaments.json')
steam_charts_dataframe = pd.read_json('steamdata.json')
wow_subs_dataframe = pd.read_json('wowsubs.json')
active_players_dataframe = pd.read_json('activeplayers.json')


steam_charts_col_names = steam_charts_dataframe.columns.tolist()

active_players_dataframe = active_players_dataframe.drop(columns=['Max Players in a Day', 'Max Player in a Day'])
active_players_dataframe.columns = steam_charts_col_names
active_players_dataframe = active_players_dataframe.drop([0])
active_players_dataframe = active_players_dataframe.reset_index()

steam_charts_dataframe['Game'] = steam_charts_dataframe['Game'].map(lambda x: x.lstrip("['").rstrip("']"))
steam_charts_dataframe = steam_charts_dataframe.drop([0])
steam_charts_dataframe = steam_charts_dataframe.reset_index()

tournaments_dataframe = tournaments_dataframe.melt(['Start Date','End Date', 'Prize Pool', 'Location'], var_name='Game')
tournaments_dataframe = tournaments_dataframe.rename(columns={'value' : 'Tournament Name'})
tournaments_dataframe = tournaments_dataframe[['Game', 'Tournament Name', 'Location', 'Start Date', 'End Date', 'Prize Pool']]
tournaments_dataframe = tournaments_dataframe.dropna()

wow_subs_dataframe.columns = ['Game', 'Month', 'Peak Players', 'Avg. Players']


total_players_df = active_players_dataframe.append(steam_charts_dataframe)
total_players_df = total_players_df.append(wow_subs_dataframe)
total_players_df = total_players_df.drop(columns='index')


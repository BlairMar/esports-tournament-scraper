import json
import pandas as pd
from json import encoder
import datetime
import pymysql 
import psycopg2
from sqlalchemy import create_engine

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

steam_charts_col_names = steam_charts_dataframe.columns.tolist()           

active_players_dataframe = active_players_dataframe.drop(columns=['Max Players in a Day', 'Max Player in a Day'])               # remove unneeded columns 
active_players_dataframe.columns = steam_charts_col_names                                                                       # set the columns to the steamchart data columns to the tables can be easily appended
active_players_dataframe = active_players_dataframe.drop([0])
active_players_dataframe = active_players_dataframe.reset_index()

steam_charts_dataframe['Game'] = steam_charts_dataframe['Game'].map(lambda x: x.lstrip("['").rstrip("']"))                      # remove unnecessary brackets and quotes from the steamcharts Game column
steam_charts_dataframe = steam_charts_dataframe.drop([0])                                                                       
steam_charts_dataframe = steam_charts_dataframe.reset_index()   

# pivot on the Game column cause I made a mess of the .json tournament data and didn't want to rescrape lol
tournaments_dataframe = tournaments_dataframe.melt(['Start Date','End Date', 'Prize Pool', 'Location'], var_name='Game')        
tournaments_dataframe = tournaments_dataframe.rename(columns={'value' : 'Tournament Name'})
tournaments_dataframe = tournaments_dataframe[['Game', 'Tournament Name', 'Location', 'Start Date', 'End Date', 'Prize Pool']]
tournaments_dataframe = tournaments_dataframe.dropna()                                                                          # drop all Nan values from the table as the pivot created un necessary data

wow_subs_dataframe.columns = ['Game', 'Month', 'Peak Players', 'Avg. Players']                                                  

# append all the tournament 
total_players_df = active_players_dataframe.append(steam_charts_dataframe)
total_players_df = total_players_df.append(wow_subs_dataframe)
total_players_df = total_players_df.drop(columns='index')

mydb = create_engine('postgresql+psycopg2://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database , echo=True)  #create string to send the data to the database on RDS
# covert the dataframes to sql and use the create_engine string to send to AWS
tournaments_dataframe.to_sql(name="Tournament_Data", con=mydb, if_exists = 'replace', index=True)                                   
total_players_df.to_sql(name="Player_Data", con=mydb, if_exists = 'replace', index=True)
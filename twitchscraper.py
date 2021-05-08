from scrapelib import *

# #%%
# tournament_data_scraper = Scraper('https://www.esportsguide.com/events/csgo')
# next_page_links = ("xpath", '//*[@id="filter_games"]/li/a', "get_attribute", "('href')")
# tournament_links = ("class_name", 'single-event-card__tourn-link', "get_attribute", "('href')")
# tournament_names = ('xpath' , '//h1[@class="tournament-block__title"]', "text", None)
# tournament_field_titles = ("xpath", '//p[@class="tournament-block__details-title"]', "text", None)
# tournament_field_values = ("xpath", '//span[@class="tournament-block__details-info"]', "text", None)
# game_name = ("xpath", '//li[1]/span[@class="title"]' , "text", None)
# tournament_data_scraper.scrape(next_page_links, 'test', tournament_links, True, 2, game_name, tournament_names, tournament_field_titles, False, tournament_field_values)

#%%
from scrapelib import *
Wowscraper = Scraper('https://mmo-population.com/r/wow/stats')
keys = ('xpath', '//tr/th[@scope ="col"]', "text", None)
dates_subs_active_users = ('xpath', '//td[starts-with(@style ,"text-align")]', "text", None)
Wowscraper.scrape(None, 'wowsubs', None, False, 0, "Game Name", "Wow", keys, True, dates_subs_active_users)

# Steamcharts = Scraper('https://steamcharts.com/')
# steam_next_page_list = ['https://steamcharts.com/app/252950', 
#                           'https://steamcharts.com/app/730', 
#                           'https://steamcharts.com/app/570', 
#                           'https://steamcharts.com/app/578080', 
#                           'https://steamcharts.com/app/359550',
#                           'https://steamcharts.com/app/1313860',
#                           'https://steamcharts.com/app/386360']
# steam_game_data = ("xpath", '//*[@class="odd"]//td', 'text' , None)
# dict_keys_steam = ('xpath', '//*[@class="common-table"]//tr/th', 'text', None)
# Steamcharts.scrape(steam_next_page_list, 'steamdata', None, False, 0 ,"Game", "CS:GO", dict_keys_steam, True, steam_game_data)

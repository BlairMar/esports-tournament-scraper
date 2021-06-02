from scrapelib import *
from multiprocessing.dummy import Pool as ThreadPool


#initialise a scraper and defined landing page
# tournament_data_scraper = Scraper('https://www.esportsguide.com/events/csgo')
# # defining either the data to scrape or the links to go to on the webpage
# main_page_links = ("xpath", '//*[@id="filter_games"]/li/a', "get_attribute", "('href')")
# tournament_links = ("class_name", 'single-event-card__tourn-link', "get_attribute", "('href')")
# tournament_names = ('xpath' , '//h1[@class="tournament-block__title"]', "text", None)
# tournament_field_titles = ("xpath", '//p[@class="tournament-block__details-title"]', "text", None)
# tournament_field_values = ("xpath", '//span[@class="tournament-block__details-info"]', "text", None)
# game_name = ("xpath", '//li[1]/span[@class="title"]' , "text", None)
# # refer to docstring for description of parameters, run main scrape method
# tournament_data_scraper.scrape(main_page_links, 'tournaments', tournament_links, True, 3, game_name, tournament_names, tournament_field_titles, False, tournament_field_values)  

# Wowscraper = Scraper('https://mmo-population.com/r/wow/stats')
# # defining either the data to scrape or the links to go to on the webpage
# keys = ('xpath', '//tr/th[@scope ="col"]', "text", None)
# dates_subs_active_users = ('xpath', '//td[starts-with(@style ,"text-align")]', "text", None)
# Wowscraper.scrape(None, 'wowsubs', None, False, 0, "Game Name", "Wow", keys, True, dates_subs_active_users)

# Steamcharts = Scraper('https://steamcharts.com/')
# steam_next_page_list = ['https://steamcharts.com/app/252950', 
#                           'https://steamcharts.com/app/730', 
#                           'https://steamcharts.com/app/570', 
#                           'https://steamcharts.com/app/578080', 
#                           'https://steamcharts.com/app/359550',
#                           'https://steamcharts.com/app/1313860',
#                           'https://steamcharts.com/app/386360']
# steam_game_data = ("xpath", '//*[@class="common-table"]//tr/td', 'text' , None)
# dict_keys_steam = ('xpath', '//*[@class="common-table"]//tr/th', 'text', None)
# steam_game_name = ('xpath', '//*[@id="app-title"]/a', 'text', None)
# #refer to docstring for description of parameters, run main scrape method
# Steamcharts.scrape(steam_next_page_list, 'steamdata', None, False, 0 ,"Game", steam_game_name, dict_keys_steam, True, steam_game_data) 

# league_scraper = Scraper('https://activeplayer.io/')
# league_main_page_links = ['https://activeplayer.io/fornite/',
#                           'https://activeplayer.io/garena-free-fire/',
#                           'https://activeplayer.io/hearthstone/',
#                           'https://activeplayer.io/arena-of-valor/',
#                           'https://activeplayer.io/overwatch/']
# game_names = ('xpath', '//h1[@class = "jeg_post_title"]' , 'text', None)
# league_key_values = ('xpath', '//*[@class="google-visualization-table-tr-head"]//th', 'text', None)
# league_data_values = ('xpath', '//*[starts-with(@class, "google-visualization-table-tr")]//td', 'text', None)
# # refer to docstring for description of parameters, run main scrape method
# league_scraper.scrape(league_main_page_links, 'activeplayers', None, False, 0, "Game", game_names, league_key_values, True, league_data_values)


game_page_list = [
        'https://www.esportsearnings.com/games/409-rocket-league/largest-tournaments',
        'https://www.esportsearnings.com/games/231-dota-2/largest-tournaments']
        
for game in game_page_list:
    Tourscrape = Scraper(game)
    tour_page = ('xpath', '//table[@class="detail_list_table"]//a[not(@title)]', "get_attribute", "('href')")
    next_links = ('xpath', '//nav[@class="navoptions_box detail_box_nav_big"]//a', 'get_attribute', "('href')")
    tour_keys = ('xpath', '//div[@class="format_cell info_text_header"]', "text", None)
    tour_vals = ('xpath', '//div[@class="format_cell info_text_value"]', "text", None)
    head_value = ('xpath', '//h1[@class="info_box_title"]', "text", None)
    Tourscrape.scrape(next_links, 'tour2', tour_page,  False, 0, 'Tour', head_value, tour_keys, False, tour_vals)

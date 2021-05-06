from scrapelib import *


tournament_data_scraper = Scraper('https://www.esportsguide.com/events/csgo')
next_page_links = ("xpath", '//*[@id="filter_games"]/li/a', "get_attribute", "('href')")
tournament_links = ("class_name", 'single-event-card__tourn-link', "get_attribute", "('href')")
tournament_names = ('xpath' , '//h1[@class="tournament-block__title"]', "text", None)
tournament_field_titles = ("xpath", '//p[@class="tournament-block__details-title"]', "text", None)
tournament_field_values = ("xpath", '//span[@class="tournament-block__details-info"]', "text", None)
game_name = ("xpath", '//li[1]/span[@class="title"]' , "text", None)
tournament_data_scraper.scrape(next_page_links, 'test' , tournament_links, False, 20, tournament_field_titles, False, tournament_field_values)
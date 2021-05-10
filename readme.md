# Esports Tournament Scraper

This Esports Tournament scraper is designed to scrape data to analyse the question, how much can game developers increase their active player base by investing in esports tournaments?

To meet this goal the idea was to scrape esports tournament data from the web such as: tournament prize pool, tournament date, game player and location. Additionally monthly player data was scraped from website to use as a basis to compare the effect tournaments had on the active player base for each game. 

Upon starting this project it was clear that the information required to analyse this question was hosted on many different websites. Due to the limitations of create an individual `.py` file for each website to scrape. I developed a  `Scraper()` class which could scrape the required websites in a few lines of code. Allowing this class to have flexibility to be applied to quickly scrape web data for future projects. 


## Installation 

scrapelib.py contains the scraper class and all associated functions needed to launch a new scraper.

`Import scrapelib.py` into any python file where you want to create new web scrapers.


## Usage

Each new scraper is initialised using the scraper class `Scraper()`.

Elements of the website you would like the scraper to retrieve can be defined by a tuple of strings.

### Examples:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```game_titles = ("xpath", '//li[1]/span[@class="title"]' , "text", None)```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```tournament_link = ("class_name", 'single-event-card__tourn-link', "get_attribute", "('href')")```

Which would a text element by xpath and a website like by class name respectively.


The scraper is then launched by it's scrape function ```Scraper.scrape()``` , please refer to the functions doc string for the available parameters.




## Roadmap

Additional features to include in the future would be:


* Using the Tkinter Python library create a GUI to allow webpages to be scraped graphically to promote user friendliness. 

* Apply machine learning techniques to analyse the data.

* Apply machine learning techniques to automate the web scrapers ability to scrape data.

* Add recursive function for 

## License

[MIT](https://choosealicense.com/licenses/mit/)
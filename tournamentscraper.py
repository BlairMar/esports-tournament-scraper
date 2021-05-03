
#%%
#import request
from selenium import webdriver 
import json
from time import sleep

# Some funky things you can do to find the elements you want
# multiple condition: //div[@class='bubble-title' and contains(text(), 'Cover')]
# partial match: //span[contains(text(), 'Assign Rate')]
# starts-with: //input[starts-with(@id,'reportcombo')]
# value has spaces: //div[./div/div[normalize-space(.)='More Actions...']]
# sibling: //td[.='LoadType']/following-sibling::td[1]/select"
# more complex: //td[contains(normalize-space(@class), 'actualcell sajcell-row-lines saj-special x-grid-row-collapsed')

#%%
class TournamentScraper():
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.esportsguide.com/events/csgo')
        sleep(2)

        self.tournament_links = self._get_data("class_name", 'single-event-card__tourn-link', "get_attribute", "('href')")
        self.next_link = self._get_data("xpath", '//*[@id="filter_games"]/li[1]/a', "get_attribute", "('href')")
        
        print(self.next_link)
    def _scrape(self):

        for next in self.next_link:
            tournament_details = []   
            self.driver.get(next)
            self._load_all_tournaments(0.5)
            for link in self.tournament_links:
                self.driver.get(link)
                tournament_details.append(self._get_data("xpath", '//*[@id="content"]/div[4]/div[2]/div', "text", None))
                self._save_data('testingdata', tournament_details)
                

    def _load_all_tournaments(self, pause_time : float):
        last_scroll_height = self.driver.execute_script("return 0.8*document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, 0.8*document.body.scrollHeight);")

            sleep(pause_time)

            new_scroll_height = self.driver.execute_script('return 0.8*document.body.scrollHeight')
            if new_scroll_height == last_scroll_height:
                break
            last_scroll_height = new_scroll_height
    
    
    def _get_data_from_webelement_list(self, web_element_list : list, attri : str, attri_type: str) -> list:
            list_name_output = []
            for web_element in web_element_list:
                if attri_type == None:
                    list_name_output.append(getattr(web_element, attri))
                else:
                    list_name_output.append(getattr(web_element, attri)(eval(attri_type)))
            return list_name_output

    def _get_data(self, data_type : str,
                             path : str,  
                        attribute : str,
                   attribute_type : str) -> list:
        web_ele_statement = f"self.driver.find_elements_by_{data_type}('{path}')"
        get_webelement = eval(web_ele_statement)
        list_name = self._get_data_from_webelement_list(get_webelement, attribute, attribute_type)   
        return list_name 

    def _save_data(self, file_name : str, *webelement_lists: list, save_type : str):
        if save_type == 'l':
            json_output = list(zip(*webelement_lists))
        elif save_type == 'd':
            json_output = dict(zip(*webelement_lists))
        json_filename = f'{file_name}.json'
        with open(json_filename, 'w') as f:
            json.dump(json_output, f, indent=4, ensure_ascii="False")

       
test = TournamentScraper()
test._scrape()

        
    

## %%

# %%

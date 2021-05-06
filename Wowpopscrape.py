from selenium import webdriver
import json
from itertools import cycle


class WowPopScraper():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://mmo-population.com/r/wow/stats')

    def _scrape(self):
        self.json_data = []
        self.keys = self._get_data('xpath', '//tr/th[@scope ="col"]', "text", None)
        self.dates_subs_active_users = self._get_data('xpath', '//td[starts-with(@style ,"text-align")]', "text", None)
        for stats in self.dates_subs_active_users:
            self.json_data.append(self._save_data('d', "Game Name", "Wow", cycle(self.keys), self.dates_subs_active_users))
        self._finalise_data('wowsubs', 'a', self.json_data)
        

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

    def _save_data(self, save_type : str, 
                       header_name : str, 
                     header_values : list, 
                  *webelement_lists: list):
        #header_name = ','.join(header_name)
        #header_values = ','.join(header_values)
        if save_type == 'l':
            self.json_output = list(zip(*webelement_lists))
        elif save_type == 'd':
            self.json_output = ({f"{header_name}" : f"{header_values}"})
            self.json_output.update(dict(zip(*webelement_lists)))
        return self.json_output

    def _finalise_data(self, json_filename :  str , add_mode : str, json_final_output):
        self.json_filename = f'{json_filename}.json'
        with open(self.json_filename, add_mode, encoding='utf-8') as f:
             json.dump(json_final_output, f, ensure_ascii="false", indent=4)   

wowpop = WowPopScraper()
wowpop._scrape()
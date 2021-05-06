from os import name
import json
from selenium import webdriver
from time import sleep
from itertools import cycle


class Scraper():

    def __init__(self, landing_page : str):
        self.driver = webdriver.Chrome()
        self.driver.get(landing_page)
        sleep(2)

    def scrape(self, next_links : list,
                  json_filename :  str,
               next_details_page: list, 
                    scroll_page : bool, 
                 page_wait_time : float,
                      dict_keys : list,
                 dict_cycle_keys: bool,
                *data_to_scrape : list,):
        
        self.json_data = []
        
        extracted_next_page_links = self.get_data(next_links)

        for next_link in extracted_next_page_links:
            self.driver.get(next_link)
            if scroll_page == True:
                self._load_web_data(page_wait_time)
            else:
                break
        
            extracted_next_details_link = self.get_data(next_details_page)
            print(extracted_next_details_link)

            for next_page in extracted_next_details_link:
                self.driver.get(next_page)

            


                if dict_cycle_keys == "True":
                    self.json_data.append(self._save_data('d', "", "", cycle(dict_keys), *data_to_scrape))
                else:
                    self.json_data.append(self._save_data('d', "", "", dict_keys, *data_to_scrape))

        self._finalise_data(f'{json_filename}', 'a', self.json_data)


    def get_data_from_webelement_list(self, web_element_list : list, attri : str, attri_type: str) -> list:
            self.list_name_output = []
            for web_element in web_element_list:
                if attri_type == None:
                    self.list_name_output.append(getattr(web_element, attri))
                else:
                    self.list_name_output.append(getattr(web_element, attri)(eval(attri_type)))
            return self.list_name_output

    def get_data(self, data_location_tuple: tuple):

        data_type, path, attribute, attribute_type = data_location_tuple
        self.web_ele_statement = f"self.driver.find_elements_by_{data_type}('{path}')"
        self.get_webelement = eval(self.web_ele_statement)
        self.list_name = self.get_data_from_webelement_list(self.get_webelement, attribute, attribute_type)   
        return self.list_name 

    def _load_web_data(self, pause_time : float):
        last_scroll_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(pause_time)

            new_scroll_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_scroll_height == last_scroll_height:
                break
            last_scroll_height = new_scroll_height

    def _save_data(self, save_type : str, 
                       header_name : str, 
                     header_values : list, 
                  *webelement_lists: list):
        header_name = ','.join(header_name)
        header_values = ','.join(header_values)
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



# %%

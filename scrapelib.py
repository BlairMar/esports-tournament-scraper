import json
from selenium import webdriver
from time import sleep
from itertools import cycle
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Scraper():

    def __init__(self, landing_page : str):
        self.driver = webdriver.Chrome()
        self.driver.get(landing_page)
        sleep(2)

    def scrape(self, next_links,
                  json_filename :  str,
              next_details_page : list, 
                    scroll_page : bool, 
                 page_wait_time : float,
                   header_names : str,
                   header_value : str,
                      dict_keys : list,
                 dict_cycle_keys: bool,
                *data_to_scrape : list):
        
        self.json_data = []

        if type(next_links) == tuple:
            extracted_next_page_links = self.get_data(next_links)
        else:
             extracted_next_page_links = next_links

        if next_links != None and next_details_page != None :
            for nextone in extracted_next_page_links:
                self.driver.get(nextone)
                if scroll_page == True:
                    self._load_web_data(page_wait_time)
   
                    extracted_next_details_link = self.get_data(next_details_page)
                    for next_page in extracted_next_details_link:
                        self.driver.get(next_page)

                        print(self.json_data)
                    
                        self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape )
        
        elif next_links != None and next_details_page == None:
            print("Entered loop")
            for nextone in extracted_next_page_links:
                self.driver.get(nextone)
                if scroll_page == True:
                    self._load_web_data(page_wait_time)
                else:
                    pass

                self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape )
                        

        elif next_links == None and next_details_page == None:   

            self.json_data.append(self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape))

                
        self._finalise_data(json_filename, 'a', self.json_data)
        self.driver.quit()


    def create_dictionary_list(self, dictionary_keys, dict_cycle, head_name, head_val, *data_values):
        
        new_data = self.get_data(*data_values)
        print(len(new_data))
        for data in range(0, len(new_data), len(self.get_data(dictionary_keys))):
            if dict_cycle == True: 
                self.temp_dict = {}          
                self.temp_dict.update(self._save_data('d', head_name, head_val, self.get_data(dictionary_keys), new_data[data : data + (len(self.get_data(dictionary_keys))) ]))
            else:
                self.temp_dict.update(self._save_data('d', head_name, head_val, self.get_data(dictionary_keys), new_data))
        
        return self.temp_dict   


    def get_data_from_webelement_list(self, web_element_list : list, attri : str, attri_type: str) -> list:
            self.list_name_output = []
            for web_element in web_element_list:
                if attri_type == None:
                    self.list_name_output.append(getattr(web_element, attri))
                else:
                    self.list_name_output.append(getattr(web_element, attri)(eval(attri_type)))
            return self.list_name_output

    def get_data(self, data_location_tuple: tuple):
        if data_location_tuple == None:
            return None
        else:
            (data_type, path, attribute, attribute_type) = data_location_tuple
            self.web_ele_statement = f"self.driver.find_elements_by_{data_type}('{path}')"
            self.get_webelement = eval(self.web_ele_statement)
            self.list_name = self.get_data_from_webelement_list(self.get_webelement, attribute, attribute_type)   
        return self.list_name 


    # def _load_web_data(self, pause_time : float):
    #     screen_height = self.driver.execute_script("return window.screen.height;")
    #     i = 1
    #     while True:
    #         self.driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    #         i += 1
    #         sleep(pause_time)
    #         # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    #         scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
    #         # Break the loop when the height we need to scroll to is larger than the total scroll height
    #         if (screen_height) * i > scroll_height:
    #             break 

    def _load_web_data(self, pause_time : float):
        last_scroll_height = self.driver.execute_script("return 0.5*document.body.scrollHeight")
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

        # if header_names and header_values == None:
        #     pass
        # else:  
        #     header_names = ','.join(header_names)
        #     header_values = ','.join(header_values)

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

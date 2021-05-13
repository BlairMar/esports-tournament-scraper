import json
from selenium import webdriver
from time import sleep
from itertools import cycle
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options


# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-extensions')


class Scraper():

    def __init__(self, landing_page : str):       # specify landing_page for scraper to start from
        self.driver = webdriver.Chrome()          # start the web chrome driver
        self.driver.get(landing_page)             # get the initial landing page to begin scraping
        sleep(2)     
        
        # pool = ThreadPool(8)
        # results = pool.map(self.driver.get(), next_page)                             # wait 2 seconds for all elements to load

    def scrape(self, main_page_links,                  
                  json_filename :  str,            
              next_details_page : tuple,            
                    scroll_page : bool,            
                 page_wait_time : float,           
                   header_names : str,             
                   header_value : str,             
                      dict_keys : list,            
                 dict_cycle_keys: bool,            
                *data_to_scrape : list):           
        '''
        Scraper function that scraps the data from webpages and then output the data to a .json file

        Parameters:
        -----------------------------------------------------
        main_page_links: list of main page links or list of web elements containing the main page links to scrape. 

        json_filename: filename to output the final scraped data to after completion.

        next_details_page: Tuple that points the selenium web driver to the 

        scroll_page: Boolean to determine wether to scroll the page to load more elements.

        page_wait_time: Float to specify the time to wait between loading page elements to give them time to load.
        
        header_name: Tuple pointing to web element string to append to each dictionary in the json file as a header key.

        header_value: Tuple pointing to web element or string to append to each dictionary as the header value of the associated key.

        dict_keys: Tuple point to web elements used as dictionary keys for each json file entry.

        dict_cycle_keys: Boolean to determine wether to cycle the list of dict_keys on each json entry. Useful if data comes from a table with column headers.

        data_to_scrape: Tuple pointing to the web elements to scrape from the website to used as dictionary values in each json entry. 

        '''
        
        self.json_data = []                                         # initialise list that all dictionary elements are appended to for saving to .json

        if type(main_page_links) == tuple:                               # check if links to get to next main pages are a tuple containing details to extract web elements
            extracted_next_page_links = self.get_data(main_page_links)   # extract the links into a list for interation to get next page
        else:
             extracted_next_page_links = main_page_links                 #otherwise leave links in a list

        if main_page_links != None and next_details_page != None :          # check if webpage is needing to iterate through details pages and main pages to be scraped
            for next_page_link in extracted_next_page_links:                # for loop to change pages after all details pages data has been received                
                self.driver.get(next_page_link)                             # move to the main page after finishing with details pages
                if scroll_page == True:                                     # check to see if the scroll parameter is active
                    self._load_web_data(page_wait_time)                     # run load webpage function to load all elements to be extracted on the page

                extracted_next_details_link = self.get_data(next_details_page) 
        
               #extract the detail pages using get_data function
                for next_page in extracted_next_details_link:                         # for loop to loop through all required details pages 
                    self.driver.get(next_page)                                        # use webdriver to get the next details page and switch there

                    #use the create_dictionary_list function to create a new dictionary from the required data on the webpage being scraped. This is then append 
                    #to the json_data list which will be used to finalise the required data to a .json file. 
                    self.json_data.extend(self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape ))
        


        elif main_page_links != None and next_details_page == None:  
            for next_details_link in extracted_next_page_links:
                self.driver.get(next_details_link)
                if scroll_page == True:                     # check if webpage needs to be scrolled to load all elements
                    self._load_web_data(page_wait_time)     # Use load_web_data function to load all elements on the page. 
                else:
                    pass
                
                # use the create_dictionary_list function to create a new dictionary from the required data on the webpage being scraped. This is then append 
                # to the json_data list which will be used to finalise the required data to a .json file. 
                self.json_data.extend(self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape ))
                        
        # run this if, if webpage does not need to iterate through main pages and details pages.
        elif main_page_links == None and next_details_page == None:  

            # use the create_dictionary_list function to create a new dictionary from the required data on the webpage being scraped. This is then append 
            # to the json_data list which will be used to finalise the required data to a .json file. 
            self.json_data.extend(self.create_dictionary_list(dict_keys, dict_cycle_keys, header_names, header_value, *data_to_scrape))

        # pool.close()
        # pool.join()        
        self._finalise_data(json_filename, 'a', self.json_data)                 # use finalise data function to finalise adding data to .json file
        self.driver.quit()                                                      # finally close driver to begin next webscrape



    def multi_linker(self):
   
        extracted_next_details_link = self.get_data(self.next_details_page)        # extract the detail pages using get_data function
        for next_page in extracted_next_details_link:                         # for loop to loop through all required details pages 
            self.driver.get(next_page)                                        # use webdriver to get the next details page and switch there


    def create_dictionary_list(self, dictionary_keys, dict_cycle : bool, head_name, head_val, *data_values):  
        '''
        Creates a dictionaries from extracted data with added functionality to cycle dictionary keys if required.

        Parameters:
        ------------------------------------
        dictionary_keys: A list of dictionary keys to add to the dictionary.

        dict_cycle: boolean to determine wether to cycle a list of dictionary keys

        head_name: string or tuple of string pointing to web elements to add to dictionary as header key.

        head_val: string or tuple of string pointing to web elements to add to dictionary as header value to associated key.

        *data_values = tuple of strings pointing to web elements containing data to add as values to the dictionary.

        Return
        ------------------------------------
        Returns a list of dictionaries 

        '''
        new_data = self.get_data(*data_values)
        self.temp_list = [] 
        for data in range(0, len(new_data), len(self.get_data(dictionary_keys))):
            if dict_cycle == True: 
                self.temp_list.append(self._save_data('d', self.get_data(head_name), self.get_data(head_val), self.get_data(dictionary_keys), new_data[data : data + (len(self.get_data(dictionary_keys))) ]))
            else:
                self.temp_list.append(self._save_data('d', self.get_data(head_name), self.get_data(head_val), self.get_data(dictionary_keys), new_data))
        
        return self.temp_list  


    def get_data_from_webelement_list(self, web_element_list : list, attri : str, attri_type: str) -> list:
        '''
        Extracts the required data of type specified from selenium webdriver elements.

        Parameters:
        ------------------------------------
        web_element_list: a list of web elements to extract the data from.

        attri: Specify wether to get text or an attribute from the element i.e choose get_attribute or text

        attri_type: Specify which attribute to get if attri = get_attribute i.e href, img etc.
        Passed to function in the format"('attri_type')" 

        Returns: A list of string elements extracted from the web elements
        '''
        self.list_name_output = []                                                              # temporary list to append extracted web elements to
        for web_element in web_element_list:                                                    # for each web element in the list of web elements
            if attri_type == None:                                                              
                self.list_name_output.append(getattr(web_element, attri))                       # get the attribute specified by attri, usually a test element
            else:
                self.list_name_output.append(getattr(web_element, attri)(eval(attri_type)))     # get the attribute specified by attri and attri type. 
        return self.list_name_output


    def get_data(self, data_location_tuple):
        '''
        Function to build string to pass to the webdriver to get required web elements from a webpage.

        Parameters:
        ------------------------------------
        data_location_tuple: A tuple of string containing the information of where to get web elements and what attributes of the data to extract.
        If a string is specified just return a string, usually used in the case of custom headers for dictionaries.

        Returns: Returns a list of data extracted from the web elements
        '''

        if isinstance(data_location_tuple, str) == True:                    # check to see if data_location_tuple is a string sometimes the case when specifiying a custom header
            return str(data_location_tuple)                                      # then return the string if this is the case
        else:
            (data_type, path, attribute, attribute_type) = data_location_tuple                 # unpack data location tuple into its attribute to build the evaluation string
            self.web_ele_statement = f"self.driver.find_elements_by_{data_type}('{path}')"     # Build evaluation string from unpacked data tuple 
            self.get_webelement = eval(self.web_ele_statement)                                 # evaluate string to get webelements from the webpage

            # pass the web elements and the required attributes to extract to the extract to the get_data_from_webelement_list function
            self.list_name = self.get_data_from_webelement_list(self.get_webelement, attribute, attribute_type)   

        return self.list_name 


    def _load_web_data(self, pause_time : float):
        '''
        Function to load web elements on a page before extracting

        Parameters:
        ------------------------
        pause_time: Time to wait while web elements load

        '''
        last_scroll_height = self.driver.execute_script("return document.body.scrollHeight")   
        while True:     
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")       # scroll to the bottom of the page
            
            sleep(pause_time)
             # page up twice to makes sure loadable elements are viewed so begin loading                                                                  # wait at the bottoms of page
            self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)               
            self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
            # wait while page elements load
            sleep(pause_time)
            # continue scrolling to the end of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       
            # get the new scroll height of the webpage
            new_scroll_height = self.driver.execute_script('return document.body.scrollHeight')

            #if the new height is equal to the previous height i.e no more element have loaded then exit the scroll while loop
            if new_scroll_height == last_scroll_height:
                break
            
            last_scroll_height = new_scroll_height


    def _save_data(self, save_type : str, 
                       header_names, 
                     header_values , 
                  *webelement_lists: list):
        '''
        Zips together dictionary or list data with header values to output

        Parameters:
        -------------------------
        save_type: Specify wether to save data in a dictionary or a list. 'd' = dictionary, 'l' = list.

        header_names: Header keys to append to the top of each list or dictionary. Can be a list or string.

        header_values: Values for the associated header_names. Can be a list or string

        webelements_lists: A list containing the web data that to be zipped together into a dictionary or list.

        Output
        -------------------------
        Return a list object or dictionary depeneding on which save_type is specified.
        '''

        if isinstance(header_names, list) or isinstance(header_values, list):  # check if header values or keys are in list format
            header_names = ','.join(header_names)                              # if they are then join header list keys and values for readability
            header_values = ','.join(header_values)

        if save_type == 'l':                                                   # update elements as a list
            self.json_output = list(zip(*webelement_lists))                     
        elif save_type == 'd':                                                 # update elements as a dictionay
            self.json_output = ({f"{header_names}" : f"{header_values}"})      # append header keys and values to the top of the dictionary
            self.json_output.update(dict(zip(*webelement_lists)))              # update the outfile with requried dictionaries
        
        return self.json_output

    
    def _finalise_data(self, json_filename :  str , add_mode : str, json_final_output):
        '''
        Finalises all json data and outputs it to json file

        Parameters:
        --------------------------
        json_filename: The json filename to output data to.

        add_mode: Parameter to specify the way in which you want to add data. 
        i.e 'a' = append, 'w' = write.

        json_final_output: List including the dictionaries to dump to the json file.
        '''
        self.json_filename = f'{json_filename}.json'                                
        with open(self.json_filename, add_mode, encoding='utf-8') as f:
             json.dump(json_final_output, f, ensure_ascii="false", indent=4)



# %%

from os import name
import json
from selenium import webdriver

def get_data_from_webelement_list(web_element_list : list, attri : str, attri_type: str) -> list:
        list_name_output = []
        for web_element in web_element_list:
            if attri_type == None:
                list_name_output.append(getattr(web_element, attri))
            else:
                list_name_output.append(getattr(web_element, attri)(eval(attri_type)))
        return list_name_output

def get_data(data_type : str,
                    path : str,  
               attribute : str,
          attribute_type : str) -> list:
    web_ele_statement = f"driver.find_elements_by_{data_type}('{path}')"
    get_webelement = eval(web_ele_statement)
    list_name = get_data_from_webelement_list(get_webelement, attribute, attribute_type)   
    return list_name 

def save_data(file_name : str, *webelement_lists: list):
    json_output = list(zip(*webelement_lists))
    json_filename = f'{file_name}.json'
    with open(json_filename, 'w') as f:
        json.dump(json_output, f, indent=4, ensure_ascii="False")




# %%

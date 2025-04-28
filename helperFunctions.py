import pickle
import os
import re


## Function to load cookies 
def load_cookies(driver):
    if os.path.isfile("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

## Function to save cookies 
def save_cookies(driver) :
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    

def remove_extra_spaces(text):
    text = ' '.join(text.split())
    return re.sub(r'\(.*?\)', '', text).strip()



# def remove_parentheses(text):
#     return 
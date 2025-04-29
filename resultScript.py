from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from helperFunctions import remove_extra_spaces, load_cookies, save_cookies
import pandas as pd

# setup for Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# creat dictionary to store the data
data = {'match_id': [],
    'Gameweek': [],
    'Date': [],
    'Time': [],
    'Result': [],
    'Home team': [],
    'Away team': []
}




if __name__ == "__main__":
    driver = setup_driver()
    try:
        startday = 1
        endday= 34
        season = 2015
        for s in range(season , 2025) :
            c= 0
            data = {'match_id': [],
                'Gameweek': [],
                'Date': [],
                'Time': [],
                'Result': [],
                'Home team': [],
                'Away team': []
            }
            for i in range(startday, endday+1):
                
                driver.get("https://www.transfermarkt.com/egyptian-premier-league/gesamtspielplan/wettbewerb/EGY1?saison_id=2024&spieltagVon=1&spieltagBis=1")
                load_cookies(driver)
                driver.get(rf"https://www.transfermarkt.com/egyptian-premier-league/gesamtspielplan/wettbewerb/EGY1?saison_id={s}&spieltagVon={i}&spieltagBis={i}")
                matches_table = driver.find_element(By.XPATH, "//th[contains(text(), 'Home team')]").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
                metadata = matches_table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")

                tbody = matches_table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                
                cuerrent_date = ''
                for row in rows:
                    lenth = len(row.find_elements(By.TAG_NAME, "td"))
                    if lenth == 1:
                        continue
                    else :
                        date = "".join(map(remove_extra_spaces,row.find_element(By.XPATH, ".//td[1]").get_attribute('textContent').split('\n')))
                        timeVar = "".join(map(remove_extra_spaces,row.find_element(By.XPATH, ".//td[2]").get_attribute('textContent').split('\n')))
                        result = "".join(map(remove_extra_spaces,row.find_element(By.XPATH, ".//td[5]").get_attribute('textContent').split('\n')))
                        home_team = "".join(map(remove_extra_spaces,row.find_element(By.XPATH, ".//td[3]").get_attribute('textContent').split('\n')))
                        away_team = "".join(map(remove_extra_spaces,row.find_element(By.XPATH, ".//td[7]").get_attribute('textContent').split('\n')))
                        
                        if not cuerrent_date:
                            cuerrent_date = date
                        if date != cuerrent_date and date :
                            cuerrent_date = date
                            data['Date'].append(cuerrent_date)
                            
                        else:
                            data['Date'].append(cuerrent_date)
                        
                        data['Time'].append(timeVar)
                        data['Result'].append(result)
                        data['Home team'].append(home_team)
                        data['Away team'].append(away_team)
                        data['Gameweek'].append(i)
                        data['match_id'].append(f"{s}{c}")
                        c+=1    
                
                
                
                
                
                df = pd.DataFrame(data) 
                print(df)
                df.to_excel(f'{s}-{s+1}_result.xlsx', index=False)
    finally:
        save_cookies(driver)
        driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# setup for Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")

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
        endday= 38
        season = 2014
        for s in range(season , 2015) :
            goalsDict = {'match_id': [],
                'GoalScorer': [],
                'OG': [],
                'Team': [],
                'Assist': [],
                'AssistType': [],
                'Penalty': [],
            }
            RefandStdium = {
                'MatchID': [],
                'Referee': [],
                'Stadium': []
            }
            c = 0
            for i in range(startday, endday+1):
                
                driver.get("https://www.transfermarkt.com/egyptian-premier-league/gesamtspielplan/wettbewerb/EGY1?saison_id=2024&spieltagVon=1&spieltagBis=1")
                driver.get(rf"https://www.transfermarkt.com/egyptian-premier-league/gesamtspielplan/wettbewerb/EGY1?saison_id={s}&spieltagVon={i}&spieltagBis={i}")
                matches_table = driver.find_element(By.XPATH, "//th[contains(text(), 'Home team')]").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
                metadata = matches_table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")

                tbody = matches_table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                games = dict()
                
                for row in rows:
                    lenth = len(row.find_elements(By.TAG_NAME, "td"))
                    if lenth == 1:
                        continue
                    else :
                        resultLink = row.find_element(By.XPATH, ".//td[5]").find_element(By.TAG_NAME ,'a').get_attribute('href')
                        
                        games[f"{season}{c}"]=  [resultLink ,row.find_element(By.XPATH, ".//td[5]").find_element(By.TAG_NAME ,'a').get_attribute('textContent').strip()]
                        c+=1 
                        print(resultLink)
                        
                        
                for k,v in games.items():
                    
                    try:
                        driver.get(v[0])
                        infoTable = driver.find_element(By.XPATH, "//p[@class='sb-zusatzinfos']").find_elements(By.TAG_NAME, "a")
                        RefandStdium['MatchID'].append(k)
                        try : 
                            RefandStdium['Stadium'].append(infoTable[0].get_attribute('textContent'))
                        except Exception as e:
                            RefandStdium['Stadium'].append('')
                            print(e)
                        try:
                            RefandStdium['Referee'].append(infoTable[1].get_attribute('textContent'))
                        except Exception as e:      
                            RefandStdium['Referee'].append('')
                            print(e)
                        
                    
                    except Exception as e:
                        print(e)

                    
                    if v[1] != '0:0':
                        try :
                            goals_list = driver.find_element(By.XPATH ,"//h2[contains(text(), 'Goals')]" ).find_element(By.XPATH , '..').find_element(By.ID, "sb-tore")
                            goals = goals_list.find_elements(By.TAG_NAME, "li")
                            for goal in goals:
                                if goal.get_attribute('class') == "sb-aktion-heim":
                                    team = "Home"
                                else :
                                    team = "Away"
                                print(team)
                                det = goal.find_element(By.CLASS_NAME, "sb-aktion-aktion")
                                names = det.find_elements(By.TAG_NAME, "a")
                                det_text = det.get_attribute('textContent')
                                if len(names) <= 1:
                                    assist = ''
                                    assistType = 'Unknown'
                                else : 
                                    assist = names[1].get_attribute('textContent').strip()
                                    ## Assist type
                                    if 'Without assist' in det_text:
                                        assistType = 'Without assist'
                                    elif 'Pass' in det_text.split('Assist:',1)[-1]:
                                        assistType = 'Pass'
                                    elif 'Cross' in det_text.split('Assist:',1)[-1]:
                                        assistType = 'Cross'
                                    elif 'Handball' in det_text.split('Assist:',1)[-1]:
                                        assistType = 'Handball '
                                    elif 'Penalty' in det_text.split('Assist:',1)[-1]:
                                        assistType = 'Penalty'
                                    elif 'Free kick' in det_text.split('Assis:')[-1]:   
                                        assistType = 'Free kick'
                                    elif 'Corner' in det_text.split('Assist:')[-1]:
                                        assistType = 'Corner'
                                    elif 'Throw-in' in det_text.split('Assist:')[-1]:
                                        assistType = 'Throw-in'
                                    elif 'Header' in det_text.split('Assist:')[-1]:
                                        assistType = 'Header'
                                    else :
                                        assistType = 'Unknown'
                                goalScorer = names[0].get_attribute('textContent').strip()
                                print(goalScorer)
                                
                                    
                                    
                                    
                                ## Penalty
                                if 'Penalty' in det_text:
                                    penalty = True
                                else:
                                    penalty = ''
                                    
                                    
                                ## OG
                                if 'Own-goal' in det_text:
                                    og = True
                                else:
                                    og = ''
                                
                                goalsDict['match_id'].append(k)
                                goalsDict['GoalScorer'].append(goalScorer)  
                                goalsDict['OG'].append(og)
                                goalsDict['Team'].append(team)
                                goalsDict['Assist'].append(assist)
                                goalsDict['AssistType'].append(assistType)
                                goalsDict['Penalty'].append(penalty)
                            
                        except Exception as e:
                            print(k)
                            print(e)
                            # print("No data")
                    
                    
                
                
                
                
                df = pd.DataFrame(goalsDict) 
                print(df)
                df.to_excel(f'{s}-{s+1}_goals.xlsx', index=False)
                df_2 = pd.DataFrame(RefandStdium)
                print(df_2) 
                df_2.to_excel(f'{s}-{s+1}_refstd.xlsx', index=False)
                
    finally:
        driver.quit()
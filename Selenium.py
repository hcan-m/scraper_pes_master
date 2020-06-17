# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:20:59 2020

@author: Huseyin Can Minareci
"""


from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os



start_time = time.time()

gecko_path = 'C:/Users/hcanm/Anaconda3/Lib/site-packages/geckodriver.exe'  # Please change the gecko_path where geckodriver.exe located



url = 'https://www.pesmaster.com'

options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options = options, executable_path = gecko_path)

driver.get(url)

time.sleep(1)

all_players = driver.find_element_by_xpath('//a[text()="All PES 2020 Players"]')
all_players.click()

time.sleep(2)

driver.find_element_by_xpath('//li[@title = "Remove"]').click() # for removing the myClub filter

time.sleep(2)

driver.find_element_by_xpath('//select[@data-name="Featured Players"]/option[text()="no"]').click() # for avoid having featured players in the list


path = os.getcwd() # for getting current path of .py folder for writing to csv

def scraper(p, names):    
    all_players = pd.DataFrame(columns=['Name', 'Nationality', 'Age', 'Height','Ovr', 'Pot','Pas','Shoot','Str','Def','Spd','Dri'])
    top_number = 100        # first how many players should be scraped per position
    l = 0                   # number of players
    k = 0                   # number of rows 
    page = 0                # current page
    while l < top_number:      
        k += 1
        if k % 25 == 0:                  # there are 30 players per page that's why after every 25 rows 
            page += 1                    # for reloading new players browser should go to end of page
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)     # sending END key to go at the end of the page
            time.sleep(1)                # waiting a second for data to appear
            print("Page = ",page)        # to know in which page scraper
            
        player = []             # creating empty list to add dataframe after scraping every row
        name = driver.find_element_by_xpath('//tbody/tr[{0}]/td[1]/a'.format(k)).text
        if name in names:       # for avoiding the scrap same player multiple times
            continue            # if the current player already exist it does not scrap and continue to next row
        else:
            names.append(name)  # adds name to the names lists
            player.append(name)
            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[3]/img'.format(k)).get_attribute("title"))

            player.append(driver.find_element_by_xpath('//div/div/table/tbody/tr[{0}]/td[4]'.format(k)).text)

            player.append(driver.find_element_by_xpath('//div/div/table/tbody/tr[{0}]/td[5]'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[7]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[8]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[9]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[10]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[11]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[12]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[13]/span'.format(k)).text)

            player.append(driver.find_element_by_xpath('//tbody/tr[{0}]/td[14]/span'.format(k)).text)
            
            l = l+1     # succesfull scraped player / increase l by one

        all_players.loc[k-1] = player       # adding player to data frame

# if you want to specify the path which scraped data would be written please comment-out next line     
    to_path = os.path.join(path,r'{0}.csv'.format(p))
#    to_path = "C:\\Users\\hcanm\\Desktop\\417121_Web_Scraping_Project\\Selenium\\{0}.csv".format(p)  # uncomment this line and change the path
    
    all_players.to_csv(to_path, index = False)    #writing players to csv
    
    print(p, "can be found at:",to_path)
# positions to scrap
positions = ("Goalkeeper", "Centre Back", "Left Back", "Right Back", "Defensive Midfielder",        
             "Centre Midfielder", "Left Midfielder", "Right Midfielder", "Attacking Midfielder",
             "Left Wing Forward", "Right Wing Forward", "Second Striker", "Centre Forward")

# loop for choosing every position seperately

for p in positions:
    print("Scrapping = ",p)     # to know in which position scraper is going to start
    driver.find_element_by_xpath('//select[@data-name="Main position"]/option[text()="{0}"]'.format(p)).click()
    time.sleep(1)
    names = []      # to erase names of previous position
    scraper(p, names)   # running the function


elapsed_time = time.time() - start_time         # for calculating how many time passed

print("Execution Time = ", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

driver.quit()

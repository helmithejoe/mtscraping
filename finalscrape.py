import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import csv


j = 0   #global variable for items counted

with open('source.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = []
    for row in csv_reader:
        #print(row)
        data.append(row)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
browser = webdriver.Chrome(options=options)

with open('target.csv','w') as file:
    file.write("Vessel name")
    file.write(",IMO")
    file.write(",MMSI")
    file.write(",Vessel Type")
    file.write(",Call Sign")
    file.write(",Flag")
    file.write(",Gross Tonnage")
    file.write(",Deadweight")
    file.write("\n")

for i in data:
    try:
        
        browser.get('https://www.marinetraffic.com/en/ais/index/search/all?keyword=' + str(i)[2:-2]) #goes to marinetraffic
        browser.maximize_window()
            
        soup=BeautifulSoup(browser.page_source,'lxml')
        numberofrecords = soup.findAll("strong")[5].string
        numberofrecords = numberofrecords.replace(',', '')
        numberofrecords = int(numberofrecords)
        numberofrecords = numberofrecords+1 #get number of records for vessels
        
        def data(): #get vessel data such as IMO number, MMSI number, latitude and longtitude
            
            soup=BeautifulSoup(browser.page_source,'lxml')

            with open('target.csv','a') as file:
                file.write("" + soup.findAll('b')[1].string)
                file.write("," + soup.findAll('b')[2].string)
                file.write("," + soup.findAll('b')[3].string)
                file.write("," + soup.findAll('b')[21].string)
                file.write("," + soup.findAll('b')[4].string)
                file.write("," + soup.findAll('b')[5].string)
                file.write("," + soup.findAll('b')[7].string)
                file.write("," + soup.findAll('b')[8].string) 
                file.write('\n')
             
        link = browser.find_element_by_xpath("(//a[@class='search_index_link'])[position()=1]")
        link.click()
        j = j+1
        print(j)
        data()        
            
        
        

    except (NoSuchElementException, IndexError):        #catch exceptions
        print("No such vessel name!")
        pass

browser.quit()

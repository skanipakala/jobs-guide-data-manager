#%% Launch Chrome

import time
  
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

  
# initializing webdriver for Chrome
driver = webdriver.Chrome()
  
# getting GeekForGeeks webpage
directoryURL = "https://identity.umd.edu/search"
driver.get(directoryURL)
  
driver.find_element(By.NAME, "login").click()
# sec = input('Press any key after you loggied in with CAS/Duo\n')
print("✅ Login click success")

input("Type data after DUO authentication")




queries = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

emailList = []
for query in queries:
    print("[!] Locating search textField")
    searchBox = driver.find_element(By.ID, "basicSearchInput")
    searchBox.clear()
    searchBox.send_keys(str(query))
    driver.find_element(By.NAME, "basicSearch").click()
    print("[!] Key send success")
    time.sleep(5)
    results= driver.find_element(By.CLASS_NAME,"SearchResults")
    data = str(results.get_attribute("innerHTML"))
    emailList.append({'query': query, 'html' : data})
    print("✅ query scrape sucess for " , query)
    # print("data ", data[1:100])


json_object = json.dumps(emailList, indent=4)
with open("a_z_scrape.json", "w") as outfile:
    outfile.write(json_object)

print("Review.json Write success ✅")


#%% ORGANIZE DATA
import re
import pandas as pd

print("running organize data...")
f = open('a_z_scrape.json')
scrapes = json.load(f)

giantList = []
for entry in scrapes:
    html = entry['html']
    print("\n✅ scanning", entry['query'])
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
    clean = list(set(emails))
    giantList = giantList + clean

df = pd.DataFrame(data=giantList, columns=['Emails'])
df.to_csv("email_scrape.csv")
print(df)
print("length of giantList ", len(giantList))
# print(giantList)
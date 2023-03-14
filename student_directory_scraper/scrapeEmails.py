# %% Launch Chrome

import pandas as pd
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import json


# Path to Chrome executable
chrome_executable_path = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

# Path to Chrome user data directory for the profile
chrome_user_data_dir = r'C:\\Users\\Sri\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1'

# Set Chrome options to use the specified user data directory and start with existing user profile
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_executable_path
chrome_options.add_argument('--user-data-dir=' + chrome_user_data_dir)
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--profile-directory=Profile 1')

# Launch Chrome with the specified options and user data directory
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a webpage
# driver.get('https://www.example.com')

# # %%
# # initializing webdriver for Chrome

# options = webdriver.ChromeOptions()
# # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
# options.add_argument(
#     r"--user-data-dir=C:\\Users\\Sri\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
# options.add_argument(r'--profile-directory=YourProfileDir')  # e.g. Profile 3

# options.add_argument('--profile-directory=UMD')
# driver = webdriver.Chrome(options=options)

# getting GeekForGeeks webpage
directoryURL = "https://identity.umd.edu/search"
driver.get(directoryURL)

driver.find_element(By.NAME, "login").click()
# sec = input('Press any key after you loggied in with CAS/Duo\n')
print("✅ Login click success")

input("Type data after DUO authentication")


queries = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

emailList = []
for query in queries:
    print("[!] Locating search textField")

    try:
        driver.find_element(By.CLASS_NAME, "collapsed").click()
    except Exception:
        print("Collpased click failure")

    searchBox = driver.find_element(By.ID, "advancedSearchInputs.firstName")
    searchBox.clear()
    searchBox.send_keys(str(query))
    driver.find_element(By.NAME, "advancedSearch").click()
    print("[!] Key send success")
    time.sleep(5)
    results = driver.find_element(By.CLASS_NAME, "SearchResults")
    data = str(results.get_attribute("innerHTML"))
    emailList.append({'query': query, 'html': data})
    print("✅ query scrape sucess for ", query)
    # print("data ", data[1:100])


json_object = json.dumps(emailList, indent=4)
with open("a_z_scrape.json", "w") as outfile:
    outfile.write(json_object)

print("Review.json Write success ✅")


# %% ORGANIZE DATA

print("running organize data...")
f = open('a_z_scrape.json')
scrapes = json.load(f)

giantList = []
for entry in scrapes:
    html = entry['html']
    print("\n✅ scanning", entry['query'])
    emails = re.findall(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', html)
    clean = list(set(emails))
    giantList = giantList + clean

df = pd.DataFrame(data=giantList, columns=['Emails'])
df.to_csv("email_scrape.csv")
print(df)
print("length of giantList ", len(giantList))
# print(giantList)

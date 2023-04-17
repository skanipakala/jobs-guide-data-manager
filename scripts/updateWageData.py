#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import numpy as np
import json
import pandas as pd


print("###############################################\n"
      "#                                             #\n"
      "#     Welcome to DBK Jobs Guide Data Manager  #\n"
      "#                                             #\n"
      "#              Version 1.1 (beta)             #\n"
      "#                                             #\n"
      "#        Developed by Sri Kanipakala          #\n"
      "#          (skanipakala@gmail.com)            #\n"
      "#                                             #\n"
      "###############################################")


# ⚠️ Please see ReadMe.md before attempting to modify code here! ⚠️
print("⚠️ Start year is fixed at 2018 ")
user_input = input(
    "Please enter END year after updating student_wages_tags.xlsx > ")
# Print the user's input

try:
    end_year = int(user_input)
    if len(user_input) != 4 or end_year < 0:
        print("❌ Invalid year format")
        sys.exit(0)
    else:
        print("✅ Selected year range 2018 - ", end_year)
except ValueError:
    print("❌ Invalid year format")
    sys.exit(0)

# If adding another year, append to this array here
# years = list(range(2018, end_year + 1))
years = [str(year) for year in range(2018, end_year + 1)]
print("YearList = ", years)
years.append("2022")
print("⚠️ Reference year (2022) selected by default. ⚠️\n\n")

# years = ['2018', '2019', '2020', '2021', '2022']

years = list(set(years))
# Cleaned up years

masterDict = dict()
for curYear in years:
    print("Parsing year...", curYear)
    df = pd.read_excel('../imports/student_wages_tags.xlsx',
                       sheet_name=curYear)
    print("✅ Excel read success for year ", curYear)

    emptyTagsOk = False
    if 'tags' not in df.columns:
        print("Column 'name' exists!")
        print("Missing 'tags' column in Excel for year ", curYear)
        ignore_tags = input("Continue without adding tags for year {}? YES/NO\n>>".format(curYear))

        if "N" in ignore_tags.upper():
            print("Add a tags column for year {} and run program again".format(curYear))
            print("Quitting DataManager Program....")
            sys.exit()
        elif "Y" in ignore_tags.upper():
            print("[Override] Continuing with empty tags for current year {}".format(curYear)) 
            emptyTagsOk = True
             


    masterList = []
    for index, row in df.iterrows():
        workgp = row['Workgroup']
        if workgp == np.nan or pd.isnull(workgp) or "EMPTY" in str(workgp).upper():
            workgp = ""

        edu = row['Category Status']
        if edu == "Undergraduate Student":
            edu = "undergraduate"
        else:
            edu = "graduate"

        unitSplit = str(row['Unit']).split("-")
        
        tagList = []

        try:
            tag = row['tags']

            if tag == np.nan or pd.isnull(tag) or "EMPTY" in str(tag).upper():
                tag = ""
                tagList = []
            else:
                tag = str(tag)
                for t in tag.split(","):
                    tagList.append(t.strip())
        except:
            if emptyTagsOk == True:
                tagList = []
            else:
                print("ISSUE WITH READING TAGS...Exiting")
                sys.exit()
            

        obj = {
            'education': edu,
            'wage': row['Hour Rate'],
            'unit': unitSplit[1],
            'workgroup': workgp,
            'department': unitSplit[0],
            'year': curYear,
            'tags': tagList
        }

        masterList.append(obj)

    masterDict[curYear] = masterList

# Serializing json
json_object = json.dumps(masterDict, indent=4)

# Writing to sample.json
with open("../exports/sample_year.json", "w") as outfile:
    outfile.write(json_object)

print("✅ sample_year.json -> write success")


# In[ ]:


import json
f = open('../exports/sample_year.json')
data = json.load(f)

# Data structures

set_department = set()
set_unit = set()
set_workgroup = set()

for end_year in years:

    print("Updating metaData for year...", end_year)
    
    for entry in data[end_year]:
        set_department.add(entry['department'].strip())
        set_unit.add(entry['unit'].strip())
        set_workgroup.add(entry['workgroup'].strip())


# set_department.remove("")
# set_unit.remove("")
set_workgroup.remove("")

export = dict()


export['unique_department'] = list(set_department)
export['unique_unit'] = list(set_unit)
export['unique_workgroup'] = list(set_workgroup)
export['unique_years'] = list(data.keys())

export['unique_department'].sort()
export['unique_unit'].sort()
export['unique_workgroup'].sort()
export['unique_years'].sort()

# Serializing json
json_object = json.dumps(export, indent=4)
 
# Writing to sample.json
with open("../exports/sample_metadata.json", "w") as outfile:
    outfile.write(json_object)

print("✅ sample_metadata.json -> write success")


# In[ ]:


print("Analyzing filters for unitToWorkgroup.json")

# Data structures
unitToWorkgroup = dict()

for unit in export['unique_unit']:
    unitToWorkgroup[unit] = set()

for entry in data['2022']:   
    unitToWorkgroup[entry['unit']].add(entry['workgroup'])

# print(unitToWorkgroup)


for unit in unitToWorkgroup.keys():
    unitToWorkgroup[unit] = list(unitToWorkgroup[unit])
    unitToWorkgroup[unit].sort()

json_object = json.dumps(unitToWorkgroup, indent=4)

# Writing to sample.json
with open("../exports/unitToWorkgroup.json", "w") as outfile:
    outfile.write(json_object)

print("✅ unitToWorkgroup.json -> write success")


# In[ ]:


print("Analyzing filters for departmentToUnit.json")

departmentToUnit = dict()

for dept in export['unique_department']:
    departmentToUnit[dept] = set()

for entry in data['2022']:   
    departmentToUnit[entry['department']].add(entry['unit'])

# print(unitToWorkgroup)


for dept in departmentToUnit.keys():
    departmentToUnit[dept] = list(departmentToUnit[dept])
    departmentToUnit[dept].sort()

json_object = json.dumps(departmentToUnit, indent=4)

# Writing to sample.json
with open("../exports/departmentToUnit.json", "w") as outfile:
    outfile.write(json_object)

print("✅ departmentToUnit.json -> write success")


# In[ ]:


import os
import json
from firebase_admin import credentials, storage
import firebase_admin
from os.path import join, dirname, abspath


# Prompt user for credentials file until a valid .json file is provided
while True:
    credentials_file = input("Enter the path to your Firebase credentials .json file: ")
    if credentials_file.endswith(".json") and os.path.isfile(credentials_file):
        break
    print("Invalid file. Please provide a valid .json file.")

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate(credentials_file)


firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'dbk-salary-guide.appspot.com'
},
)


bucket = storage.bucket()

# Loop through all files in a directory and upload only .json files to Firebase storage

dir_path = input("Enter directory path of .json files: \nDefault path is ../exports/ if running inside scripts folder\n>>")
for filename in os.listdir(dir_path):
    if filename.endswith(".json"):
        file_path = join(dir_path, filename)
        with open(file_path, 'rb') as file:
            blob = bucket.blob(filename)
            blob.upload_from_file(file)
            print(f"🔃 {filename} uploaded to Firebase storage.")

print("ALL TASKS COMPLETED 😀 (please exit now)")


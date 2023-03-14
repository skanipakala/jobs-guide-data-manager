# ReadMe for Jobs Guide App


## About the Data 📊

- The Flutter app (jobs.dbknews.com) reads the jobs guide data from `.json` files
- Here's what each file means.

| Exported File  | What it does |
| ------------- | ------------- |
| `sample_metadata.json`  | Contains all data about all unqiue, departments, units, and workgroups   |
| `sample_year.json`  | Actual wage data segregated by years (2018-latest). This is main source of data for jobs guide   |
| `departmentToUnit.json`  | Complementary file to help quick lookups of all the units within a specific department. These are used to help update the __unit dropdown filter__ with only the necessary units when a department filter is set.   |
| `unitToWorkgroup.json`  | Similar to `departmentToUnit.json` but this file helps for quick lookups of all workgroups with a specific unit. These are used to help update the __workgroup dropdown filter__ with only the necessary workgroups when a unit filter is set.  |
| `unit_reviews.json`  | List of reviews for each unit. Contains min/max wages, reported wage, job title, and review description   |

## Updating Wage Data 💰
- These are steps to update the data for a new year (i.e 2023 data)

### Generating new `.json` files with new excel data
1. Acquire the new year data via FOIA request
2. Navigate to `/imports` folder and add open the `student_wages_tags.xlsx` file
3. You should see sheets for different years from 2018 - 2022 data.
4. Copy your data into a new sheet called `2023` or whatever your year is and save + close Excel
5. Navigate to `/scripts` folder
6. Append your year `2023` to the `years` array. 
    - Should look like this --> `years = ['2018', '2019', '2020', '2021', '2022', '2023']`
7. To install all the depencies run. Ensure you have python installed first.
```
pip install -r requirements.txt
```
8. Now run the file `updateWageData.py` with the command
 ```
 python updateWageData.py
 ```
9. This will re-create all wage data related `.json` files and store them in `/exports` folder.
    - ⚠️  `unit_reviews.json` will not be updated. You must run `python updateReviews.py` for this


## Updating Review Data 💬
- Follow these steps to update student reviews
1. Download the latest review data from this google sheet. Make sure to check the sheet called `cleaned`
2. Navigate to `/scripts/`
3. Copy your updated excel file, replacing `responses.xlsx` (keep the file name the same)
4. Run the python script to generate `unit_reviews.json` inside the `/exports` folder
```
python updateReviews.py
```
5. Entries in the `unit_reviews.json` should be in the following structure:
```json
{"A. James Clark School of Engineering": {
        "wage_range": {
            "min": 9.25,
            "max": 15.0
        },
        "reviews": [
            {
                "job_title": "Instructional Fabrication Lab Technician",
                "hourly_rate": "17.0",
                "review": "Fun, educational, useful in industry, flexible",
                "timestamp": "2023-02-09 13:17:40.950000"
            },
            {
                "job_title": "Peer Assistant",
                "hourly_rate": "15.0",
                "review": "I thoroughly enjoy my job and responsibilities",
                "timestamp": "2023-02-13 11:35:06.959000"
            }
        ]
    }
}
```


### Updating files in Flutter app 📂
10. Ensure you have Flutter installed on your PC. Follow instructions here: https://docs.flutter.dev/get-started/install

11. Next clone the latest version of jobs guide app from repo
    ```    
    git clone https://github.com/skanipakala/dbk_jobs_guide.git
    ```

12. Copy the updated `.json` files and paste it inside the `assets/data/` folder in the flutter app directory you just cloned. Follow the next step to actually deploy the app with new data

### Deploying Flutter web app with changes 🚀
13. Ensure you have Firebase CLI installed. If not, follow steps here: https://firebase.google.com/docs/cli#windows-npm
    - You can install Firebase CLI via npm. (You must have Node installed first)
    ```    
    npm install -g firebase-tools
    ```
14. Please log in to gain access to Firebase backend so you can push changes via CLI 
    ```    
    firebase login
    ```
    This will open your browser. Log into Google with dbklab credentials. You can redirect back after this.

15. Next, run `flutter build web` need to re-build the flutter app. This may take a while as it compiles `.dart` code to HTML/JS
```
flutter build web
``` 
16. Next run `firebase deploy` inside the flutter app directory and it should deploy new version to `jobs.dbknews.com` automatically with the latest data.
```
firebase deploy
```

17. You can check the latest deployed version via the Firebase Console here:
-  https://console.firebase.google.com/u/0/project/dbk-salary-guide/hosting/sites
- Make sure you are logged into google with the DBK Lab account

### ✉️ contact skanipakala@gmail.com  (301)-529-6291 if you have any questions 😀
# ReadMe for Jobs Guide App

## About the Data 📊

- The Flutter app (jobs.dbknews.com) reads the jobs guide data from `.json` files
- Here's what each file means.

| Exported File           | What it does                                                                                                                                                                                                                                   |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sample_metadata.json`  | Contains all data about all unqiue, departments, units, and workgroups                                                                                                                                                                         |
| `sample_year.json`      | Actual wage data segregated by years (2018-latest). This is main source of data for jobs guide                                                                                                                                                 |
| `departmentToUnit.json` | Complementary file to help quick lookups of all the units within a specific department. These are used to help update the **unit dropdown filter** with only the necessary units when a department filter is set.                              |
| `unitToWorkgroup.json`  | Similar to `departmentToUnit.json` but this file helps for quick lookups of all workgroups with a specific unit. These are used to help update the **workgroup dropdown filter** with only the necessary workgroups when a unit filter is set. |
| `unit_reviews.json`     | List of reviews for each unit. Contains min/max wages, reported wage, job title, and review description                                                                                                                                        |

## Updating Wage Data 💰

- These are steps to update the data for a new year (i.e 2023 data)

### Easiest way to update wage data & sync to Firebase 👈🏻

1. Make sure you add the new data to Excel file called `student_wages_tags.xlsx` in the `scripts/` folder. Each years data is a new "sheet", shown at the bottom of the Excel. Must be titled in correct year format like "2018", "2049"
2. Clone this repo
3. Make sure you have downloaded the `JOBS_GUIDE_KEY.json` file (check Dev slack or contact me)
4. Run `updateWageData.py` and follow on-screen instructions

```
pip install -r requirements.txt
```

Now run the file `updateWageData.py` with the below command. This will generate .json files from excel and also auto-upload them to Firebase storage all in one go.

> Follow on-screen instructions after running updateWageData.py

```
python updateWageData.py
```

> That's it! Visit https://jobs.dbknews.com/ to see changes after it propagates ✅

---

### Manually update data (Slow and for emergencies)

1. Acquire the new year data via FOIA request
2. Navigate to `/imports` folder and add open the `student_wages_tags.xlsx` file
3. You should see sheets for different years from 2018 - 2022 data.
4. Copy your data into a new sheet called `2023` or whatever your year is and save + close Excel
5. Navigate to `/scripts` folder
6. Append your year `2023` to the `years` array.
   - Should look like this --> `years = ['2018', '2019', '2020', '2021', '2022', '2023]`
7. To install all the depencies run.
8. Run all cells inside .ipynb

## Updating Review Data (in-progress) 🗣️

- Follow these steps to update student reviews

1. Download the latest review data from this google sheet. Make sure to check the sheet called `cleaned`
2. Navigate to `/scripts/`
3. Copy your updated excel file, replacing `responses.xlsx` (keep the file name the same)
4. Run the python script to generate `unit_reviews.json` inside the `/exports` folder

```
python updateReviews.py
```

5. ⚠️ Changes won't show on website until you sync them to the flutter web app (see instructions below)
6. Entries in the `unit_reviews.json` should be in the following structure:

```json
{
  "A. James Clark School of Engineering": {
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

### Manually syncing new wage/review data to Flutter app 📂

1. Ensure you have Flutter installed on your PC. Follow instructions here: https://docs.flutter.dev/get-started/install

2. Next clone the latest version of jobs guide app from repo

   ```
   git clone https://github.com/skanipakala/dbk_jobs_guide.git
   ```

3. Copy the updated `.json` files and paste it inside the `assets/data/` folder in the flutter app directory you just cloned. Follow the next step to actually deploy the app with new data

### Manually deploy Flutter Web app 🚀

1. Ensure you have Firebase CLI installed. If not, follow steps here: https://firebase.google.com/docs/cli#windows-npm
   - You can install Firebase CLI via npm. (You must have Node installed first)
   ```
   npm install -g firebase-tools
   ```
2. Please log in to gain access to Firebase backend so you can push changes via CLI

   ```
   firebase login
   ```

   This will open your browser. Log into Google with dbklab credentials. You can redirect back after this.

3. Next, run `flutter build web` need to re-build the flutter app. This may take a while as it compiles `.dart` code to HTML/JS

```
flutter build web
```

4. Next run `firebase deploy` inside the flutter app directory and it should deploy new version to `jobs.dbknews.com` automatically with the latest data.

```
firebase deploy
```

5. You can check the latest deployed version via the Firebase Console here:

- https://console.firebase.google.com/u/0/project/dbk-salary-guide/hosting/sites
- Make sure you are logged into google with the DBK Lab account

### ✉️ contact skanipakala@gmail.com (301)-529-6291 if you have any questions 😀

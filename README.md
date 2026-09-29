# RBSK Portal Student Automation Bot

## Overview
This project is a Python-based browser automation suite designed to bulk-add students into the **Rashtriya Bal Swasthya Karyakram (RBSK)** government health portal. 

Since the portal requires manual login (CAPTCHA) and uses complex React-based forms with significant latency, this automation is built to attach to an **already-open Chrome browser**. This allows the user to log in manually, select the correct school, and then hand over control to the bot to perform the repetitive data entry from an Excel sheet.

## The Goal & Context
The user (a data entry operator or coordinator) is given Excel sheets containing student information (Names, DOB, Parents' Names, Mobile Numbers, Classes) for various schools (e.g., GMS KATKAI, GPS KUNJPURA). 
The manual process of entering these students one-by-one is incredibly tedious because:
1. The portal is slow and requires waiting between clicks.
2. The UI has unexpected modals (e.g., a "Plan Completed" popup every time a new student is added).
3. The Date of Birth (DOB) picker is notoriously difficult to interact with manually or via standard automation.
4. Mobile numbers are sometimes missing in the Excel sheet, requiring a fallback to existing valid numbers from the sheet.

**What the bot needs to do:**
Read the Excel sheet, clean the data, intelligently cycle through valid mobile numbers if one is missing, navigate the RBSK portal, handle popup modals, inject data directly into React's state, and submit the forms carefully with built-in delays to avoid crashing the government servers.

---

## Technical Approach & Challenges Solved

### 1. Bypassing Login & CAPTCHA (Chrome CDP)
Instead of using Selenium or Playwright to open a fresh browser (which would require logging in and solving CAPTCHAs every time), the bot connects to an existing Chrome session using the **Chrome DevTools Protocol (CDP)** on port `9222`.

### 2. React State Updates (`dispatchEvent`)
The RBSK portal is built with React. Simply setting the `value` of an input field via automation does not trigger React's internal state update, causing the form to submit as blank. The bot solves this by injecting a custom JavaScript function into the browser that sets the native value and manually dispatches `input`, `change`, and `blur` events so React recognizes the text.

### 3. The Date of Birth (DOB) Datepicker
Standard `.fill()` commands fail on the custom datepicker. The bot solves this by clicking the input field and using raw keyboard automation (`page.keyboard.type('DDMMYYYY')` followed by `Tab`) to reliably enter the date.

### 4. Handling Intermittent Modals
After saving a student, clicking "+ Add New Student" triggers a "Plan Completed" modal. The bot contains explicit waits and DOM queries to detect the "Yes, proceed!" button and the "Without ABHA" selection to clear these hurdles automatically.

### 5. Missing Data Handling (Mobile Numbers)
The portal requires a 10-digit mobile number, but the Excel sheets often have blank cells. The bot dynamically extracts all valid mobile numbers from the Excel sheet and cycles through them sequentially whenever it encounters a student without a mobile number.

### 6. Cross-Referencing Lists
The bot also includes logic to scrape the currently added students from the portal's HTML table and cross-reference them against the master Excel sheet. This ensures that if the process is interrupted, the bot can accurately identify and only upload the *missing* students.

---

## How to Run the Automation

### Step 1: Launch Chrome with Debugging
Close all existing Chrome windows, open your terminal, and launch Chrome with the remote debugging port open:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
```

### Step 2: Manual Setup
1. In the newly opened Chrome window, navigate to the RBSK Portal.
2. Log in with your credentials (e.g., `MHT-106256`).
3. Solve the CAPTCHA.
4. Navigate to the specific school's "Student List" page.

### Step 3: Prepare the Data
Ensure your Excel file is in the project directory (e.g., `StudentListingReport (24).xlsx` or your specific school's sheet). If cross-referencing, ensure the script is pointing to the correct Excel file and School Name.

### Step 4: Run the Bot
Activate the virtual environment and run the desired script:
```bash
source venv/bin/activate

# To run a specific batch of students:
python3 run_remaining_class_6.py

# Or to cross-reference and add missing students:
python3 add_missing_students.py
```

The bot will print its progress to the console, take screenshots of the filled forms before saving, and wait appropriate amounts of time (15 seconds after saving, 8 seconds after returning to the list) to ensure the portal registers the data successfully.

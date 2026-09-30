# RBSK Portal & ABHA Automation Bot

## Overview
This project is a Python-based browser automation suite designed to perform tedious data entry and verification tasks on the **Rashtriya Bal Swasthya Karyakram (RBSK)** government health portal. 

It handles two primary workflows:
1. **Bulk Student Addition:** Adding new students from Excel sheets into the portal.
2. **ABHA (Ayushman Bharat Health Account) Linking Bot:** Automatically scanning the portal for students, fetching their Aadhaar data from an Excel/Numbers sheet, and generating/linking their ABHA ID in the portal using the "Green Heart" workflow.

Since the portal requires manual login (CAPTCHA) and uses complex React-based forms with significant latency, this automation connects to an **already-open Chrome browser**. This allows you to log in manually and select the correct page, and then hand over control to the bot.

## 1. The ABHA Bot (Green Heart Process)

### The Goal
Once students are uploaded, the portal requires generating and linking an ABHA ID for each student by clicking a "Heart" icon next to their name. 
The manual process involves:
1. Identifying unprocessed students (green heart icon).
2. Clicking the icon to open a modal.
3. Switching tabs to "Using Aadhaar Demographic".
4. Finding the student's exact Aadhaar Number and Mobile Number from an Excel file (resolving duplicate names by cross-referencing parents' names).
5. Filling the form and acknowledging consent boxes.
6. Waiting for the government server to generate the ABHA (which can take a long time).
7. Navigating through multiple profile linking screens ("View & Link Profile" -> "Confirm & Link with RBSK ID").
8. Waiting for the green success toast before closing the modal.

### How to Run the ABHA Bot
1. **Prepare Data:** Save your `.numbers` file as `students_data.csv` using the provided `read_numbers.py` script. The bot reads this CSV to find the Aadhaar numbers and Mobile numbers.
2. **Setup Browser:** Navigate to the school's student list on the RBSK portal in the debugged Chrome window.
3. **Run the Script:**
   ```bash
   source venv/bin/activate
   python3 abha_bot.py
   ```
4. **Behavior:** The script will automatically scan the page for any green heart icons (unprocessed students). It will match the name and parents' names against `students_data.csv`. It dynamically handles loading times, waiting up to 45 seconds for government servers to process the ABHA links, and ensures the profile is successfully linked before closing the modal and moving to the next row. It automatically skips missing data or mismatched profiles.

## 2. Bulk Student Addition

### The Goal
Read Excel sheets containing student information and manually input them into the portal's "Add New Student" form. It intelligently cycles through valid mobile numbers if one is missing, navigates popups, and injects data directly into React's state.

### How to Run
```bash
source venv/bin/activate
python3 add_missing_students.py
```

---

## Technical Approach & Challenges Solved

### 1. Bypassing Login & CAPTCHA (Chrome CDP)
Instead of opening a fresh browser (which requires logging in and solving CAPTCHAs), the bot connects to an existing Chrome session using the **Chrome DevTools Protocol (CDP)** on port `9222`.

### 2. React State Updates (`dispatchEvent`)
The RBSK portal is built with React. Simply setting the `value` of an input field via automation does not trigger React's internal state update. The bot injects custom JavaScript to set the native value and manually dispatches `input`, `change`, and `blur` events.

### 3. Dynamic Latency & Government Servers
The ABHA generation API is notoriously slow. The bot employs smart polling loops to wait for specific UI elements (like the "Confirm & Link" button enabling or a success toast appearing) rather than hardcoded sleeps, ensuring it doesn't fail on slow connections but doesn't waste time on fast ones.

### 4. Smart Duplicate Name Resolution
When searching the Excel sheet for an Aadhaar number, the bot handles duplicate names (e.g., two students named "Nancy") by cross-referencing both the Father's Name and Mother's Name from the portal against the Excel data.

### 5. Missing Data Handling (Mobile Fallbacks)
The portal requires a 10-digit mobile number. For both workflows, if a mobile number is missing, the bot dynamically tracks and limits the reuse of other valid mobile numbers from the sheet (up to 5 times) to bypass the form constraints safely.

## Launching Chrome for the Bot
Close all existing Chrome windows, open your terminal, and launch Chrome with the remote debugging port open:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"
```

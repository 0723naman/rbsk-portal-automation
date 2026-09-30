from playwright.sync_api import sync_playwright
import time
import csv

def read_data():
    with open('students_data.csv', 'r') as f:
        lines = f.readlines()
    
    data = []
    reader = csv.reader(lines[2:])
    for row in reader:
        if len(row) > 30:
            name = row[11].strip().upper()
            father = row[23].strip().upper()
            mother = row[31].strip().upper()
            aadhaar = row[15].strip()
            mobile = row[32].strip()
            if mobile.endswith('.0'):
                mobile = mobile[:-2]
            
            data.append({
                'name': name,
                'father': father,
                'mother': mother,
                'aadhaar': aadhaar,
                'mobile': mobile
            })
    return data

def main():
    print("Reading Excel data...")
    excel_data = read_data()
    
    # Initialize fallback mobile usage tracker
    mobile_usage = {}
    
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            # Close any dangling modals before starting
            page.evaluate('''() => {
                let closeBtn = document.querySelector('button.close, .modal-close');
                if (!closeBtn) {
                    let btns = Array.from(document.querySelectorAll('button'));
                    closeBtn = btns.find(b => b.innerText && b.innerText.toLowerCase().trim() === 'close');
                }
                if (closeBtn) closeBtn.click();
                else {
                    let svgs = Array.from(document.querySelectorAll('svg'));
                    let closeSvg = svgs.find(s => s.parentElement && s.parentElement.tagName === 'BUTTON' && s.innerHTML.includes('M6 18L18 6M6 6l12 12'));
                    if (closeSvg) closeSvg.parentElement.click();
                }
            }''')
            time.sleep(1)
            
            processed_indices = []
            
            # Re-fetch rows in a loop so we get fresh elements
            while True:
                print("Scanning for next unprocessed student on page...")
                
                # We do this one by one so DOM updates don't break our references
                target_row_index = page.evaluate('''(processed) => {
                    let rows = Array.from(document.querySelectorAll("table tbody tr"));
                    for (let i = 0; i < rows.length; i++) {
                        if (processed.includes(i)) continue;
                        let btn = rows[i].querySelector('button[title="Create or Link ABHA"]');
                        if (btn && !btn.disabled) {
                            return i;
                        }
                    }
                    return -1;
                }''', processed_indices)
                
                if target_row_index == -1:
                    print("No more unprocessed students found on this page!")
                    break
                
                processed_indices.append(target_row_index)
                
                # Get details of the target row
                row_data = page.evaluate(f'''(rowIndex) => {{
                    let r = document.querySelectorAll("table tbody tr")[rowIndex];
                    let cols = Array.from(r.querySelectorAll("td"));
                    return {{
                        name: cols[2].innerText.trim(),
                        father: cols[7].innerText.trim(),
                        mother: cols[8].innerText.trim()
                    }};
                }}''', target_row_index)
                
                print(f"\\n--- Processing Student: {row_data['name']} (Row {target_row_index + 1}) ---")
                
                # Match in excel
                matches = [s for s in excel_data if s['name'] == row_data['name'].upper()]
                if len(matches) > 1:
                    better = [s for s in matches if s['father'] == row_data['father'].upper() and s['mother'] == row_data['mother'].upper()]
                    if better:
                        matches = better
                    else:
                        matches = [s for s in matches if s['father'] == row_data['father'].upper() or s['mother'] == row_data['mother'].upper()]
                
                if len(matches) == 0:
                    print(f"Could not find matching data in Excel for {row_data['name']}. Skipping...")
                    # We need to mark it as skipped or the loop will get stuck forever!
                    # We can just inject a disabled attribute so it ignores it next time.
                    page.evaluate(f'''(rowIndex) => {{
                        let r = document.querySelectorAll("table tbody tr")[rowIndex];
                        let btn = r.querySelector('button[title="Create or Link ABHA"]');
                        if (btn) btn.disabled = true;
                    }}''', target_row_index)
                    continue
                
                target_student = matches[0]
                print(f"Found Excel Data -> Aadhaar: {target_student['aadhaar']}, Mobile: {target_student['mobile']}")
                
                if not target_student['aadhaar']:
                    print("No Aadhaar number in Excel. Skipping...")
                    page.evaluate(f'''(rowIndex) => {{
                        let r = document.querySelectorAll("table tbody tr")[rowIndex];
                        let btn = r.querySelector('button[title="Create or Link ABHA"]');
                        if (btn) btn.disabled = true;
                    }}''', target_row_index)
                    continue

                # Determine which mobile number to use
                mobile_to_use = target_student['mobile']
                if not mobile_to_use:
                    # Find a fallback mobile
                    for s in excel_data:
                        m = s['mobile']
                        if m and mobile_usage.get(m, 0) < 5:
                            mobile_to_use = m
                            mobile_usage[m] = mobile_usage.get(m, 0) + 1
                            print(f"Using fallback mobile: {mobile_to_use}")
                            break

                # 1. Click Heart icon
                print("1. Clicking 'Create or Link ABHA' Heart icon...")
                page.evaluate(f'''(rowIndex) => {{
                    let btn = document.querySelectorAll("table tbody tr")[rowIndex].querySelector('button[title="Create or Link ABHA"]');
                    if (btn) btn.click();
                }}''', target_row_index)
                time.sleep(4)
                
                # 2. Click Using Aadhaar Demographic
                print("2. Switching to 'Using Aadhaar Demographic'...")
                page.evaluate('''() => {
                    let label = document.querySelector('label[for="byAadhaarDemographic"]');
                    if (label) label.click();
                }''')
                time.sleep(3)
                
                # 3. Ensure checkboxes are checked
                print("3. Checking consent boxes...")
                page.evaluate('''() => {
                    let checkboxes = document.querySelectorAll('input[type="checkbox"]');
                    checkboxes.forEach(cb => {
                        if (!cb.checked) {
                            cb.click();
                        }
                    });
                }''')
                time.sleep(2)
                
                # 4. Click PROCEED
                print("4. Clicking 'PROCEED'...")
                page.evaluate('''() => {
                    let btns = Array.from(document.querySelectorAll('button'));
                    let proceedBtn = btns.find(b => b.innerText.trim() === 'PROCEED');
                    if (proceedBtn) proceedBtn.click();
                }''')
                time.sleep(4)
                
                # 5. Fill Data
                print("5. Filling Aadhaar and Mobile Number...")
                page.evaluate(f'''(data) => {{
                    const triggerChange = (el) => {{
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }};
                    const setNativeValue = (el, val) => {{
                        const proto = window.HTMLInputElement.prototype;
                        const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
                        setter.call(el, val);
                        triggerChange(el);
                    }};

                    let inputs = Array.from(document.querySelectorAll("input"));
                    let aadhaarInput = inputs.find(i => i.placeholder && i.placeholder.includes('xxxx')); 
                    if (!aadhaarInput) aadhaarInput = document.querySelector('input[name="aadhaarNumber"], input[name="aadhaar"]');
                    if (aadhaarInput && data.aadhaar) {{
                        setNativeValue(aadhaarInput, data.aadhaar);
                    }}

                    let mobileInput = inputs.find(i => i.placeholder && i.placeholder.includes('10-digit'));
                    if (!mobileInput) mobileInput = document.querySelector('input[name="mobileNumber"], input[name="mobile"]');
                    if (mobileInput) {{
                        if (!mobileInput.value || mobileInput.value.trim() === '') {{
                            if (data.mobile) {{
                                setNativeValue(mobileInput, data.mobile);
                            }}
                        }}
                    }}
                }}''', {'aadhaar': target_student['aadhaar'], 'mobile': mobile_to_use})
                time.sleep(3)
                
                # 6. Click Create ABHA
                print("6. Clicking 'Create ABHA'...")
                page.evaluate('''() => {
                    let btns = Array.from(document.querySelectorAll('button'));
                    let createBtns = btns.filter(b => b.innerText && b.innerText.trim() === 'Create ABHA');
                    if (createBtns.length > 0) {
                        let btn = createBtns[createBtns.length - 1];
                        btn.scrollIntoView();
                        btn.click();
                    }
                }''')
                # Wait longer for Govt site processing
                time.sleep(10)
                
                # 7. Wait and Click View & Link Profile
                print("7. Waiting for 'View & Link Profile' button...")
                link_success = False
                for _ in range(25):  # Wait up to 25 seconds for Govt site
                    btn_state = page.evaluate('''() => {
                        let btns = Array.from(document.querySelectorAll('button'));
                        let linkBtn = btns.find(b => b.innerText && b.innerText.includes('View & Link Profile'));
                        if (linkBtn) {
                            linkBtn.click();
                            return true;
                        }
                        return false;
                    }''')
                    if btn_state:
                        link_success = True
                        break
                    time.sleep(1)
                
                if not link_success:
                    print("Timed out waiting for 'View & Link Profile'. Closing modal...")
                    # If we couldn't even generate the ABHA, we just close and move on.
                else:
                    time.sleep(3)
                    # 8. Wait for Confirm & Link to become enabled and click
                    print("8. Waiting for Profile Match Analysis and clicking 'Confirm & Link with RBSK ID'...")
                    success = False
                    for _ in range(45):  # Wait up to 45 seconds
                        btn_state = page.evaluate('''() => {
                            let btns = Array.from(document.querySelectorAll('button'));
                            let confirmBtn = btns.find(b => b.innerText && b.innerText.includes('Confirm & Link with RBSK ID'));
                            if (!confirmBtn) return "NOT_FOUND";
                            if (confirmBtn.disabled) return "DISABLED";
                            
                            // If it is found and not disabled, click it!
                            confirmBtn.scrollIntoView();
                            confirmBtn.click();
                            return "CLICKED";
                        }''')
                        
                        if btn_state == "CLICKED":
                            print("Successfully clicked Confirm & Link!")
                            success = True
                            
                            # Wait for "successfully linked" toast
                            print("Waiting for 'successfully linked' confirmation...")
                            linked = False
                            for _ in range(45):
                                has_toast = page.evaluate('''() => {
                                    return document.body.innerText.includes('successfully linked');
                                }''')
                                if has_toast:
                                    linked = True
                                    break
                                time.sleep(1)
                                
                            if linked:
                                print("Linking successful!")
                            else:
                                print("Timed out waiting for linking confirmation toast.")
                                
                            time.sleep(2) # Extra buffer
                            break
                        
                        time.sleep(1)
                    
                    if not success:
                        print("Could not click Confirm & Link (probably Not Matched or timed out).")
                
                # Close modal
                print("Closing modal...")
                page.evaluate('''() => {
                    let closeBtn = document.querySelector('button.close, .modal-close');
                    if (!closeBtn) {
                        let btns = Array.from(document.querySelectorAll('button'));
                        closeBtn = btns.find(b => b.innerText && b.innerText.toLowerCase().trim() === 'close');
                    }
                    if (closeBtn) closeBtn.click();
                    else {
                        let svgs = Array.from(document.querySelectorAll('svg'));
                        let closeSvg = svgs.find(s => s.parentElement && s.parentElement.tagName === 'BUTTON' && s.innerHTML.includes('M6 18L18 6M6 6l12 12'));
                        if (closeSvg) closeSvg.parentElement.click();
                    }
                }''')
                time.sleep(4)
                print(f"Finished {row_data['name']}. Moving to next.\\n")

            print("Batch process complete for this page.")
            browser.close()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

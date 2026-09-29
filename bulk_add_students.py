import pandas as pd
from playwright.sync_api import sync_playwright
import time
import math
import random

def bulk_add_remaining_students():
    print("Loading Excel data...")
    try:
        df = pd.read_excel('StudentListingReport (24).xlsx')
        df.columns = df.columns.str.strip()
        
        # Get all valid mobile numbers from the ENTIRE list to cycle through
        valid_mobiles = []
        for mob in df["Father's Mobile No"]:
            mob_str = str(mob).strip()
            if mob_str != 'nan' and mob_str != 'None' and mob_str != '':
                clean_mob = mob_str.replace('.0', '')
                if len(clean_mob) >= 10:
                    valid_mobiles.append(clean_mob)
                    
        # Remove duplicates
        valid_mobiles = list(set(valid_mobiles))
        print(f"Found {len(valid_mobiles)} valid mobile numbers in the list to use for blanks: {valid_mobiles}")
        
        class_6 = df[df['Class'].astype(str).str.contains('Sixth', case=False, na=False)]
        
        # We start from index 4 (SONAM RAJPUT) since we already added SONAM, MAHI, LAXMI, PRAGYA
        # Wait, the index in the filtered class_6 dataframe:
        # 0: SONAM
        # 1: MAHI
        # 2: LAXMI
        # 3: PRAGYA
        # 4: SONAM RAJPUT
        remaining_students = class_6.iloc[4:].copy()
        
    except Exception as e:
        print(f"Error reading excel: {e}")
        return

    print(f"Found {len(remaining_students)} students to process.")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        for p_ext in browser.contexts[0].pages:
            if "childScreening" in p_ext.url or "student" in p_ext.url.lower():
                page = p_ext
                break
                
        mobile_idx = 0
                
        for index, row in remaining_students.iterrows():
            name = str(row['FullName as on Aadhar Card']).strip()
            
            dob_raw = row['Date of Birth']
            try:
                dob_dt = pd.to_datetime(dob_raw)
                dob_str = dob_dt.strftime('%d%m%Y')
            except:
                print(f"Skipping {name} due to invalid DOB format: {dob_raw}")
                continue
                
            father = str(row["Father's Full Name aso on Aadhar Card"]).strip()
            mother = str(row["Mother's Full Name as on Aadhaar"]).strip()
            
            mobile = str(row["Father's Mobile No"]).strip()
            if mobile == 'nan' or not mobile or mobile == 'None':
                # Pick a mobile from the valid ones (round-robin)
                mobile = valid_mobiles[mobile_idx % len(valid_mobiles)]
                mobile_idx += 1
            elif mobile.endswith('.0'):
                mobile = mobile[:-2]
                
            cls_raw = str(row['Class']).strip()
            if cls_raw.lower() == 'sixth': cls_val = 'Class 6'
            elif cls_raw.lower() == 'seventh': cls_val = 'Class 7'
            elif cls_raw.lower() == 'eighth': cls_val = 'Class 8'
            else: cls_val = 'Class 6'
            
            address = "GMS KATKAI"
            
            print(f"\n--- Processing {name} ({dob_str}) with Mobile {mobile} ---")
            
            try:
                print("1. Clicking + Add New Student")
                page.evaluate('''() => {
                    let btns = Array.from(document.querySelectorAll('button'));
                    let addBtn = btns.find(b => b.innerText.includes('Add New Student'));
                    if (addBtn) addBtn.click();
                }''')
                time.sleep(2)
                
                print("2. Clicking Without ABHA & Proceed")
                page.evaluate('''() => {
                    let labels = Array.from(document.querySelectorAll('label, div'));
                    let withoutAbha = labels.find(l => l.innerText.includes('Without ABHA'));
                    if (withoutAbha) withoutAbha.click();
                }''')
                time.sleep(1)
                
                page.evaluate('''() => {
                    let btns = Array.from(document.querySelectorAll('button'));
                    let proceed = btns.find(b => b.innerText.includes('Proceed'));
                    if (proceed) proceed.click();
                }''')
                time.sleep(3.5)
                
                print("3. Filling details via JS")
                page.evaluate(f'''() => {{
                    const triggerChange = (el) => {{
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }};
                    const setNativeValue = (el, val) => {{
                        const proto = el.tagName === "SELECT" ? window.HTMLSelectElement.prototype : window.HTMLInputElement.prototype;
                        const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
                        setter.call(el, val);
                        triggerChange(el);
                    }};

                    let nEl = document.querySelector("input[name='studentName']");
                    if (nEl) setNativeValue(nEl, "{name}");
                    
                    let mEl = document.querySelector("input[name='motherName']");
                    if (mEl) setNativeValue(mEl, "{mother}");
                    
                    let fEl = document.querySelector("input[name='fatherName']");
                    if (fEl) setNativeValue(fEl, "{father}");
                    
                    let mob = document.querySelector("input[name='mobile']");
                    if (mob) setNativeValue(mob, "{mobile}");
                    
                    let addr = document.querySelector("input[name='address']");
                    if (addr) setNativeValue(addr, "{address}");
                    
                    let gen = document.querySelector("select[name='gender']");
                    if (gen) {{
                        // Use Female for all currently, or adapt if you have gender in sheet
                        for(let i=0; i<gen.options.length; i++) {{
                            if (gen.options[i].text === "Female") {{ setNativeValue(gen, gen.options[i].value); break; }}
                        }}
                    }}
                    
                    let mOwn = document.querySelector("select[name='mobileOwner']");
                    if (mOwn) {{
                        for(let i=0; i<mOwn.options.length; i++) {{
                            if (mOwn.options[i].text.includes("Parents")) {{ setNativeValue(mOwn, mOwn.options[i].value); break; }}
                        }}
                    }}
                    
                    let cls = document.querySelector("select[name='className']");
                    if (cls) {{
                        for(let i=0; i<cls.options.length; i++) {{
                            if (cls.options[i].text === "{cls_val}") {{ setNativeValue(cls, cls.options[i].value); break; }}
                        }}
                    }}
                }}''')
                time.sleep(1)
                
                print("4. Typing DOB")
                # Clear strictly first
                page.evaluate('''() => {
                    let d = document.querySelector("input[placeholder='dd-mm-yyyy']");
                    if(d) d.value = "";
                }''')
                time.sleep(0.5)
                
                dob_el = page.locator("input[placeholder='dd-mm-yyyy']").first
                dob_el.click(force=True)
                page.keyboard.type(dob_str, delay=100)
                page.keyboard.press("Tab")
                time.sleep(1.5)
                
                print("5. Verifying Form Data")
                verify = page.evaluate('''() => {
                    let v = {};
                    let n = document.querySelector("input[name='studentName']");
                    let d = document.querySelector("input[placeholder='dd-mm-yyyy']");
                    v.name = n ? n.value : "";
                    v.dob = d ? d.value : "";
                    return v;
                }''')
                
                if verify['name'].upper() == name.upper() and verify['dob'] != "":
                    print(f"VERIFIED: Name={verify['name']}, DOB={verify['dob']}")
                else:
                    print(f"VERIFICATION FAILED! Read Name={verify['name']}, DOB={verify['dob']}")
                    break
                    
                print("6. Clicking Save & Start Screening")
                page.evaluate('''() => {
                    let buttons = Array.from(document.querySelectorAll('button'));
                    let saveBtn = buttons.find(b => b.innerText.includes('Save & Start Screening'));
                    if (saveBtn) saveBtn.click();
                }''')
                
                print("Waiting 15 seconds to let the save process completely finish...")
                time.sleep(15) 
                
                print("7. Clicking Back button")
                page.evaluate('''() => {
                    let buttons = Array.from(document.querySelectorAll('button'));
                    let backBtn = buttons.find(b => b.innerText.includes('Back'));
                    if (backBtn) backBtn.click();
                }''')
                time.sleep(5) 
                
            except Exception as e:
                print(f"Failed processing {name}: {e}")
                break

        print("\nFinished processing loop!")
        browser.close()

if __name__ == "__main__":
    bulk_add_remaining_students()

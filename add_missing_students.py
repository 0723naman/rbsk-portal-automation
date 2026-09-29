from playwright.sync_api import sync_playwright
import time

students = [
    {
        "name": "JIVESH KUMAR",
        "dob": "27072018",
        "gender": "Male",
        "mother": "JYOTI",
        "father": "YOGESH KUMAR",
        "mobile": "8396001165",
        "class_val": "Class 2"
    },
    {
        "name": "YAGINI",
        "dob": "10112018",
        "gender": "Female",
        "mother": "POOJA",
        "father": "SACHIN",
        "mobile": "9050948384",
        "class_val": "Class 2"
    },
    {
        "name": "YASHVI",
        "dob": "03102018",
        "gender": "Female",
        "mother": "ANJANA GAUR",
        "father": "JAGPAL SHARMA",
        "mobile": "9001369659",
        "class_val": "Class 2"
    },
    {
        "name": "KHYATI",
        "dob": "17102018",
        "gender": "Female",
        "mother": "SUMAN",
        "father": "RINKU",
        "mobile": "9728101897",
        "class_val": "Class 2"
    },
    {
        "name": "DEVANSH",
        "dob": "08032019",
        "gender": "Male",
        "mother": "RAJNI SHARMA",
        "father": "JONY SHARMA",
        "mobile": "9354277288",
        "class_val": "Class 3"
    },
    {
        "name": "TANISH",
        "dob": "12122020",
        "gender": "Male",
        "mother": "CHHINDU KUMARI",
        "father": "SANDEEP KUMAR",
        "mobile": "9050409488",
        "class_val": "1 Class In Pre-Primary"
    }
]

def add_student(page, student):
    print(f"\n--- Adding Student: {student['name']} ---")
    
    print("Clicking '+ Add New Student'...")
    page.evaluate('''() => {
        let btns = Array.from(document.querySelectorAll('button'));
        let addBtn = btns.find(b => b.innerText.includes('Add New Student'));
        if (addBtn) addBtn.click();
    }''')
    time.sleep(3)
    
    print("Checking for 'Plan Completed' modal...")
    page.evaluate('''() => {
        let btns = Array.from(document.querySelectorAll('button'));
        let proceedBtn = btns.find(b => b.innerText.includes('Yes, proceed!'));
        if (proceedBtn) proceedBtn.click();
    }''')
    time.sleep(3)

    print("Clicking 'Without ABHA'...")
    page.evaluate('''() => {
        let labels = Array.from(document.querySelectorAll('label, div'));
        let withoutAbha = labels.find(l => l.innerText === 'Without ABHA' || (l.innerText && l.innerText.includes('Without ABHA')));
        if (withoutAbha) withoutAbha.click();
    }''')
    time.sleep(3)

    print("Clicking 'Proceed' on ABHA modal...")
    page.evaluate('''() => {
        let btns = Array.from(document.querySelectorAll('button'));
        let proceed = btns.find(b => b.innerText.trim() === 'Proceed');
        if (proceed) proceed.click();
    }''')
    time.sleep(6)
    
    print("Filling text details...")
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
        if (nEl) setNativeValue(nEl, "{student['name']}");
        
        let mEl = document.querySelector("input[name='motherName']");
        if (mEl) setNativeValue(mEl, "{student['mother']}");
        
        let fEl = document.querySelector("input[name='fatherName']");
        if (fEl) setNativeValue(fEl, "{student['father']}");
        
        let mob = document.querySelector("input[name='mobile']");
        if (mob) setNativeValue(mob, "{student['mobile']}");
        
        let addr = document.querySelector("input[name='address']");
        if (addr) setNativeValue(addr, "GPS KUNJPURA");
        
        let gen = document.querySelector("select[name='gender']");
        if (gen) {{
            for(let i=0; i<gen.options.length; i++) {{
                if (gen.options[i].text === "{student['gender']}") {{ setNativeValue(gen, gen.options[i].value); break; }}
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
                if (cls.options[i].text === "{student['class_val']}") {{ setNativeValue(cls, cls.options[i].value); break; }}
            }}
        }}
    }}''')
    time.sleep(3)
    
    print(f"Typing DOB: {student['dob']}...")
    try:
        dob_el = page.locator("input[placeholder='dd-mm-yyyy']").first
        dob_el.click(force=True)
        page.keyboard.type(student['dob'], delay=100)
        page.keyboard.press("Tab")
    except Exception as e:
        print(f"DOB Error: {e}")
    
    time.sleep(4)
    print("Clicking 'Save & Start Screening'...")
    page.evaluate('''() => {
        let buttons = Array.from(document.querySelectorAll('button'));
        let saveBtn = buttons.find(b => b.innerText.includes('Save & Start Screening'));
        if (saveBtn) saveBtn.click();
    }''')
    
    print("Waiting 15 seconds for save to complete...")
    time.sleep(15)
    
    print("Clicking '<- Back'...")
    page.evaluate('''() => {
        let buttons = Array.from(document.querySelectorAll('button'));
        let backBtn = buttons.find(b => b.innerText.includes('Back'));
        if (backBtn) backBtn.click();
    }''')
    
    print("Waiting 8 seconds to return to list...")
    time.sleep(8)
    print(f"Done with {student['name']}.")

def main():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            for s in students:
                add_student(page, s)
                
            browser.close()
            print("Successfully processed all missing students!")
            
    except Exception as e:
        print(f"Browser automation error: {e}")

if __name__ == "__main__":
    main()

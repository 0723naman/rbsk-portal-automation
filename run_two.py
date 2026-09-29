from playwright.sync_api import sync_playwright
import time

def add_student(page, name, mother, father, mobile, dob_str, is_first=False):
    print(f"\n--- Adding Student: {name} ---")
    
    if not is_first:
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
        if (nEl) setNativeValue(nEl, "{name}");
        
        let mEl = document.querySelector("input[name='motherName']");
        if (mEl) setNativeValue(mEl, "{mother}");
        
        let fEl = document.querySelector("input[name='fatherName']");
        if (fEl) setNativeValue(fEl, "{father}");
        
        let mob = document.querySelector("input[name='mobile']");
        if (mob) setNativeValue(mob, "{mobile}");
        
        let addr = document.querySelector("input[name='address']");
        if (addr) setNativeValue(addr, "GMS KATKAI");
        
        let gen = document.querySelector("select[name='gender']");
        if (gen) {{
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
                if (cls.options[i].text === "Class 6") {{ setNativeValue(cls, cls.options[i].value); break; }}
            }}
        }}
    }}''')
    time.sleep(3)
    
    print(f"Typing DOB: {dob_str}...")
    try:
        dob_el = page.locator("input[placeholder='dd-mm-yyyy']").first
        dob_el.click(force=True)
        page.keyboard.type(dob_str, delay=100)
        page.keyboard.press("Tab")
    except Exception as e:
        print(f"DOB Error: {e}")
    
    time.sleep(4)
    print("Taking screenshot before save...")
    page.screenshot(path=f"{name}_filled.png", full_page=True)
    
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
    page.screenshot(path=f"{name}_after_back.png", full_page=True)
    print(f"Done with {name}.")

def main():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            # TANNU is partially started
            add_student(page, name="TANNU", mother="RAJNI DEVI", father="VINOD KUMAR", mobile="8569905257", dob_str="26072015", is_first=True)
            
            # DIVYA
            add_student(page, name="DIVYA", mother="POONAM DEVI", father="TARUN KUMAR", mobile="9050251672", dob_str="01102015", is_first=False)
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

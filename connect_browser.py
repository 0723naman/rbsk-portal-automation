from playwright.sync_api import sync_playwright
import time

def process_pragya_no_submit():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            for p_ext in browser.contexts[0].pages:
                if "childScreening" in p_ext.url or "student" in p_ext.url.lower():
                    page = p_ext
                    break
                    
            print("Step 1: Clicking + Add New Student")
            page.evaluate('''() => {
                let btns = Array.from(document.querySelectorAll('button'));
                let addBtn = btns.find(b => b.innerText.includes('Add New Student'));
                if (addBtn) addBtn.click();
            }''')
            time.sleep(2)
            
            print("Step 2: Clicking Without ABHA & Proceed")
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
            time.sleep(4)
            
            print("Step 3: Filling details for PRAGYA")
            page.evaluate('''() => {
                const triggerChange = (el) => {
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    el.dispatchEvent(new Event('blur', { bubbles: true }));
                };
                const setNativeValue = (el, val) => {
                    const proto = el.tagName === "SELECT" ? window.HTMLSelectElement.prototype : window.HTMLInputElement.prototype;
                    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
                    setter.call(el, val);
                    triggerChange(el);
                };

                let nEl = document.querySelector("input[name='studentName']");
                if (nEl) setNativeValue(nEl, "PRAGYA");
                
                let mEl = document.querySelector("input[name='motherName']");
                if (mEl) setNativeValue(mEl, "ANJU DEVI");
                
                let fEl = document.querySelector("input[name='fatherName']");
                if (fEl) setNativeValue(fEl, "LAXMAN");
                
                let mob = document.querySelector("input[name='mobile']");
                if (mob) setNativeValue(mob, "9416344901");
                
                let addr = document.querySelector("input[name='address']");
                if (addr) setNativeValue(addr, "GMS KATKAI");
                
                let gen = document.querySelector("select[name='gender']");
                if (gen) {
                    for(let i=0; i<gen.options.length; i++) {
                        if (gen.options[i].text === "Female") { setNativeValue(gen, gen.options[i].value); break; }
                    }
                }
                
                let mOwn = document.querySelector("select[name='mobileOwner']");
                if (mOwn) {
                    for(let i=0; i<mOwn.options.length; i++) {
                        if (mOwn.options[i].text.includes("Parents")) { setNativeValue(mOwn, mOwn.options[i].value); break; }
                    }
                }
                
                let cls = document.querySelector("select[name='className']");
                if (cls) {
                    for(let i=0; i<cls.options.length; i++) {
                        if (cls.options[i].text === "Class 6") { setNativeValue(cls, cls.options[i].value); break; }
                    }
                }
            }''')
            time.sleep(2)
            
            print("Step 4: Typing DOB with hyphens: 09-05-2016")
            page.evaluate('''() => {
                let d = document.querySelector("input[placeholder='dd-mm-yyyy']");
                if(d) d.value = "";
            }''')
            time.sleep(0.5)
            
            try:
                dob_input = page.locator("input[placeholder='dd-mm-yyyy']").first
                dob_input.click(force=True)
                
                # Mashing Backspace/Delete to ensure it's empty
                for _ in range(12):
                    page.keyboard.press("Backspace")
                    page.keyboard.press("Delete")
                    page.keyboard.press("ArrowRight")
                
                # Typing the date as requested by the user
                page.keyboard.type("09-05-2016", delay=100)
                page.keyboard.press("Tab")
            except Exception as e:
                print(f"DOB Error: {e}")
                
            time.sleep(2)
            
            print("Step 5: Stopping before submit!")
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_pragya_no_submit()

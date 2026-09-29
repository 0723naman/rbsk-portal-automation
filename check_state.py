from playwright.sync_api import sync_playwright
import time

def reload_and_search():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Reloading page...")
            page.reload()
            time.sleep(4)
            
            print("Selecting Month again...")
            page.evaluate('''() => {
                let selects = Array.from(document.querySelectorAll('select'));
                let monthSelect = selects[selects.length - 1];
                if (monthSelect) {
                    for(let i=0; i<monthSelect.options.length; i++) {
                        if (monthSelect.options[i].text.includes("September")) {
                            monthSelect.value = monthSelect.options[i].value;
                            monthSelect.dispatchEvent(new Event('change', { bubbles: true }));
                            break;
                        }
                    }
                }
            }''')
            time.sleep(1)
            
            print("Clicking Search...")
            page.evaluate('''() => {
                let buttons = Array.from(document.querySelectorAll('button'));
                let search = buttons.find(b => b.innerText.trim() === 'Search');
                if (search) search.click();
            }''')
            time.sleep(4)
            
            html = page.content()
            if "KATKAI" in html.upper():
                print("Found KATKAI in HTML!")
            else:
                print("KATKAI not found yet.")
                
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reload_and_search()

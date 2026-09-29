from playwright.sync_api import sync_playwright
import time

def setup_page():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Navigating to childScreening...")
            page.goto("https://rbsk.mohfw.gov.in/RBSK/childScreening")
            time.sleep(3)
            
            print(f"Current URL: {page.url}")
            
            texts = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('button, a, select, h1, h2, h3')).map(el => el.innerText || el.value || el.name || '').filter(t => t.length > 0);
            }''')
            
            print("Actionable/Select elements:")
            for t in set(texts):
                print(f"- {t}")
                
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_page()

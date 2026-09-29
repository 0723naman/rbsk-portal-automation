from playwright.sync_api import sync_playwright
import time

def proceed():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Clicking 'Yes, proceed!'...")
            page.evaluate('''() => {
                let buttons = Array.from(document.querySelectorAll('button'));
                let yes = buttons.find(b => b.innerText.includes('Yes, proceed!'));
                if (yes) yes.click();
            }''')
            time.sleep(2)
            
            page.screenshot(path="after_proceed.png", full_page=True)
            print("Done! Screenshot saved to after_proceed.png")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    proceed()

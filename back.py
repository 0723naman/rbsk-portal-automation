from playwright.sync_api import sync_playwright
import time

def click_back():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Clicking '<- Back' button...")
            page.evaluate('''() => {
                let buttons = Array.from(document.querySelectorAll('button'));
                let backBtn = buttons.find(b => b.innerText.includes('Back'));
                if (backBtn) backBtn.click();
            }''')
            time.sleep(3)
            
            page.screenshot(path="after_back.png", full_page=True)
            print("Done! Screenshot saved to after_back.png")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    click_back()

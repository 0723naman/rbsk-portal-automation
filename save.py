from playwright.sync_api import sync_playwright
import time

def save_and_screen():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Clicking 'Save & Start Screening'...")
            page.evaluate('''() => {
                let buttons = Array.from(document.querySelectorAll('button'));
                let saveBtn = buttons.find(b => b.innerText.includes('Save & Start Screening'));
                if (saveBtn) saveBtn.click();
            }''')
            time.sleep(4)
            
            page.screenshot(path="after_save.png", full_page=True)
            print("Done! Screenshot saved to after_save.png")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_and_screen()

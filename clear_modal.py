from playwright.sync_api import sync_playwright
import time

def clear_modal():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Clicking 'Yes, proceed!' on modal...")
            page.evaluate('''() => {
                let buttons = Array.from(document.querySelectorAll('button'));
                let proceed = buttons.find(b => b.innerText.includes('Yes, proceed!'));
                if (proceed) proceed.click();
            }''')
            time.sleep(3)
            page.screenshot(path="after_modal_clear.png", full_page=True)
            print("Done! Screenshot saved to after_modal_clear.png")
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clear_modal()

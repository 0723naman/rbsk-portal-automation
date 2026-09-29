from playwright.sync_api import sync_playwright

def get_screenshot():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            page.screenshot(path="current_state.png", full_page=True)
            print("Screenshot saved to current_state.png")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_screenshot()

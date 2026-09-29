from playwright.sync_api import sync_playwright
import time

def screenshot_list():
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            page.screenshot(path="class_6_done.png", full_page=True)
            print("Done")
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    screenshot_list()

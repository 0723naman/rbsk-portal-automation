from playwright.sync_api import sync_playwright
import time

def process_pragya():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            print("Step 4: Fixing DOB...")
            
            try:
                dob_input = page.locator("input[placeholder='dd-mm-yyyy']").first
                dob_input.click(force=True)
                
                # Mashing Backspace/Delete to ensure it's empty
                for _ in range(12):
                    page.keyboard.press("Backspace")
                    page.keyboard.press("Delete")
                    page.keyboard.press("ArrowRight")
                
                # Typing the date as 09052016 without hyphens to see if it auto-formats
                page.keyboard.type("09052016", delay=100)
                page.keyboard.press("Tab")
            except Exception as e:
                print(f"DOB Error: {e}")
                
            time.sleep(2)
            
            page.screenshot(path="pragya_filled_2.png", full_page=True)
            print("Done! Screenshot saved to pragya_filled_2.png")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_pragya()

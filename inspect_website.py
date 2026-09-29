from playwright.sync_api import sync_playwright
import time

def inspect_website():
    with sync_playwright() as p:
        # Use headless=True since the environment does not have a GUI display.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        print("Navigating to https://rbsk.mohfw.gov.in/RBSK/ ...")
        page.goto("https://rbsk.mohfw.gov.in/RBSK/", wait_until="networkidle")
        time.sleep(5)
        
        page.screenshot(path="homepage.png")
        print("Screenshot saved to homepage.png")
        
        title = page.title()
        print(f"Title: {title}")
        
        inputs = page.locator("input").all()
        print(f"\nInputs found ({len(inputs)}):")
        for i in inputs:
            try:
                name = i.get_attribute("name") or i.get_attribute("id") or i.get_attribute("placeholder") or "unnamed"
                type_ = i.get_attribute("type") or "text"
                print(f" - {name} (type: {type_})")
            except:
                pass
                
        buttons = page.locator("button").all()
        print(f"\nButtons found ({len(buttons)}):")
        for b in buttons:
            try:
                text = b.inner_text().strip()
                print(f" - {text}")
            except:
                pass

        print("\nPage text content excerpt:")
        try:
            print(page.locator("body").inner_text()[:1000])
        except:
            print("Could not get text")
        
        browser.close()

if __name__ == "__main__":
    inspect_website()

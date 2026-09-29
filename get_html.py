from playwright.sync_api import sync_playwright

def get_html():
    print("Connecting to Chrome...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            with open("body.html", "w") as f:
                f.write(page.content())
            print("Saved body.html")
            
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_html()

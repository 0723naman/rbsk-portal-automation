from playwright.sync_api import sync_playwright

def get_portal_names():
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            page = browser.contexts[0].pages[0]
            
            # Scrape page 1
            names = []
            rows = page.locator("table tbody tr").all()
            for row in rows:
                cols = row.locator("td").all()
                if len(cols) > 3:
                    name = cols[2].inner_text().strip()
                    names.append(name)
                    
            print(f"Found {len(names)} names on current page:")
            for n in names:
                print(n)
                
            browser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_portal_names()

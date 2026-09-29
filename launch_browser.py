import os
import subprocess
import time

def launch():
    print("Launching Chrome with a remote debugging port (9222)...")
    
    # Create a profile directory in the project folder to keep this session separate and safe
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    
    # Mac path for Google Chrome
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    if not os.path.exists(chrome_path):
        print("Google Chrome not found at default location. Please ensure Chrome is installed.")
        return
        
    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://rbsk.mohfw.gov.in/RBSK/"
    ]
    
    # Launch Chrome as a background process so it stays open
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"\nChrome launched successfully! (PID: {process.pid})")
    print("\nNext Steps:")
    print("1. Please log in to the website in the newly opened Chrome window.")
    print("2. Navigate to the exact form/tab where we need to enter data.")
    print("3. Let me know when you are ready, and I will connect to this window to inspect the form.")

if __name__ == "__main__":
    launch()

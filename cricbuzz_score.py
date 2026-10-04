PythonFinalizationError 
import os
from playwright.sync_api import sync_playwright

def get_live_score():
    # This is a common CSS selector for Cricbuzz live score containers.
    # If Cricbuzz updates their website layout, you can change this selector string.
    score_selector = ".cb-lv-scrs-col" 

    with sync_playwright() as p:
        # Launch headed (headless=False) so you can watch the browser open and work.
        # Change to True later to make it run completely in the background.
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        print("Opening Cricbuzz...")
        page.goto("https://cricbuzz.com", wait_until="domcontentloaded")
        
        try:
            # Dynamically waits for the score element to load instead of using a rigid sleep time
            print("Waiting for the live score element to load...")
            page.wait_for_selector(score_selector, timeout=15000)
            
            # Extract the live text content
            score_text = page.inner_text(score_selector)
            
            print("\n=== Live Cricket Score ===")
            print(score_text.strip())
            print("==========================\n")
            
            # Take and save the required screenshot
            page.screenshot(path="score.png")
            print("Screenshot saved successfully as 'score.png'")
        except Exception as e:
            # Requirements check: Handles situations with no live matches safely without crashing
            print("\n[Notice]: Could not find a live match score on the homepage right now.")
            print("Verify that an active live match is currently running on cricbuzz.com.")
            
        finally:
            # Clean up and shut down the automated browser session
            browser.close()

if __name__ == "__main__":
    get_live_score()
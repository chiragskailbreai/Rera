from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os

# Setup the WebDriver (change to the appropriate driver for your browser)
driver = webdriver.Chrome()  # or webdriver.Firefox()
driver.maximize_window()
# Navigate to the website (replace with the actual URL)
driver.get("https://rera.karnataka.gov.in/projectViewDetails")

# Find the dropdown and select "Bengaluru Urban"
dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "projectDist"))
)
select = Select(dropdown)
select.select_by_visible_text("Bengaluru Urban")

# Click the button (you'll need to provide the correct selector for this button)
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))  # Replace with correct ID or selector
)
button.click()

# Wait for 10 seconds
time.sleep(10)

# Create a directory to save the HTML files
if not os.path.exists("html_pages"):
    os.makedirs("html_pages")

# Loop through pages
page_number = 1
while True:
    # Save the current page's HTML
    with open(f"html_pages/page_{page_number}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    print(f"Saved page {page_number}")

    # Try to find and click the "Next" button
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "approvedTable_next"))
        )
        next_button.click()
        
        # Wait for the page to load
        time.sleep(5)
        
        page_number += 1
        
        # Break the loop if we've processed all 49 pages
        if page_number > 366:
            break
    except:
        print("No more pages to scrape or error occurred.")
        break

# Close the browser
driver.quit()

print("Scraping completed.")
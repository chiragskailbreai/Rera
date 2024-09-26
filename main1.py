import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re

def safe_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def click_element(driver, element, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            ActionChains(driver).move_to_element(element).click().perform()
            return True
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_attempts - 1:
                print(f"Failed to click element after {max_attempts} attempts")
                return False
            time.sleep(1)

def save_project_details(driver, reg_number):
    try:
        # Navigate to the website
        driver.get("https://rera.karnataka.gov.in/projectViewDetails")
        
        # Wait for the input field and enter the registration number
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='regNo2']"))
        )
        input_field.clear()
        input_field.send_keys(reg_number)
        time.sleep(3)
        
        # Click the submit button
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))
        )
        button.click()
        
        # Wait for the results to load
        time.sleep(5)
        
        # Find and click on the file icon
        icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='View Project Details']"))
        )
        if not click_element(driver, icon):
            return False
        

        time.sleep(5)
        # Wait for the new page to load and click on "Project Details"
        pd = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Project Details']"))
        )
        pd.click()
        
        # Get the HTML content
        html_content = driver.page_source
        
        # Create a safe filename
        safe_reg_number = safe_filename(reg_number)
        filename = f"RERA_FILES/project_details_{safe_reg_number}.html"
        
        # Save the HTML content to a new file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Saved {filename}")
        return True
    
    except Exception as e:
        print(f"Error processing registration number {reg_number}: {str(e)}")
        return False

def main():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Setup the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Read registration numbers from CSV file
    with open('registration_numbers.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row if present
        registration_numbers = [row[0] for row in csv_reader]

    successful_saves = 0

    # Process each registration number
    for reg_number in registration_numbers:
        if save_project_details(driver, reg_number):
            successful_saves += 1

    # Close the browser
    driver.quit()

    print(f"Scraping completed. Successfully saved {successful_saves} out of {len(registration_numbers)} project details.")

if __name__ == "__main__":
    main()
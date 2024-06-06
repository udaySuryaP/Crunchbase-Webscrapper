import subprocess
import sys
import time
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to install packages
def install_packages():
    packages = ['selenium==4.8.0', 'pandas==1.5.3', 'webdriver-manager==3.8.5']
    for package in packages:
        try:
            __import__(package.split('==')[0])
        except ImportError:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', package])


# Function to initialize the webdriver
def initialize_driver(browser_choice):
    if browser_choice.lower() == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser_choice.lower() == 'edge':
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        raise ValueError("Unsupported browser!")
    return driver


# Function to scrape recent investments
def scrape_recent_investments(driver, url):
    driver.get(url)
    time.sleep(20)  # Increase wait time to ensure the page loads completely

    investments = []

    try:
        # Wait for the rows to be present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//mat-row[contains(@class, "ng-star-inserted")]')))

        # Find the investment rows
        rows = driver.find_elements(
            By.XPATH, '//mat-row[contains(@class, "ng-star-inserted")]')

        for row in rows:
            try:
                investment_date = row.find_element(By.XPATH,
                                                   './/mat-cell[1]').text
                investor_name = row.find_element(By.XPATH,
                                                 './/mat-cell[2]').text
                company_name = row.find_element(By.XPATH,
                                                './/mat-cell[3]').text
            except Exception as e:
                print(f"Error extracting data from row: {e}")
                investment_date, investor_name, company_name = "N/A", "N/A", "N/A"

            investments.append({
                'Investment Date': investment_date,
                'Investor Name': investor_name,
                'Company Name': company_name
            })
    except Exception as e:
        print(f"Error locating investment rows: {e}")

    return investments


# Function to save data to CSV
def save_to_csv(data):
    if data:
        df = pd.DataFrame(data)
        df.to_csv('recent_investments.csv', index=False)
        print("Data saved to recent_investments.csv")
    else:
        print("No data found to save.")


# Function to read user inputs from config file
def get_user_inputs_from_file():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("config.json not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding config.json: {e}")
        return None


# Main function
def main():
    install_packages()  # Ensure all required packages are installed

    user_inputs = get_user_inputs_from_file()

    if not user_inputs:
        print("All inputs are required!")
        return

    browser_choice = user_inputs.get('browser_choice')
    api_key = user_inputs.get('api_key')
    crunchbase_url = user_inputs.get('crunchbase_url')

    driver = None  # Initialize the driver variable outside the try block

    try:
        driver = initialize_driver(browser_choice)
        investment_data = scrape_recent_investments(driver, crunchbase_url)
        save_to_csv(investment_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()

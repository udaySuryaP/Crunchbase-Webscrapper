import subprocess
import sys
import time
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
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
    if browser_choice == 'Chrome':
        chrome_options = ChromeOptions()
        chrome_options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser_choice == 'Edge':
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.headless = True
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        raise ValueError("Unsupported browser!")
    return driver

# Function to scrape recent investments


def scrape_recent_investments(driver, url):
    driver.get(url)
    time.sleep(10)  # Wait for the page to load completely

    investments = []

    try:
        # Wait for the rows to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//mat-row[contains(@class, "ng-star-inserted")]')))

        # Find the investment rows
        rows = driver.find_elements(
            By.XPATH, '//mat-row[contains(@class, "ng-star-inserted")]')

        for row in rows:
            try:
                investment_date = row.find_element(
                    By.XPATH, './/mat-cell[1]').text
                investor_name = row.find_element(
                    By.XPATH, './/mat-cell[2]').text
                company_name = row.find_element(
                    By.XPATH, './/mat-cell[3]').text
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

# Function to get user inputs via Tkinter


def get_user_inputs():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    browser_choice = simpledialog.askstring(
        "Input", "Enter browser choice (Chrome/Edge):")
    api_key = simpledialog.askstring("Input", "Enter your Crunchbase API Key:")
    crunchbase_url = simpledialog.askstring(
        "Input", "Enter the Crunchbase URL of the company:")

    return browser_choice, api_key, crunchbase_url

# Main function


def main():
    install_packages()  # Ensure all required packages are installed

    browser_choice, api_key, crunchbase_url = get_user_inputs()

    if not browser_choice or not api_key or not crunchbase_url:
        print("All inputs are required!")
        return

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

# Crunchbase Scraper

## Overview

This Python script `scrappy.py` is designed to scrape recent investment data from a Crunchbase company page. It allows users to input the browser of choice (Chrome or Edge), Crunchbase API key, and the Crunchbase URL of the company they wish to scrape. The script then automates the process of navigating to the Crunchbase page, extracting investment data, and saving it to a CSV file.

## Features

- **Automated Web Scraping**: The script automates the process of navigating to the Crunchbase webpage, extracting investment data, and saving it to a CSV file.
  
- **Browser Compatibility**: Supports both Chrome and Edge browsers for web scraping.
  
- **User-friendly Interface**: Utilizes Tkinter to provide a simple GUI for users to input necessary details such as browser choice, Crunchbase API key, and company URL.
  
- **Dependency Installation**: Automatically checks for and installs required dependencies listed in the `requirements.txt` file if not already installed.

## Dependencies

The script relies on the following Python libraries:

- **Selenium**: For web automation.
- **Pandas**: For data manipulation and CSV file handling.
- **Webdriver-manager**: For managing WebDriver binaries.

These dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone the repository or download the `scrappy.py` file.

2. Install the required dependencies by running the following command in your terminal:

`pip install -r requirements.txt`


3. Ensure you have either Google Chrome or Microsoft Edge installed on your system.

## Usage

1. Run the script `scrappy.py` using Python:

`python scrappy.py`


2. Follow the prompts to input the necessary details:
 - Browser choice (Chrome or Edge)
 - Crunchbase API key
 - Crunchbase URL of the company

3. The script will then proceed to scrape the investment data, and upon completion, it will save the data to a CSV file named `recent_investments.csv`.

## Notes

- Ensure that the provided Crunchbase URL leads to a valid company page with recent investment data.
- In case of any issues or errors during execution, check the console output for error messages and logs.
- For additional customization or modification, refer to the source code comments for guidance.



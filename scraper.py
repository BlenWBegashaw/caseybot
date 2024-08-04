import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to log in to Salesforce
def login_to_salesforce(username, password):
    try:
        driver.get('https://login.salesforce.com')
        time.sleep(3)  # Wait for the page to load

        # Find and fill the username and password fields
        username_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'Login')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        time.sleep(5)  # Wait for the login to complete
    except Exception as e:
        print(f"Error logging in to Salesforce: {e}")
        driver.quit()
        exit(1)

# Function to navigate to a specific case
def navigate_to_case(case_url):
    try:
        driver.get(case_url)
        time.sleep(5)  # Wait for the page to load
    except Exception as e:
        print(f"Error navigating to case URL {case_url}: {e}")
        driver.quit()
        exit(1)

# Function to scrape data from the case page
def scrape_case_data():
    try:
        # Adjust the selectors based on the actual HTML structure of the Salesforce case page
        subject = driver.find_element(By.CSS_SELECTOR, 'h1').text
        description = driver.find_element(By.CSS_SELECTOR, 'p').text
        return subject, description
    except Exception as e:
        print(f"Error scraping case data: {e}")
        driver.quit()
        exit(1)

# Function to send data to the backend
def send_data_to_backend(subject, description):
    try:
        payload = {
            "case": {
                "subject": subject,
                "description": description
            }
        }
        response = requests.post('http://localhost:5000/match_cases', json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending data to backend: {e}")
        return None

# Main function to run the scraper
def main():
    salesforce_username = os.getenv('SALESFORCE_USERNAME', 'blenw@gmail.com')
    salesforce_password = os.getenv('SALESFORCE_PASSWORD', 'Blen1234567?')
    case_urls = [
        'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view',
        # Add more case URLs as needed
    ]

    # Log in to Salesforce
    login_to_salesforce(salesforce_username, salesforce_password)

    # Loop through each case URL and scrape data
    for case_url in case_urls:
        navigate_to_case(case_url)
        subject, description = scrape_case_data()
        print(f'Subject: {subject}')
        print(f'Description: {description}')
        response = send_data_to_backend(subject, description)
        if response:
            print(f'Response: {response}')
        time.sleep(60)  # Wait for 60 seconds before scraping the next case

    # Close the WebDriver
    driver.quit()

if __name__ == '__main__':
    main()


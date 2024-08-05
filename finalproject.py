
import os
import time
import requests
from flask import Flask, request, jsonify, render_template
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Define constants
DOMAIN = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
OAUTH_ENDPOINT = '/services/oauth2/token'

# Hardcoded Salesforce credentials
CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
USERNAME = 'blenw@gmail.com'
PASSWORD = 'Blen1234567?'

# Function to calculate similarity between two strings
def calculate_similarity(text1: str, text2: str) -> float:
    if text1 is None:
        text1 = ""
    if text2 is None:
        text2 = ""
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# Function to find top matches based on similarity
def find_top_matches(given_case: dict, cases: list, top_n: int = 5) -> list:
    similarities = []
    for case in cases:
        subject_similarity = calculate_similarity(given_case.get("subject", ""), case.get("Subject", ""))
        description_similarity = calculate_similarity(given_case.get("description", ""), case.get("Description", ""))
        overall_similarity = (subject_similarity + description_similarity) / 2
        similarities.append((case, overall_similarity))

    sorted_cases = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_matches = []
    for case, similarity in sorted_cases[:top_n]:
        case_number = case["CaseNumber"]
        case_link = f"{DOMAIN}/lightning/r/Case/{case['Id']}/view"
        top_matches.append({
            "case_number": case_number,
            "case_link": case_link,
            "subject": case["Subject"],
            "description": case["Description"],
            "similarity": similarity
        })
    return top_matches

# Function to log in to Salesforce using Selenium
def login_to_salesforce(driver, username, password):
    driver.get('https://login.salesforce.com')
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.ID, 'Login')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    time.sleep(5)

# Function to scrape data from a specific case URL
def scrape_case_data(driver, case_url):
    driver.get(case_url)
    time.sleep(5)

    subject = driver.find_element(By.CSS_SELECTOR, 'h1').text
    description = driver.find_element(By.CSS_SELECTOR, 'p').text
    return subject, description

# Function to get access token
def get_access_token():
    payload = {
        'grant_type': 'password',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(DOMAIN + OAUTH_ENDPOINT, data=payload)
    response.raise_for_status()
    token_response = response.json()
    return token_response['access_token']

# Function to fetch cases from Salesforce
def fetch_cases(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{DOMAIN}/services/data/v52.0/query/?q=SELECT+Id,CaseNumber,Subject,Description+FROM+Case', headers=headers)
    response.raise_for_status()
    return response.json()['records']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match_cases', methods=['POST'])
def match_cases():
    data = request.json
    given_case = data['case']

    try:
        # Get access token
        access_token = get_access_token()

        # Fetch cases from Salesforce
        existing_cases = fetch_cases(access_token)

        # Find top matches
        top_matches = find_top_matches(given_case, existing_cases)

        return jsonify(top_matches)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape_cases', methods=['POST'])
def scrape_cases():
    salesforce_username = 'blenw@gmail.com'
    salesforce_password = 'Blen1234567?'
    case_urls = request.json.get('case_urls', [])

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Log in to Salesforce
        login_to_salesforce(driver, salesforce_username, salesforce_password)

        results = []
        for case_url in case_urls:
            subject, description = scrape_case_data(driver, case_url)
            results.append({
                "subject": subject,
                "description": description,
                "url": case_url
            })
            time.sleep(60)  # Wait between scraping to avoid hitting the server too fast

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)



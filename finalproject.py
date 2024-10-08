import os
import requests
import json
import time
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from difflib import SequenceMatcher
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Salesforce credentials
LOGIN_DOMAIN = 'https://login.salesforce.com'
INSTANCE_URL = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
OAUTH_ENDPOINT = '/services/oauth2/token'
CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
USERNAME = 'blenw@gmail.com'
PASSWORD = 'Blen1234567?'

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to calculate similarity between two strings
def calculate_similarity(text1: str, text2: str) -> float:
    if text1 is None:
        text1 = ""
    if text2 is None:
        text2 = ""
    return SequenceMatcher(None, text1, text2).ratio()

# Function to get access token
def get_access_token():
    payload = {
        'grant_type': 'password',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(LOGIN_DOMAIN + OAUTH_ENDPOINT, data=payload)
    response.raise_for_status()
    token_response = response.json()
    return token_response['access_token']

# Function to fetch cases from Salesforce
def fetch_cases(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{INSTANCE_URL}/services/data/v52.0/query/?q=SELECT+Id,CaseNumber,Subject,Description+FROM+Case', headers=headers)
    response.raise_for_status()
    return response.json()['records']


def scrape_case_details(url):
    try:
        session = requests.Session()
        response = session.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Check if the response is a redirection page
        if "window.location.replace" in response.text or "window.location.href" in response.text:
            # Extract the redirection URL
            soup = BeautifulSoup(response.content, 'html.parser')
            redirect_script = soup.find('script', text=lambda t: t and "window.location" in t)
            if redirect_script:
                redirect_url = redirect_script.text.split("'")[1]
                response = session.get(redirect_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
        else:
            soup = BeautifulSoup(response.content, 'html.parser')

        # Debug: Print the HTML content
        print("HTML Content:", soup.prettify())

        # Update the selectors based on the actual HTML structure
        subject_element = soup.find('lightning-formatted-text', {'title': True})
        subject = subject_element['title'].strip() if subject_element else 'No subject found'

        description_element = soup.find('lightning-formatted-text', {'data-output-element-id': 'output-field', 'slot': 'outputField'})
        description = description_element.text.strip() if description_element else 'No description found'

        # Ensure subject and description are strings
        subject = str(subject)
        description = str(description)

        # Debug: Print the extracted subject and description
        print("Extracted Subject:", subject)
        print("Extracted Description:", description)

        return subject, description
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return 'No subject found', 'No description found'
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
        return 'No subject found', 'No description found'



# Function to find the top N matching cases based on subject and description using GPT-3.5 or GPT-4
def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
    prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
    for case in cases:
        prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

    prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        response_text = response.choices[0].message['content'].strip()
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        response_text = response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    # Debug: Print the response text to the console
    print("Response Text:", response_text)

    top_matches = []
    for line in response_text.split('\n'):
        if line.startswith("Case Number:"):
            try:
                parts = line.split()
                case_number = parts[2]
                relevance_score = float(parts[-1])
                for case in cases:
                    if case["CaseNumber"] == case_number:
                        top_matches.append({
                            "case_number": case["CaseNumber"],
                            "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
                            "subject": case["Subject"],
                            "description": case["Description"],
                            "similarity": relevance_score
                        })
                        break
            except Exception as e:
                print(f"Error parsing line '{line}': {e}")

    # Debug: Print the top matches to the console
    print("Top Matches:", top_matches)
    return top_matches[:top_n]

@app.route('/')
def home():
    # Example URL to scrape
    url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
    
    # Scrape the subject and description from the case page
    subject, description = scrape_case_details(url)
    given_case = {'subject': subject, 'description': description}

    # Debug: Print the given case to the console
    print("Given Case:", given_case)

    # Get access token
    access_token = get_access_token()

    # Fetch cases from Salesforce
    existing_cases = fetch_cases(access_token)

    # Debug: Print the existing cases to the console
    print("Existing Cases:", existing_cases)

    # Find top matches using GPT-3.5 or GPT-4
    top_matches = find_top_matches_gpt(given_case, existing_cases)

    # Debug: Print the top matches to the console
    print("Top Matches:", top_matches)

    return render_template('file.html', matches=top_matches)

@app.route('/recommend_cases', methods=['POST'])
def recommend_cases():
    data = request.json
    given_case = data['case']

    # Scrape the subject and description from the case page
    subject, description = scrape_case_details(given_case['url'])
    given_case['subject'] = subject
    given_case['description'] = description

    # Get access token
    access_token = get_access_token()

    # Fetch cases from Salesforce
    existing_cases = fetch_cases(access_token)

    # Find top matches using GPT-3.5 or GPT-4
    top_matches = find_top_matches_gpt(given_case, existing_cases)

    return jsonify(top_matches)

if __name__ == '__main__':
    socketio.run(app, debug=True)

# import os
# import requests
# import json
# import time
# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# import openai
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app)

# # Salesforce credentials
# LOGIN_DOMAIN = 'https://login.salesforce.com'
# INSTANCE_URL = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
# OAUTH_ENDPOINT = '/services/oauth2/token'
# CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
# CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
# USERNAME = 'blenw@gmail.com'
# PASSWORD = 'Blen1234567?'

# # Set your OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # Function to find the top N matching cases based on subject and description using GPT-3.5 or GPT-4
# # def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
# #     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
# #     for case in cases:
# #         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

# #     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

# #     try:
# #         response = openai.ChatCompletion.create(
# #             model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
# #             messages=[
# #                 {"role": "system", "content": "You are a helpful assistant."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             max_tokens=150,
# #             n=1,
# #             stop=None,
# #             temperature=0.7,
# #         )
# #         response_text = response.choices[0].message['content'].strip()
# #     except openai.error.RateLimitError as e:
# #         print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
# #         time.sleep(60)  # Wait for 60 seconds before retrying
# #         response = openai.ChatCompletion.create(
# #             model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
# #             messages=[
# #                 {"role": "system", "content": "You are a helpful assistant."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             max_tokens=150,
# #             n=1,
# #             stop=None,
# #             temperature=0.7,
# #         )
# #         response_text = response.choices[0].message['content'].strip()

# #     # Debug: Print the response text to the console
# #     print("Response Text:", response_text)

# #     top_matches = []
# #     for line in response_text.split('\n'):
# #         if "Case Number:" in line:
# #             parts = line.split()
# #             case_number = parts[2]
# #             relevance_score = 0.0  # Default relevance score
# #             if "Relevance Score:" in line:
# #                 relevance_score = float(parts[-1].replace("(", "").replace(")", "").replace("Relevance", "").replace("Score:", "").replace("High", "1.0").replace("Medium", "0.5").replace("Low", "0.1"))
# #             for case in cases:
# #                 if case["CaseNumber"] == case_number:
# #                     top_matches.append({
# #                         "case_number": case["CaseNumber"],
# #                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
# #                         "subject": case["Subject"],
# #                         "description": case["Description"],
# #                         "similarity": relevance_score
# #                     })
# #                     break
# #     # Debug: Print the top matches to the console
# #     print("Top Matches:", top_matches)
# #     return top_matches[:top_n]

# import openai
# import time

# import openai
# import time
# import requests
# from bs4 import BeautifulSoup

# # Salesforce credentials
# DOMAIN = 'https://login.salesforce.com'
# OAUTH_ENDPOINT = '/services/oauth2/token'
# CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
# CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
# USERNAME = 'blenw@gmail.com'
# PASSWORD = 'Blen1234567?'

# # Salesforce instance URL
# INSTANCE_URL = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'

# # Function to get access token
# def get_access_token():
#     payload = {
#         'grant_type': 'password',
#         'client_id': CONSUMER_KEY,
#         'client_secret': CONSUMER_SECRET,
#         'username': USERNAME,
#         'password': PASSWORD
#     }
#     response = requests.post(DOMAIN + OAUTH_ENDPOINT, data=payload)
#     response.raise_for_status()
#     token_response = response.json()
#     return token_response['access_token'], token_response['instance_url']

# # Function to get case details using the Salesforce REST API
# def get_case_details(access_token, instance_url, case_id):
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     case_url = f'{instance_url}/services/data/v52.0/sobjects/Case/{case_id}'
#     response = requests.get(case_url, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         case_data = response.json()
#         subject = case_data.get('Subject', 'No subject found')
#         description = case_data.get('Description', 'No description found')
#         return subject, description
#     else:
#         print(f'Failed to retrieve the case details. Status code: {response.status_code}')
#         return None, None
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     # url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
#     # print("HERE IS URLLLL:", url)
#     # x = scrape_case_details(url)
#     # print("Here is x:", x)
#     try:
#         # Get access token
#         access_token, instance_url = get_access_token()
#         print('Access token obtained successfully.')

#         # Get case details
#         case_id = '500aj00000FL9RyAAL'
#         subject, description = get_case_details(access_token, instance_url, case_id)
#         if subject and description:
#             print(f'Subject: {subject}')
#             print(f'Description: {description}')
#     except Exception as e:
#         print(f'An error occurred: {e}')
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         response_text = response.choices[0].message['content'].strip()
#     except openai.error.RateLimitError as e:
#         print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
#         time.sleep(60)  # Wait for 60 seconds before retrying
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         response_text = response.choices[0].message['content'].strip()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             try:
#                 parts = line.split()
#                 case_number = parts[2]
#                 relevance_score = float(parts[-1])
#                 for case in cases:
#                     if case["CaseNumber"] == case_number:
#                         top_matches.append({
#                             "case_number": case["CaseNumber"],
#                             "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                             "subject": case["Subject"],
#                             "description": case["Description"],
#                             "similarity": relevance_score
#                         })
#                         break
#             except Exception as e:
#                 print(f"Error parsing line '{line}': {e}")

#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

# # Example usage:
# given_case = {"subject": "Network Issue", "description": "The network is down in the office."}
# cases = [
#     {"CaseNumber": "001", "Subject": "Network Issue", "Description": "The network is down in the office.", "Id": "a1"},
#     {"CaseNumber": "002", "Subject": "Login Issue", "Description": "Unable to login to the system.", "Id": "b2"},
#     {"CaseNumber": "003", "Subject": "Network Issue", "Description": "Slow internet speed.", "Id": "c3"},
#     {"CaseNumber": "004", "Subject": "Hardware Issue", "Description": "The printer is not working.", "Id": "d4"},
#     {"CaseNumber": "005", "Subject": "Network Issue", "Description": "Wi-Fi is not connecting.", "Id": "e5"},
# ]

# INSTANCE_URL = "https://example.salesforce.com"
# top_matches = find_top_matches_gpt(given_case, cases)
# print(top_matches)




# # Function to get access token
# def get_access_token():
#     payload = {
#         'grant_type': 'password',
#         'client_id': CONSUMER_KEY,
#         'client_secret': CONSUMER_SECRET,
#         'username': USERNAME,
#         'password': PASSWORD
#     }
#     response = requests.post(LOGIN_DOMAIN + OAUTH_ENDPOINT, data=payload)
#     response.raise_for_status()
#     token_response = response.json()
#     return token_response['access_token']

# # Function to fetch cases from Salesforce
# def fetch_cases(access_token):
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.get(f'{INSTANCE_URL}/services/data/v52.0/query/?q=SELECT+Id,CaseNumber,Subject,Description+FROM+Case', headers=headers)
#     response.raise_for_status()
#     return response.json()['records']

# # Function to scrape subject and description from the case page
# def scrape_case_details(url):
#     response = requests.get(url)
#     print("url:", url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     print("HERE I AM:", soup)
    
#     # Debug: Print the HTML content
#     print("HTML Content:", soup.prettify())
    
#     # Update the selectors based on the actual HTML structure
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
    
#     # Update the selector for the description element
#     description_element = soup.find('lightning-formatted-text', {'data-output-element-id': 'output-field'})
#     description = description_element.text.strip() if description_element else 'No description found'
    
#     # Debug: Print the extracted subject and description
#     print("Extracted Subject:", subject)
#     print("Extracted Description:", description)
    
#     return subject, description

# @app.route('/')
# def home():
#     # Example URL to scrape
#     url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
    
#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(url)
#     given_case = {'subject': subject, 'description': description}

#     # Debug: Print the given case to the console
#     print("Given Case:", given_case)

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Debug: Print the existing cases to the console
#     print("Existing Cases:", existing_cases)

#     # Find top matches using GPT-3.5 or GPT-4
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)

#     return render_template('file.html', matches=top_matches)

# @app.route('/recommend_cases', methods=['POST'])
# def recommend_cases():
#     data = request.json
#     given_case = data['case']

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(given_case['url'])
#     given_case['subject'] = "MS Switchports keep flapping" #subject
#     given_case['description'] = "My switch is having issues" #description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5 or GPT-4
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# if __name__ == '__main__':
    
#     # url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
#     # # print("HERE IS THE URL", url)
#     # # # Scrape the subject and description from the case page
#     # # subject, description = scrape_case_details(url)
    
#     socketio.run(app, debug=True)


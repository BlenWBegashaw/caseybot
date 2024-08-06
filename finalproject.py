# import os
# import requests
# import json
# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# import openai

# app = Flask(__name__)
# # CORS(app)
# # socketio = SocketIO(app)

# # Define constants
# DOMAIN = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
# OAUTH_ENDPOINT = '/services/oauth2/token'

# # Define your Salesforce credentials
# CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
# CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
# USERNAME = 'blenw@gmail.com'
# PASSWORD = 'Blen1234567?'

# # Set your OpenAI API key
# openai.api_key = 'sk-l6r8FFBAuZC-3g5aDaLE3wqHYPcn15QKborDVqrMTXT3BlbkFJqIRzJJypRwwa0wPIS1hPYzZ01DK2ikbV818JyDpWcA'

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # Function to find the top N matching cases based on subject and description
# def find_top_matches(given_case: dict, cases: list, top_n: int = 5) -> list:
#     similarities = []
#     for case in cases:
#         subject_similarity = calculate_similarity(given_case.get("subject", ""), case.get("Subject", ""))
#         description_similarity = calculate_similarity(given_case.get("description", ""), case.get("Description", ""))
#         overall_similarity = (subject_similarity + description_similarity) / 2
#         similarities.append((case, overall_similarity))

#     # Sort by similarity in descending order
#     sorted_cases = sorted(similarities, key=lambda x: x[1], reverse=True)
#     # Return the top N matches with case number and link
#     top_matches = []
#     for case, similarity in sorted_cases[:top_n]:
#         case_number = case["CaseNumber"]
#         case_link = f"{DOMAIN}/lightning/r/Case/{case['Id']}/view"
#         top_matches.append({
#             "case_number": case_number,
#             "case_link": case_link,
#             "subject": case["Subject"],
#             "description": case["Description"],
#             "similarity": similarity
#         })
#     return top_matches

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
#     return token_response['access_token']

# # Function to fetch cases from Salesforce
# def fetch_cases(access_token):
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     response = requests.get(f'{DOMAIN}/services/data/v52.0/query/?q=SELECT+Id,CaseNumber,Subject,Description+FROM+Case', headers=headers)
#     response.raise_for_status()
#     return response.json()['records']

# @app.route('/')
# def home():
#     subject = request.args.get('subject', '')
#     description = request.args.get('description', '')
#     return render_template('file.html', subject=subject, description=description)

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches
#     top_matches = find_top_matches(given_case, existing_cases)

#     return jsonify(top_matches)

# # @socketio.on('connect')
# # def handle_connect():
# #     print('Client connected')

# # @socketio.on('disconnect')
# # def handle_disconnect():
# #     print('Client disconnected')

# # @socketio.on('message')
# # def handle_message(data):
# #     print('Received message: ' + data)
# #     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
# import os
# import requests
# import json
# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# import openai
# from bs4 import BeautifulSoup

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
# openai.api_key = 'sk-lqeaCDS4EUf8H8vC8lhNdDcaVqU17xPZ_QhjJlB2YzT3BlbkFJgXtJK9gbrQsIVlLyuTcrSRok95mYbX6aSw4192cewA'

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # Function to find the top N matching cases based on subject and description using GPT-3.5
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )

#     response_text = response.choices[0].text.strip()
#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1])
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     return top_matches[:top_n]

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
# def scrape_case_details():
#     url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
#     return subject, description

# @app.route('/')
# def home():
#     subject = request.args.get('subject', '')
#     description = request.args.get('description', '')
#     return render_template('file.html', subject=subject, description=description)

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details()
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data)
#     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
# import os
# import requests
# import json
# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# import openai
# from bs4 import BeautifulSoup

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
# openai.api_key = 'sk-lqeaCDS4EUf8H8vC8lhNdDcaVqU17xPZ_QhjJlB2YzT3BlbkFJgXtJK9gbrQsIVlLyuTcrSRok95mYbX6aSw4192cewA'

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # Function to find the top N matching cases based on subject and description using GPT-3.5
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )

#     response_text = response.choices[0].text.strip()
#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1])
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
#     return subject, description

# @app.route('/')
# def home():
#     subject = request.args.get('subject', '')
#     description = request.args.get('description', '')
#     return render_template('file.html', subject=subject, description=description)

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(given_case['url'])
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data)
#     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
# import os
# import requests
# import json
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# import openai
# from bs4 import BeautifulSoup

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
# openai.api_key = 'sk-lqeaCDS4EUf8H8vC8lhNdDcaVqU17xPZ_QhjJlB2YzT3BlbkFJgXtJK9gbrQsIVlLyuTcrSRok95mYbX6aSw4192cewA'

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # Function to find the top N matching cases based on subject and description using GPT-3.5
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )

#     response_text = response.choices[0].text.strip()
#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1])
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
#     return subject, description

# @app.route('/')
# def home():
#     return "Hello, World!"

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(given_case['url'])
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data)
#     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
# import os
# import requests
# import json
# from flask import Flask, request, jsonify, render_template
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# from difflib import SequenceMatcher
# from dotenv import load_dotenv
# import openai
# from bs4 import BeautifulSoup

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
# # # Set your OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')
# # client = OpenAI(
# #     api_key = os.environ.get('OPENAI_API_KEY') 
# # )

# # Function to calculate similarity between two strings
# def calculate_similarity(text1: str, text2: str) -> float:
#     if text1 is None:
#         text1 = ""
#     if text2 is None:
#         text2 = ""
#     return SequenceMatcher(None, text1, text2).ratio()

# # # Function to find the top N matching cases based on subject and description using GPT-3.5
# # def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
# #     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
# #     for case in cases:
# #         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

# #     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

# #     response = openai.ChatCompletion.create(
# #         engine="gpt-4o-mini",
# #         prompt=prompt,
# #         max_tokens=150,
# #         n=1,
# #         stop=None,
# #         temperature=0.7,
# #     )

# #     response_text = response.choices[0].text.strip()
# #     top_matches = []
# #     for line in response_text.split('\n'):
# #         if line.startswith("Case Number:"):
# #             parts = line.split()
# #             case_number = parts[2]
# #             relevance_score = float(parts[-1])
# #             for case in cases:
# #                 if case["CaseNumber"] == case_number:
# #                     top_matches.append({
# #                         "case_number": case["CaseNumber"],
# #                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
# #                         "subject": case["Subject"],
# #                         "description": case["Description"],
# #                         "similarity": relevance_score
# #                     })
#     #                 break
#     # return top_matches[:top_n]
# # Function to find the top N matching cases based on subject and description using GPT-4.0
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4.0-mini",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#     # except openai.error.RateLimitError as e:
#     #     print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
#     #     time.sleep(60)  # Wait for 60 seconds before retrying
#     #     response = openai.ChatCompletion.create(
#     #         model="gpt-4.0-mini",
#     #         messages=[
#     #             {"role": "system", "content": "You are a helpful assistant."},
#     #             {"role": "user", "content": prompt}
#     #         ],
#     #         max_tokens=150,
#     #         n=1,
#     #         stop=None,
#     #         temperature=0.7,
#     #     )

#     response_text = response.choices[0].message['content'].strip()
#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1])
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     return top_matches[:top_n]
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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
#     return subject, description

# @app.route('/')
# def home():
#     # Example URL to scrape
#     url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
    
#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(url)
#     given_case = {'subject': subject, 'description': description}

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return render_template('file.html', matches=top_matches)

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(given_case['url'])
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data)
#     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
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
# from dotenv import load_dotenv  # Import load_dotenv

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

# # Function to find the top N matching cases based on subject and description using GPT-4.0
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
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
#             model="gpt-4.0-mini",
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

#     top_matches = []
#     for line in response_text.split('\n'):
#         if line.startswith("Case Number:"):
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1])
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
#     return subject, description

# @app.route('/')
# def home():
#     # Example URL to scrape
#     url = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view'
    
#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(url)
#     given_case = {'subject': subject, 'description': description}

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-4.0
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return render_template('file.html', matches=top_matches)

# @app.route('/match_cases', methods=['POST'])
# def match_cases():
#     data = request.json
#     given_case = data['case']

#     # Log the received case for debugging
#     print('Received case:', given_case)

#     # Scrape the subject and description from the case page
#     subject, description = scrape_case_details(given_case['url'])
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-4.0
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message: ' + data)
#     # Process the message and perform any necessary actions

# if __name__ == '__main__':
#     from os import environ
#     socketio.run(app, host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)

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
# CONSUMER_KEY = os.getenv('CONSUMER_KEY')
# CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
# USERNAME = os.getenv('USERNAME')
# PASSWORD = os.getenv('PASSWORD')

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
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
#     prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
#     for case in cases:
#         prompt += f"\nCase Number: {case['CaseNumber']}\nSubject: {case['Subject']}\nDescription: {case['Description']}\n"

#     prompt += "\nPlease provide the top matches with their case numbers and relevance scores."

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         response_text = response.choices[0].message['content'].strip()
#     except openai.error.RateLimitError:
#         print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
#         time.sleep(60)  # Wait for 60 seconds before retrying
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         response_text = response.choices[0].message['content'].strip()

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     # Parsing the response to extract case numbers and relevance scores
#     top_matches = []
#     lines = response_text.split('\n')
#     for i in range(len(lines)):
#         if lines[i].startswith("Case Number:"):
#             parts = lines[i].split()
#             case_number = parts[2]
#             try:
#                 relevance_score = float(parts[-1])
#             except ValueError:
#                 relevance_score = None

#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break

#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
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

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
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
# from dotenv import load_dotenv  # Import load_dotenv

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
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
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

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     top_matches = []
#     for line in response_text.split('\n'):
#         if "Case Number:" in line:
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1].replace("(", "").replace(")", "").replace("Relevance", "").replace("Score:", "").replace("High", "1.0").replace("Medium", "0.5").replace("Low", "0.1"))
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
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
# from dotenv import load_dotenv  # Import load_dotenv

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
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
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

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     top_matches = []
#     for line in response_text.split('\n'):
#         if "Case Number:" in line:
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = float(parts[-1].replace("(", "").replace(")", "").replace("Relevance", "").replace("Score:", "").replace("High", "1.0").replace("Medium", "0.5").replace("Low", "0.1"))
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
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
#     given_case['subject'] = subject
#     given_case['description'] = description

#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5 or GPT-4
#     top_matches = find_top_matches_gpt(given_case, existing_cases)

#     return jsonify(top_matches)
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
# from dotenv import load_dotenv  # Import load_dotenv

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
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
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

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     top_matches = []
#     for line in response_text.split('\n'):
#         if "Case Number:" in line:
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = 0.0  # Default relevance score
#             if "Relevance Score:" in line:
#                 relevance_score = float(parts[-1].replace("(", "").replace(")", "").replace("Relevance", "").replace("Score:", "").replace("High", "1.0").replace("Medium", "0.5").replace("Low", "0.1"))
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

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
#     soup = BeautifulSoup(response.content, 'html.parser')
#     subject_element = soup.find('lightning-formatted-text', {'title': True})
#     subject = subject_element['title'].strip() if subject_element else 'No subject found'
#     description_element = soup.find('div', {'class': 'description-class'})  # Update the selector as needed
#     description = description_element.text.strip() if description_element else 'No description found'
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
#     given_case['subject'] = subject
#     given_case['description'] = description
    
#     # Get access token
#     access_token = get_access_token()

#     # Fetch cases from Salesforce
#     existing_cases = fetch_cases(access_token)

#     # Find top matches using GPT-3.5 or GPT-4
#     top_matches = find_top_matches_gpt(given_case, existing_cases)
    
#  return render_template('file.html', matches=top_matches)
#     # return jsonify(top_matches)
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

# Function to find the top N matching cases based on subject and description using GPT-3.5 or GPT-4
# def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
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

#     # Debug: Print the response text to the console
#     print("Response Text:", response_text)

#     top_matches = []
#     for line in response_text.split('\n'):
#         if "Case Number:" in line:
#             parts = line.split()
#             case_number = parts[2]
#             relevance_score = 0.0  # Default relevance score
#             if "Relevance Score:" in line:
#                 relevance_score = float(parts[-1].replace("(", "").replace(")", "").replace("Relevance", "").replace("Score:", "").replace("High", "1.0").replace("Medium", "0.5").replace("Low", "0.1"))
#             for case in cases:
#                 if case["CaseNumber"] == case_number:
#                     top_matches.append({
#                         "case_number": case["CaseNumber"],
#                         "case_link": f"{INSTANCE_URL}/lightning/r/Case/{case['Id']}/view",
#                         "subject": case["Subject"],
#                         "description": case["Description"],
#                         "similarity": relevance_score
#                     })
#                     break
#     # Debug: Print the top matches to the console
#     print("Top Matches:", top_matches)
#     return top_matches[:top_n]

import openai
import time

def find_top_matches_gpt(given_case: dict, cases: list, top_n: int = 5) -> list:
    # prompt = f"Find the most relevant cases for the following case:\n\nSubject: {given_case['subject']}\nDescription: {given_case['description']}\n\nHere are the available cases:\n"
    prompt = f"Find the most relevant cases for the following case:\n\nSubject: {"MS Switchports keep flapping"}\nDescription: {"My switch is having issues"}\n\nHere are the available cases:\n"
    for case in cases:
        prompt += f"\nCase Number: {"100100"}\nSubject: {"MS Switchports keep flapping"}\nDescription: {"My switch is having issues"}\n"

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

# Example usage:
given_case = {"subject": "Network Issue", "description": "The network is down in the office."}
cases = [
    {"CaseNumber": "001", "Subject": "Network Issue", "Description": "The network is down in the office.", "Id": "a1"},
    {"CaseNumber": "002", "Subject": "Login Issue", "Description": "Unable to login to the system.", "Id": "b2"},
    {"CaseNumber": "003", "Subject": "Network Issue", "Description": "Slow internet speed.", "Id": "c3"},
    {"CaseNumber": "004", "Subject": "Hardware Issue", "Description": "The printer is not working.", "Id": "d4"},
    {"CaseNumber": "005", "Subject": "Network Issue", "Description": "Wi-Fi is not connecting.", "Id": "e5"},
]

INSTANCE_URL = "https://example.salesforce.com"
top_matches = find_top_matches_gpt(given_case, cases)
print(top_matches)



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

# Function to scrape subject and description from the case page
def scrape_case_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Debug: Print the HTML content
    print("HTML Content:", soup.prettify())
    
    # Update the selectors based on the actual HTML structure
    subject_element = soup.find('lightning-formatted-text', {'title': True})
    subject = subject_element['title'].strip() if subject_element else 'No subject found'
    
    # Update the selector for the description element
    description_element = soup.find('lightning-formatted-text', {'data-output-element-id': 'output-field'})
    description = description_element.text.strip() if description_element else 'No description found'
    
    # Debug: Print the extracted subject and description
    print("Extracted Subject:", subject)
    print("Extracted Description:", description)
    
    return subject, description

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
    given_case['subject'] = "MS Switchports keep flapping" #subject
    given_case['description'] = "My switch is having issues" #description

    # Get access token
    access_token = get_access_token()

    # Fetch cases from Salesforce
    existing_cases = fetch_cases(access_token)

    # Find top matches using GPT-3.5 or GPT-4
    top_matches = find_top_matches_gpt(given_case, existing_cases)

    return jsonify(top_matches)

if __name__ == '__main__':
    socketio.run(app, debug=True)


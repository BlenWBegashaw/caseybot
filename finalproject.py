import requests
import json
from flask import Flask, request, jsonify, render_template
from difflib import SequenceMatcher
import openai
import os

app = Flask(__name__)

# Read Salesforce credentials and OpenAI API key from environment variables
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Define constants
DOMAIN = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
OAUTH_ENDPOINT = '/services/oauth2/token'

# Function to calculate similarity between two strings
def calculate_similarity(text1: str, text2: str) -> float:
    return SequenceMatcher(None, text1, text2).ratio()

# Function to find the top N matching cases based on subject and description
def find_top_matches(given_case: dict, cases: list, top_n: int = 5) -> list:
    similarities = []
    for case in cases:
        subject_similarity = calculate_similarity(given_case["subject"], case["Subject"])
        description_similarity = calculate_similarity(given_case["description"], case["Description"])
        overall_similarity = (subject_similarity + description_similarity) / 2
        similarities.append((case, overall_similarity))

    # Sort by similarity in descending order
    sorted_cases = sorted(similarities, key=lambda x: x[1], reverse=True)
    # Return the top N matches with case number and link
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
    return render_template('file.html')

@app.route('/match_cases', methods=['POST'])
def match_cases():
    data = request.json
    given_case = data['case']

    # Get access token
    access_token = get_access_token()

    # Fetch cases from Salesforce
    existing_cases = fetch_cases(access_token)

    # Find top matches
    top_matches = find_top_matches(given_case, existing_cases)

    return jsonify(top_matches)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))

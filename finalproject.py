import requests
import json
from flask import Flask, request, jsonify, render_template
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Define constants
DOMAIN = 'https://ciscomeraki4-dev-ed.develop.my.salesforce.com'
OAUTH_ENDPOINT = '/services/oauth2/token'

# Define your Salesforce credentials
CONSUMER_KEY = '3MVG9XgkMlifdwVB7aHSFpsEfvZn554iyhEGunwebN1ImlP5XMEoK7YjGcNU2Lm9ZJUylKNLhgzkoPbuy8BPh'
CONSUMER_SECRET = 'FBEA32905771C3B4C69E8BA0DE8FD91C5C812AFA63BE46137675736792FE9EA3'
USERNAME = 'blenw@gmail.com'
PASSWORD = 'Blen1234567?'

# Function to calculate similarity between two strings using TF-IDF and cosine similarity
def calculate_similarity(text1: str, text2: str) -> float:
    if text1 is None:
        text1 = ""
    if text2 is None:
        text2 = ""
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# Function to find the top N matching cases based on subject and description
def find_top_matches(given_case: dict, cases: list, top_n: int = 5) -> list:
    similarities = []
    for case in cases:
        subject_similarity = calculate_similarity(given_case.get("subject", ""), case.get("Subject", ""))
        description_similarity = calculate_similarity(given_case.get("description", ""), case.get("Description", ""))
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
    return render_template('index.html')

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
    app.run(debug=True)

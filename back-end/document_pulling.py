import requests
import json
from datetime import datetime

# Your existing variables
TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
BASEURL = 'https://q.utoronto.ca'

# Initialize documents list
documents = []

# Common headers for all requests
headers = {
    'Authorization': f'Bearer {TOKEN}',
}

def append_announcements_to_documents(context_codes, documents, start_date=None, end_date=None):
    # Set end_date to today's date if not provided
    end_date = end_date or datetime.now().date().isoformat()
    params = {
        'context_codes[]': context_codes,
        'start_date': start_date,
        'end_date': end_date,
    }
    url = f'{BASEURL}/api/v1/announcements'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        announcements = response.json()
        for i, announcement in enumerate(announcements, start=1):
            message = announcement.get('message', 'No message available')
            documents.append({
                "title": f"{context_codes[0]} announcement {i}",
                "text": message[:1000]  # Safely handling None message
            })

def append_assignments_to_documents(course_id, documents, include=None):
    params = {}
    if include:
        params['include[]'] = include
    url = f'{BASEURL}/api/v1/courses/{course_id}/assignments'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        assignments = response.json()
        for i, assignment in enumerate(assignments, start=1):
            # Handling potential None description
            description = assignment.get('description', 'No description available') or 'No description available'
            documents.append({
                "title": f"{course_id} assignment {i}",
                "text": description[:1000]  # First 100 characters of the description
            })

def append_modules_to_documents(course_id, documents, include=None):
    params = {}
    if include:
        params['include[]'] = include
    url = f'{BASEURL}/api/v1/courses/{course_id}/modules'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        modules = response.json()
        for i, module in enumerate(modules, start=1):
            name = module.get('name', 'Unnamed module')
            documents.append({
                "title": f"{course_id} module {i}",
                "text": name[:1000]  # First 100 characters of the module name
            })

def append_submissions_to_documents(course_id, documents, include=None):
    params = {}
    if include:
        params['include[]'] = include
    url = f'{BASEURL}/api/v1/courses/{course_id}/students/submissions'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        submissions = response.json()
        for i, submission in enumerate(submissions, start=1):
            snippet = f"User {submission.get('user_id', 'Unknown user')}, grade: {submission.get('grade', 'No grade')}, score: {submission.get('score', 'No score')}"
            documents.append({
                "title": f"{course_id} submission {i}",
                "text": snippet[:1000]  # First 1000 characters of the snippet
            })

# Example usage
context_codes = ['course_333675']
course_id = '333675'

# Fetch and append data to documents
append_announcements_to_documents(context_codes, documents, start_date='2024-01-01', end_date=datetime.now().date().isoformat())
append_assignments_to_documents(course_id, documents)
append_modules_to_documents(course_id, documents, include=['items', 'content_details'])
append_submissions_to_documents(course_id, documents, include=['submission_comments', 'submission_history'])

# Print the structured documents
#print(json.dumps(documents, indent=2))

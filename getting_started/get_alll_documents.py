import requests
import json

# Your existing variables
TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
BASEURL = 'https://q.utoronto.ca'

# Common headers for all requests
headers = {
    'Authorization': f'Bearer {TOKEN}',
}

# Function to fetch announcements
def fetch_announcements(context_codes, start_date=None, end_date=None, active_only=False, latest_only=False):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
    }
    params = {
        'context_codes[]': context_codes,
        'start_date': start_date,
        'end_date': end_date,
        'active_only': active_only,
        'latest_only': latest_only
    }
    url = f'{BASEURL}/api/v1/announcements'

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch announcements. Status Code: {response.status_code}")
        print(f"Error Message: {response.text}")
        return []

def fetch_assignments(course_id, include=None):
    params = {}
    if include:
        params['include[]'] = include
    response = requests.get(f'{BASEURL}/api/v1/courses/{course_id}/assignments', headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch assignments for course {course_id}: {response.status_code}")
        return []


course_id = '333675'  # Use one of your course IDs here
assignments = fetch_assignments(course_id)
print(assignments)

def fetch_modules(course_id, include=None, search_term=None, student_id=None):
    """
    Fetches modules for a specific course from the Canvas API.

    Parameters:
    - course_id: The ID of the course.
    - include: List of additional information to include. Possible values are 'items' and 'content_details'.
    - search_term: Partial name of the modules to match and return.
    - student_id: Returns module completion information for the student with this ID.
    """
    # Constructing the request parameters
    params = {}
    if include:
        params['include[]'] = include
    if search_term:
        params['search_term'] = search_term
    if student_id:
        params['student_id'] = student_id

    # Making the GET request to the Canvas API
    response = requests.get(f'{BASEURL}/api/v1/courses/{course_id}/modules', headers=headers, params=params)

    # Checking the response status
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch modules for course {course_id}: {response.status_code}")
        print(f"Error Message: {response.text}")
        return []

# Example usage
course_id = '303385'  # Replace with the actual course ID you're interested in
modules = fetch_modules(course_id, include=['items', 'content_details'])
print(json.dumps(modules, indent=2))




# Example usage
context_codes = ['course_333675']  # Replace with your actual course IDs
announcements = fetch_announcements(context_codes, start_date='2024-01-01', end_date='2024-03-19')
#print(json.dumps(announcements, indent=2))

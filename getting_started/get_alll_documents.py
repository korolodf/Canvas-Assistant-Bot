import requests
import json
from datetime import datetime


# Your existing variables
TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
BASEURL = 'https://q.utoronto.ca'

import requests

import requests




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
course_id = '333675'  # Replace with the actual course ID you're interested in
modules = fetch_modules(course_id, include=['items', 'content_details'])
print(json.dumps(modules, indent=2))




# Example usage
context_codes = ['course_333675']  # Replace with your actual course IDs
announcements = fetch_announcements(context_codes, start_date='2024-01-01', end_date='2024-03-19')
print(json.dumps(announcements, indent=2))

def fetch_collaborations(context_type, context_id):
    """
    Fetches collaborations for a specific course or group.

    Parameters:
    - context_type: 'courses' or 'groups' depending on the context.
    - context_id: The ID of the course or group.
    """
    url = f'{BASEURL}/api/v1/{context_type}/{context_id}/collaborations'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch collaborations for {context_type} {context_id}. Status Code: {response.status_code}")
        print(f"Error Message: {response.text}")
        return []


def fetch_collaboration_members(collaboration_id, include=None):
    """
    Fetches members of a given collaboration.

    Parameters:
    - collaboration_id: The ID of the collaboration.
    - include: List of additional information to include with each member ('collaborator_lti_id', 'avatar_image_url').
    """
    params = {}
    if include:
        params['include[]'] = include

    url = f'{BASEURL}/api/v1/collaborations/{collaboration_id}/members'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch members for collaboration {collaboration_id}: {response.status_code}")
        print(f"Error Message: {response.text}")
        return []


def fetch_submissions_for_course(course_id, include=None):
    """
    Fetches all submissions for assignments in a course.

    Parameters:
    - course_id: The ID of the course.
    - include: Associations to include with the group.
    """
    # Constructing the request parameters
    params = {}
    if include:
        params['include[]'] = include

    url = f'{BASEURL}/api/v1/courses/{course_id}/students/submissions'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch submissions for course {course_id}: {response.status_code}")
        print(f"Error Message: {response.text}")
        return []

# Example usage
# Include parameters such as submission_comments, submission_history, etc., as needed
include_options = ['submission_comments', 'submission_history', 'rubric_assessment', 'assignment', 'user']
submissions = fetch_submissions_for_course(course_id, include=include_options)
print(json.dumps(submissions, indent=2))


def fetch_assignments_with_submissions_and_rubrics_v3(course_id):
    assignments_info = []
    assignments_url = f'{BASEURL}/api/v1/courses/{course_id}/assignments'
    assignments_response = requests.get(assignments_url, headers=headers)

    if assignments_response.status_code == 200:
        assignments = assignments_response.json()
        for assignment in assignments:
            assignment_detail = {
                "assignment_name": assignment['name'],
                "assignment_id": assignment['id'],
                "submissions": [],
                "rubric": []
            }

            # Check for rubric information in assignment details
            if 'rubric' in assignment:
                for rubric_criterion in assignment['rubric']:
                    assignment_detail["rubric"].append({
                        "criterion": rubric_criterion['description'],
                        "points": rubric_criterion['points']
                    })

            # Fetch submissions for the assignment
            submissions_url = f'{BASEURL}/api/v1/courses/{course_id}/assignments/{assignment["id"]}/submissions'
            submissions_response = requests.get(submissions_url, headers=headers)
            if submissions_response.status_code == 200:
                submissions = submissions_response.json()
                for submission in submissions:
                    submission_detail = {
                        "user_id": submission['user_id'],
                        "grade": submission.get('grade', 'No grade'),
                        "score": submission.get('score', 'No score'),
                        "comments": [],
                        "rubric_assessment": submission.get('rubric_assessment', {})
                    }
                    # Adding submission comments
                    if 'submission_comments' in submission:
                        for comment in submission['submission_comments']:
                            submission_detail["comments"].append({
                                "author_name": comment['author_name'],
                                "comment": comment['comment']
                            })
                    assignment_detail["submissions"].append(submission_detail)
            else:
                print(f"Failed to fetch submissions for assignment {assignment['id']}")

            assignments_info.append(assignment_detail)

    else:
        print(f"Failed to fetch assignments for course {course_id}: {assignments_response.status_code}")

    return assignments_info


# Example usage
#course_id = '333675'  # Example course ID, replace with the actual course ID you're interested in
assignments_info = fetch_assignments_with_submissions_and_rubrics_v3(course_id)

# Pretty print the collected information
print(json.dumps(assignments_info, indent=2))


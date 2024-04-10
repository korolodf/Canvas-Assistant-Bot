import requests
from datetime import datetime
import json

BASEURL = 'https://q.utoronto.ca'

def fetch_and_append_documents(api_token):
    documents = []
    headers = {
        'Authorization': f'Bearer {api_token}',
    }

    def fetch_active_courses(user_id='self'):
        url = f"{BASEURL}/api/v1/users/{user_id}/courses"
        params = {
            "enrollment_state": "active",
            "include": ["teachers"]  # You can add more if needed
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch active courses. Status Code: {response.status_code}")
            return []

    def append_course_info_to_documents(courses):
        course_details_list = []
        for i, course in enumerate(courses, start=1):
            course_id = course.get('id')
            course_name = course.get('name', 'Unnamed Course')
            course_code = course.get('course_code', 'No Course Code Available')
            start_at = course.get('start_at', 'No Start Date Available')
            end_at = course.get('end_at', 'No End Date Available')
            enrollment_term_id = course.get('enrollment_term_id', 'No Term Information Available')
            teachers = ', '.join(
                [teacher.get('display_name', 'Unnamed Teacher') for teacher in course.get('teachers', [])])

            course_detail = (
                f"{course_name} ({course_code})\n"
                f"  - Course ID: {course_id}\n"
                f"  - Start Date: {start_at}\n"
                f"  - End Date: {end_at}\n"
                f"  - Enrollment Term ID: {enrollment_term_id}\n"
                f"  - Teachers: {teachers}\n"
            )
            course_details_list.append(course_detail)

        # Join all course details into a single string
        all_course_details = "\n".join(course_details_list)
        # Append as a single document after generating the string
        documents.append({"title": "All Courses", "text": all_course_details})

    def append_announcements_to_documents(context_codes, start_date=None, end_date=None):
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

    def append_assignments_to_documents(course_id, include=None):
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

    def append_modules_to_documents(course_id, include=None):
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

    def append_submissions_to_documents(course_id, include=None):
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

    def append_user_profile_to_documents(user_id='self'):
        url = f"{BASEURL}/api/v1/users/{user_id}/profile"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            profile = response.json()
            name = profile.get('name')
            bio = profile.get('bio', 'No bio available')
            avatar_url = profile.get('avatar_url', 'No avatar URL available')
            documents.append({
                "title": f"{name}'s Profile",
                "text": f"Bio: {bio}\nAvatar URL: {avatar_url}"
            })


    # Fetch active courses for the student
    active_courses = fetch_active_courses()
    # Append as a single document
    append_course_info_to_documents(active_courses)
    append_user_profile_to_documents()

    # Loop over each course and append documents
    for course in active_courses:
        course_id = str(course['id'])
        context_codes = [f'course_{course_id}']
        append_announcements_to_documents(context_codes, start_date='2024-01-01', end_date=datetime.now().date().isoformat())
        append_assignments_to_documents(course_id)
        append_modules_to_documents(course_id, include=['items', 'content_details'])
        append_submissions_to_documents(course_id, include=['submission_comments', 'submission_history'])

    return documents

# Example usage, remove or comment out before using this script as a module.
documents = fetch_and_append_documents('11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD')
print(json.dumps(documents, indent=2))
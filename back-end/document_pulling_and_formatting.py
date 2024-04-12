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
            "include": ["teachers"]
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch active courses. Status Code: {response.status_code}")
            return []


    def append_active_courses_to_documents(courses):
        courses_details = "\n".join([f"Course Name: {course['name']}, Course Code: {course['course_code']}, Teachers: {', '.join(teacher['display_name'] for teacher in course.get('teachers', []))}"
                                        for course in courses])
        preamble = "This document contains a list of all the courses that the user is currently enrolled in:\n\n"
        documents.append({
            "title": "Active Courses",
            "text": preamble + courses_details
        })


    def append_user_profile_to_documents():
        user_id = 'self'  # Assuming 'self' is used for the current user context
        url = f"{BASEURL}/api/v1/users/{user_id}/profile"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            profile = response.json()
            name = profile.get('name')
            bio = profile.get('bio', 'No bio available')
            avatar_url = profile.get('avatar_url', 'No avatar URL available')
            preamble = f"This document contains the profile information for the current user that you are talking to, {name}.\n\n"
            profile_text = f"Bio: {bio}\nAvatar URL: {avatar_url}"
            documents.append({
                "title": f"{name}'s Profile",
                "text": preamble + profile_text
            })

    def append_course_announcements_to_documents(course_id, course_code, start_date=None, end_date=None):
        end_date = end_date or datetime.now().date().isoformat()
        params = {
            'context_codes[]': [f'course_{course_id}'],
            'start_date': start_date,
            'end_date': end_date,
        }
        url = f'{BASEURL}/api/v1/announcements'
        response = requests.get(url, headers=headers, params=params)
        announcements_text = "Announcements:\n"
        if response.status_code == 200:
            announcements = response.json()
            announcements_text += "\n".join(
                [f"{i+1}. {announcement.get('message', 'No message available')[:1000]}" for i, announcement in enumerate(announcements)]
            ) if announcements else "No announcements available."
        documents.append({
            "title": f"{course_code} Announcements",
            "text": f"This document contains all announcements for the course {course_code}.\n\n{announcements_text}"
        })

    def append_user_todo_items_to_documents():
        url = f"{BASEURL}/api/v1/users/self/todo"
        response = requests.get(url, headers=headers)
        todo_items_text = "TODO Items:\n"
        if response.status_code == 200:
            todo_items = response.json()
            if todo_items:
                for i, item in enumerate(todo_items, start=1):
                    item_type = item.get('type')
                    context_type = item.get('context_type')
                    course_id = item.get('course_id')
                    item_details = f"Item {i}: Type - {item_type}, Context - {context_type}, Course ID - {course_id}\n"

                    # Handling different item types
                    if item_type in ['grading', 'submitting']:
                        if 'assignment' in item:
                            assignment = item.get('assignment')
                            item_details += f"Assignment: {assignment.get('name', 'No name available')}, Due at: {assignment.get('due_at', 'No due date')}\n"
                        elif 'quiz' in item:
                            quiz = item.get('quiz')
                            item_details += f"Quiz: {quiz.get('title', 'No title available')}, Due at: {quiz.get('due_at', 'No due date')}\n"

                    item_details += f"HTML URL: {item.get('html_url', 'No URL available')}\n\n"
                    todo_items_text += item_details
            else:
                todo_items_text += "No TODO items available."
        else:
            todo_items_text += "Failed to fetch TODO items."

        documents.append({
            "title": "User's TODO Items",
            "text": f"This document contains the current list of TODO items for the user. These are the upcoming events that the user should work on including assignments, classes and more\n\n{todo_items_text}"
        })

    def append_course_assignments_to_documents(course_id, course_code, include=None):
        params = {'include[]': include} if include else {}
        url = f'{BASEURL}/api/v1/courses/{course_id}/assignments'
        response = requests.get(url, headers=headers, params=params)
        assignments_text = "Assignments:\n"
        if response.status_code == 200:
            assignments = response.json()
            if assignments:
                for i, assignment in enumerate(assignments, start=1):
                    # Ensure we have valid strings for name and description
                    name = assignment.get('name', 'Unnamed assignment')
                    description = assignment.get('description', 'No description available')
                    # If either is None, replace with a default text
                    name = name if name is not None else "Unnamed assignment"
                    description = description if description is not None else "No description available"
                    assignments_text += f"{i}. {name}: {description[:1000]}\n"
            else:
                assignments_text += "No assignments available."
        else:
            assignments_text += "Failed to fetch assignments."

        documents.append({
            "title": f"{course_code} Assignments",
            "text": f"This document contains all assignments for the course {course_code}.\n\n{assignments_text}"
        })

    def append_course_modules_to_documents(course_id, course_code, include=None):
        params = {'include[]': include} if include else {}
        url = f'{BASEURL}/api/v1/courses/{course_id}/modules'
        response = requests.get(url, headers=headers, params=params)
        modules_text = "Modules:\n"
        if response.status_code == 200:
            modules = response.json()
            modules_text += "\n".join(
                [f"{i+1}. {module.get('name', 'Unnamed module')}" for i, module in enumerate(modules)]
            ) if modules else "No modules available."
        documents.append({
            "title": f"{course_code} Modules",
            "text": f"This document contains all modules for the course {course_code}.\n\n{modules_text}"
        })

    def append_course_submissions_to_documents(course_id, course_code, include=None):
        params = {'include[]': include} if include else {}
        url = f'{BASEURL}/api/v1/courses/{course_id}/students/submissions'
        response = requests.get(url, headers=headers, params=params)
        submissions_text = "Submissions:\n"
        if response.status_code == 200:
            submissions = response.json()
            submissions_text += "\n".join(
                [f"{i+1}. User {submission.get('user_id', 'Unknown user')}, Grade: {submission.get('grade', 'No grade')}, Score: {submission.get('score', 'No score')}" for i, submission in enumerate(submissions)]
            ) if submissions else "No submissions available."
        documents.append({
            "title": f"{course_code} Submissions",
            "text": f"This document contains all submissions for the course {course_code}.\n\n{submissions_text}"
        })

    # Functions for modules and submissions follow a similar pattern to assignments and announcements

    active_courses = fetch_active_courses()
    append_active_courses_to_documents(active_courses)
    append_user_profile_to_documents()
    append_user_todo_items_to_documents()
    for course in active_courses:
        course_id = str(course['id'])
        course_code = course.get('course_code', 'No Course Code Available')
        # Append course information documents
        append_course_announcements_to_documents(course_id, course_code, start_date='2024-01-01', end_date=datetime.now().date().isoformat())
        append_course_assignments_to_documents(course_id, course_code)
        append_course_modules_to_documents(course_id, course_code)  # Now included
        append_course_submissions_to_documents(course_id, course_code)  # Now included



    return documents

#documents = fetch_and_append_documents('11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD')
#print(json.dumps(documents, indent=2))

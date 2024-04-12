import canvasapi

TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
BASEURL = 'https://q.utoronto.ca'

canvas_api = canvasapi.Canvas(BASEURL, TOKEN)
result = canvas_api.get_user('self')
courses = canvas_api.get_courses(enrollment_state='active')

course_list = []
for course in courses:
    try:
        course_list.append(course.course_code)
    except AttributeError:
        continue

print(course_list)
#documents = [{'title': f'Document {i+1}', 'snippet': string} for i, string in enumerate(course_list)]
#user_request = input("Hello there, what can I help you with?")
#user_request = "What courses am I enrolled in?"

#course = 'INF412H1 S LEC0101'
print(course)
assignments = courses[1].get_assignments()
for assignment in assignments:
    print(assignment)


result = canvas_api.get_user('self')

print(result)

import json

# getpass and input are simple ways to get user input
import getpass

import requests
import pandas as pd
from builtins import input

# Static settings
# Using a base urls is useful for switching between test and production environments easily
PER_PAGE = 100

# User input settings
# token should be treated as a password (not visible when typed)
while not TOKEN:
    TOKEN = getpass.getpass('Enter your access token:')
auth_header = {'Authorization': 'Bearer ' + TOKEN} # setup the authorization header to be used later

# require the course state to be provided
course_state = None
while not course_state in ['unpublished', 'available', 'completed', 'deleted']:
    course_state = input("Select a course state [unpublished, available, completed, deleted]:")


print("Finding courses...")
print("-----------------------------")
# continue to make requests until all data has been received
page = 1
courses = []
while True:
    # request urls should always be based of the base url so they do not
    # need to be changed when switching between test and production environments
    request_url = BASEURL + '/api/v1/courses'
    params = {
        "per_page": str(PER_PAGE),
        "page": str(page),
        "state[]": [course_state],
        "include[]": ['total_students']
    }
    r = requests.get(request_url, headers=auth_header, params=params)

    # always take care to handle request errors
    r.raise_for_status() # raise error if 4xx or 5xx

    data = r.json()
    if len(data) == 0:
        break

    courses += data

    print("Finished processing page: "+str(page))
    page+=1

if len(courses) == 0:
    print("No courses found to report on.")
    exit()

# from here, a simple table is printed out
# using pandas for convenience
print("Report for "+str(len(courses)) + " courses.")
print("-----------------------------")

courses_df = pd.DataFrame(courses)
result = courses_df.to_string(
    columns=['id', 'name', 'course_code', 'workflow_state', 'start_at', 'end_at', 'total_students']
)
print(result)

import dotenv
import os
import canvasapi

#dotenv.load_dotenv(dotenv.find_dotenv())
#TOKEN = os.environ.get('CANVAS_API_TOKEN')

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


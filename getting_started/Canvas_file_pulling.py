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
import canvasapi
import cohere

co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
BASEURL = 'https://q.utoronto.ca'

canvas_api = canvasapi.Canvas(BASEURL, TOKEN)
result = canvas_api.get_user('self')
courses = canvas_api.get_courses(enrollment_state='active')

#get course information
course_list = []
for course in courses:
    try:
        course_list.append(course.course_code)
    except AttributeError:
        continue

documents = [{'title': f'Document {i+1}', 'snippet': string} for i, string in enumerate(course_list)]
print(course_list)
#user_request = input("Hello there, what can I help you with?")
#user_request = "How many courses am I enrolled in? Just give me the number"


rag_response = co.chat(
  model="command",
  message= user_request,
  documents= documents
  )

print(rag_response.text)

user_request2 = input("Is there anything else I can help you with?")
#user_request = " What are the rest of the courses I am enrolled in?"

rag_response = co.chat(
  model="command",
  message= user_request2,
  documents= documents
  )
print(rag_response.text)

import canvasapi
import cohere


def chatbot_response(user_request):
  co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')
  TOKEN = '11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD'
  BASEURL = 'https://q.utoronto.ca'
  canvas_api = canvasapi.Canvas(BASEURL, TOKEN)
  result = canvas_api.get_user('self')
  courses = canvas_api.get_courses(enrollment_state='active')
  course_list = []
  for course in courses:
      try:
          course_list.append(course.name)
      except AttributeError:
          continue
  documents = [{'title': f'Document {i+1}', 'snippet': string} for i, string in enumerate(course_list)]

  rag_response = co.chat(
      model="command",
      message=user_request,
      documents=documents
  )
  return rag_response.text  # Return the response text instead of printing it

def chatting():
    user_req = input("Hello there, what can I help you with?")
    stop = False
    while not stop:
        print(chatbot_response(user_req))
        user_req = input("Anything else I can help you with? Say 'No' to end session")
        if user_req == 'No' or user_req == 'no':
            stop = True

chatting()
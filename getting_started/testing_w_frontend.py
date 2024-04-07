import canvasapi
import cohere
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    return rag_response.text

@app.route('/chatbot', methods=['GET', 'POST'])  # Only allow POST requests
def handle_chatbot_request():
    if request.method == 'POST':
        # Handle POST request
        user_request = request.json['message']
        response_text = chatbot_response(user_request)
        return jsonify({'response': response_text})
    elif request.method == 'GET':
        # Handle GET request (if necessary)
        return 'This is the chatbot endpoint. Send a POST request with a "message" parameter to get a response.'

    
#@app.route('/')
#def home():
#    return 'Welcome to my Flask application!'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
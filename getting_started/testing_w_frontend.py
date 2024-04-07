import canvasapi
import cohere
from flask import Flask, request, jsonify
from flask_cors import CORS
import markdown2

app = Flask(__name__)
CORS(app)

chatterbox_preamble = '''

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
Be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.
Use bulleted lists when appropriate, like listing things, making sure to start a new line with every item.
'''

def chatbot_response(user_request, access_token):
    co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')
    BASEURL = 'https://q.utoronto.ca'
    canvas_api = canvasapi.Canvas(BASEURL, access_token)
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
        documents=documents,
        preamble=chatterbox_preamble,
        temperature=0.8
    )
    response_html = markdown2.markdown(rag_response.text)

    return response_html

@app.route('/chatbot', methods=['GET', 'POST'])  # Only allow POST requests
def handle_chatbot_request():
    if request.method == 'POST':
        # Extract data from the request
        request_data = request.json
        user_request = request_data.get('message')
        access_token = request_data.get('access_token')
        
        # Call the chatbot function with the user's message and access token
        response_text = chatbot_response(user_request, access_token)
        
        # Return the response as JSON
        return jsonify({'response': response_text})
    elif request.method == 'GET':
        # Handle GET request (if necessary)
        return 'This is the chatbot endpoint. Send a POST request with a "message" parameter to get a response.'
    else:
        return 'Method Not Allowed', 405
    
#@app.route('/')
#def home():
#    return 'Welcome to my Flask application!'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
"""

Faculty of Information
University of Toronto
Bachelor of Information
INF453: Capstone Project
Instructor: Dr Maher Elshakankiri
Supervisor: Dr Rohan Alexander
Names: Jayden Jung, Finn Korol-O'Dwyer, Sofia Sellitto
Date created: March 10, 2024
Date last modified: April 10, 2024

This Flask application serves as a chatbot interface named 'Chatterbox', designed specifically for students at the University of Toronto using the Canvas (Quercus) educational platform. The chatbot utilizes the cohere.ai API to rerank and reformat academic documents pulled from Canvas, offering a conversational interface for students to query academic information.

Inputs:
- access_token: A string token used to authenticate with the Canvas API.
- user_request: A string containing the user's query or request.

Outputs:
- A JSON object containing the HTML formatted response from the chatbot, which includes information from academic documents such as course details, assignments, and user profile, contextualized to the user's queries.

Key Features:
- The chatbot leverages the Cohere API to process academic documents for relevant information based on user queries.
- The Flask application supports POST requests where the user can submit their queries and receive formatted responses.
- CORS (Cross-Origin Resource Sharing) is enabled to allow web-based clients to interact with the API seamlessly.
- The chatbot maintains a history of conversation to provide context for better responses and limits the conversation to a maximum of 10 turns to prevent abuse.

The application primarily uses endpoints for handling chatbot interactions, ensuring that responses are relevant and contextually accurate based on the documents retrieved from the user's Canvas account and the chatbot's defined conversational guidelines.

"""


import cohere
import re
import markdown2
import canvasapi
from flask import Flask, request, jsonify
from flask_cors import CORS
#from document_pulling import fetch_and_append_documents
from document_pulling_and_formatting import fetch_and_append_documents
app = Flask(__name__)
CORS(app)

# providing API token and creating a custom preamble for the chatbot
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')
chatterbox_preamble = '''

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English spelling for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
Your response will be returned as HTML so make sure to always include formatting for text in this format.
When you are prompted to provide information, be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.
Be helpful and suggest on further information that you could help the user with. 
When providing a list of things, always use bulleted lists, and again remember to use markdown/HTML formatting. This might be listing courses or assignments or due dates. 

## Additional Considerations
Pull from the user profile document when you begin speaking with a user to address them by name. When asked about assignments, refer to documents for both assignments and submissions. 
Note that real course codes are 3 capital letters followed by 3 numbers, and then H1 (Example: ABC123H1). If asked about courses, ignore information about courses that aren't in this format. DO NOT MENTION COURSES THAT AREN'T IN THIS FORMAT. 
When pulling on documents about Announcements, recognize that relative mentions of time like "today" and "this week" are based on the date that the announcement was made, not the current date in reality. Avoid using future tense to refer to things that are coming up according to announcements, as there's the chance that it is only future-relative to the dat of the announcement. 
'''

chat_history = []
max_turns = 10

# Rerank and reformat function based on provided documents and user request
def rerank_reformat(docs, user_request):
    #Rerank documents according to user request
    reranked_documents = co.rerank(model="rerank-english-v2.0", query=user_request, documents=docs, top_n=10)

    # Convert the reranked_results object to a string
    reranked_results_str = str(reranked_documents)

    # Define a regex pattern to capture the document text
    # Adjust the pattern if necessary to correctly match your data structure
    pattern = r"document\['text'\]: (.*?)>, RerankResult<"

    # Use re.findall() to find all matches of the pattern
    # Note: The regex might need adjustment based on the exact format of the stringified reranked_results
    matches = re.findall(pattern, reranked_results_str)

    # Format the extracted text into the specified structure
    formatted_data = [{"title": f"Result {index + 1}", "snippet": match} for index, match in enumerate(matches)]

    return formatted_data

def rerank_reformat_new(docs, user_request):
    reranked_documents = co.rerank(model="rerank-english-v2.0", query=user_request, documents=docs, return_documents=True, top_n=10)
    reformatted_documents = []
    for idx, r in enumerate(reranked_documents.results):
        reformatted_documents.append({'text': r.document.text})

    return(reformatted_documents)

# Generate chatbot response function based on provided documents and user request
def chatbot_response(docs, user_request):
    rag_response = co.chat(
        model="command-r-plus",
        message=user_request,
        documents=docs,
        preamble=chatterbox_preamble,
        chat_history=chat_history,
        temperature=0.8
    )
    response_html = markdown2.markdown(rag_response.text)

    return response_html

# FOR TESTING
def make_test_doc(access_token):
    co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')
    BASEURL = 'https://q.utoronto.ca'
    canvas_api = canvasapi.Canvas(BASEURL, access_token)
    courses = canvas_api.get_courses(enrollment_state='active')
    course_list = []
    for course in courses:
        try:
            course_list.append(f'{course.course_code}: {course.name}')
        except AttributeError:
            continue
    documents = [{'title': f'Course {i+1}', 'text': string} for i, string in enumerate(course_list)]

    return documents
#test_doc = make_test_doc('11834~AXJ7biYxaQiuIwUcz3kkkuEXlIJjD6WRF2LtVDfElrsMWw6DGmEb24GRvH9cHFHD')
#test_doc.append({'title': 'blah blah this is not important', 'text': 'woopdeedoo'})
#test_doc.append({'title': 'user profile', 'text': 'Name: Jayden Jung'})
#print(test_doc)
#print('-----')

# Create Flask App to handle chatbot conversation
@app.route('/chatbot', methods=['GET', 'POST'])  # Only allow POST requests
def handle_chatbot_request():
    global chat_history 
    if len(chat_history) >= max_turns:
        return jsonify({'response': 'Max turns reached. Cannot continue chat.'}), 400
    
    if request.method == 'POST':
        # Extract data from the request
        request_data = request.json
        user_request = request_data.get('message')
        access_token = request_data.get('access_token')
        
        # Call the chatbot function with the user's message and access token
        documents = fetch_and_append_documents(access_token)
        rankeddocuments = rerank_reformat_new(documents, user_request)
        response_text = chatbot_response(rankeddocuments, user_request)
        
        # Update the chat history with user's message and bot's response
        chat_history.append({'role': 'USER', 'text': user_request})
        chat_history.append({'role': 'BOT', 'text': response_text})

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
    app.run(port=4000, debug=True)
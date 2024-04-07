import cohere
import re
import markdown2
from flask import Flask, request, jsonify
from flask_cors import CORS
from document_pulling import pull_all_documents

app = Flask(__name__)
CORS(app)

co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

chatterbox_preamble = '''

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English spelling for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
When you are prompted to provide information, be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.
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

# Generate chatbot response function based on provided documents and user request
def chatbot_response(docs, user_request):
    rag_response = co.chat(
        model="command",
        message=user_request,
        documents=docs,
        preamble=chatterbox_preamble,
        temperature=0.8
    )
    response_html = markdown2.markdown(rag_response.text)

    return response_html

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
        documents = pull_all_documents(access_token)
        documents = rerank_reformat(documents, user_request)
        response_text = chatbot_response(documents, user_request)
        
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
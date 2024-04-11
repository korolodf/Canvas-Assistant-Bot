#from document_pulling import documents
from document_pulling_and_formatting import documents
import cohere

user_request = "what courses am I in?"
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')


# Prepare documents for the `rerank` function
# Extracting the "snippet" for each document as the text content
docs_for_rerank = [doc["text"] for doc in documents]

# Use the rerank model to rerank the documents based on the query
reranked_documents = co.rerank(model="rerank-english-v2.0", query=user_request, documents=docs_for_rerank, return_documents=True, top_n=10)

print(reranked_documents)
print('------')

# Extracting necessary information from reranked_documents
import re
import json

#def save_documents_to_json(docs):
    #documents = []
    
documents = []
for idx, r in enumerate(reranked_documents.results):
    documents.append({'text': r.document.text})
print(documents)

#formatted_documents = save_documents_to_json(reranked_documents)

#print(formatted_documents)
#print('------')

def format_rerank_results_as_json(reranked_results):
    # Convert the reranked_results object to a string
    reranked_results_str = str(reranked_results)

    # Define a regex pattern to capture the document text
    # Adjust the pattern if necessary to correctly match your data structure
    pattern = r"document\['text'\]: (.*?)>, RerankResult<"

    # Use re.findall() to find all matches of the pattern
    # Note: The regex might need adjustment based on the exact format of the stringified reranked_results
    matches = re.findall(pattern, reranked_results_str)

    # Format the extracted text into the specified structure
    formatted_data = [{"title": f"Result {index + 1}", "snippet": match} for index, match in enumerate(matches)]

    return formatted_data


# Assuming reranked_documents is your variable holding the results from co.rerank
#reranked_documents_str = str(reranked_documents)
#rag_format_documents = format_rerank_results_as_json(reranked_documents_str)
#print(rag_format_documents)

# print(json.dumps(rag_format_documents, indent=2))

# print(json.dumps(rag_format_documents, indent=2))

#print(json.dumps(rag_format_documents, indent=2))


chatterbox_preamble = '''

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
When you are prompted to provide information, be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.

## Additional Considerations
Pull from the user profile document when you begin speaking with a user to address them by name. When asked about assignments, refer to documents for both assignments and submissions. 
Note that actual course codes are 3 capital letters followed by 3 numbers, and then H1 (Example: ABC123H1). If asked about courses, ignore information about courses that aren't in this format.
'''
# Then you can proceed with your API call that requires JSON serializable input
# Example RAG model call (assuming it expects a list of strings)
rag_response = co.chat(
    model="command-r-plus",
    message=user_request,
    documents=documents,  # Using the list of strings
    preamble=chatterbox_preamble,
    temperature=0.8
)

print(rag_response.text)
# Continue with your logic, potentially printing rag_response or further processing it
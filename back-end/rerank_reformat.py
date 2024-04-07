from document_pulling import documents
import re

import cohere

user_request = "what's your name"
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

import cohere
import json

# Prepare documents for the `rerank` function
# Extracting the "snippet" for each document as the text content
docs_for_rerank = [doc["text"] for doc in documents]

# Use the rerank model to rerank the documents based on the query
reranked_documents = co.rerank(model="rerank-english-v2.0", query=user_request, documents=docs_for_rerank, top_n=10)

#print(reranked_documents)

# Extracting necessary information from reranked_documents
import re
import json


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
reranked_documents_str = str(reranked_documents)
rag_format_documents = format_rerank_results_as_json(reranked_documents_str)


#print(json.dumps(rag_format_documents, indent=2))

chatterbox_preamble = '''

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
When you are prompted to provide information, be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.
'''
# Then you can proceed with your API call that requires JSON serializable input
# Example RAG model call (assuming it expects a list of strings)
rag_response = co.chat(
    model="command-r-plus",
    message=user_request,
    documents=rag_format_documents,  # Using the list of strings
    preamble=chatterbox_preamble,
    temperature=0.8
)

print(rag_response.text)
# Continue with your logic, potentially printing rag_response or further processing it


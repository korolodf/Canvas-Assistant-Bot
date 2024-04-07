from document_pulling import documents

import cohere

user_request = 'Hi tell me about my most recent assignments'
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

import cohere
import json

# Prepare documents for the `rerank` function
# Extracting the "snippet" for each document as the text content
docs_for_rerank = [doc["snippet"] for doc in documents]

# Use the rerank model to rerank the documents based on the query
reranked_documents = co.rerank(
  model='rerank-english-v2.0',
  query=user_request,
  documents=docs_for_rerank,
  top_n=3  # Adjust `top_n` as needed
)

# The `rerank` function returns a Cohere object. Extract the reranked documents texts.
top_documents = [doc.text for doc in reranked_documents.documents]

# If needed, convert the top_documents back to the original format for the RAG model
formatted_documents = [{"title": f"Result {i+1}", "snippet": doc} for i, doc in enumerate(top_documents)]

# Now, you can use the formatted, reranked documents in the RAG model or any subsequent operation
# Example (assuming your model supports this format directly):
rag_response = co.chat(
  model="command",  # Ensure this is the correct model you intend to use
  message=user_request,
  documents=formatted_documents
)

print(rag_response)


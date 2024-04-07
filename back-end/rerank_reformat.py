from document_pulling import documents
import cohere

user_request = "what's your name"
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')


# Prepare documents for the `rerank` function
# Extracting the "snippet" for each document as the text content
docs_for_rerank = [doc["text"] for doc in documents]

# Use the rerank model to rerank the documents based on the query
reranked_documents = co.rerank(model="rerank-english-v2.0", query=user_request, documents=docs_for_rerank, top_n=10)

print(reranked_documents)

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


print(json.dumps(rag_format_documents, indent=2))



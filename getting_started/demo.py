import cohere
import json
import re

def extract_sentences(input_string):
  # Define a pattern that accurately captures sentences between the specified boundaries
  pattern = r"document\['text'\]: (.*?)(?=, index)"

  # Use re.findall() to find all matches of the pattern
  sentences = re.findall(pattern, input_string)

  # Format the extracted sentences into the specified structure
  formatted_data = [{"title": f"Result {index + 1}", "snippet": sentence} for index, sentence in enumerate(sentences)]

  return formatted_data

#user_request = str(input("What course information are you looking for?"))
user_request = 'name some islands in the Pacific Ocean'
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

docs = ['Carson City is the capital city of the American state of Nevada.',
'The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.',
'Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.',
'Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.']

# https://docs.cohere.com/docs/reranking
documents = co.rerank(
  model = 'rerank-english-v2.0',
  query = user_request,
  documents = docs,
  top_n = 3,
)

string_documents = str(documents)
#print(type(string_documents))
#print(string_documents)

json_documents = extract_sentences(string_documents)
#print(json_documents)
#print(type(json_documents))

# https://docs.cohere.com/docs/retrieval-augmented-generation-rag
rag_response = co.chat(
  model="command",
  message= user_request,
  documents= json_documents
  )
print(rag_response)
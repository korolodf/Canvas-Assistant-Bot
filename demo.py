import cohere
import json

class RerankResult:
  def __init__(self, text, index, relevance_score):
    self.document = {'text': text}
    self.index = index
    self.relevance_score = relevance_score


def convert_to_json(results):
  # Convert the list of RerankResult objects into a list of dictionaries
  results_list = [
    {
      "text": result.document['text'],
      "index": result.index,
      "relevance_score": result.relevance_score
    }
    for result in results
  ]

  # Convert the list of dictionaries into a JSON string
  json_str = json.dumps(results_list, indent=2)
  return json_str

#user_request = str(input("What course information are you looking for?"))
user_request = 'name some islands in the Pacific Ocean'
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

docs = ['Carson City is the capital city of the American state of Nevada.',
'The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.',
'Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.',
'Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.']

documents = co.rerank(
  model = 'rerank-english-v2.0',
  query = user_request,
  documents = docs,
  top_n = 3,
)

string_documents = str(documents)
print(type(string_documents))
print(string_documents)


co.chat(
  model="command",
  message= user_request,
  documents= string_documents
  )

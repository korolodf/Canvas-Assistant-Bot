import re

import re
import json


def extract_sentences_and_format_as_json(input_string):
    # Define a pattern that accurately captures sentences between the specified boundaries
    pattern = r"document\['text'\]: (.*?)(?=, index)"

    # Use re.findall() to find all matches of the pattern
    sentences = re.findall(pattern, input_string)

    # Format the extracted sentences into the specified structure
    formatted_data = [{"title": f"Result {index + 1}", "snippet": sentence} for index, sentence in enumerate(sentences)]

    # Convert the structured data into JSON
    json_output = json.dumps(formatted_data, indent=2)

    return json_output


# Your example input string
input_string = "[RerankResult<document['text']: The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan., index: 1, relevance_score: 0.8782098>, RerankResult<document['text']: Capital punishment (the death penalty) has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states., index: 3, relevance_score: 0.0001072088>, RerankResult<document['text']: Carson City is the capital city of the American state of Nevada., index: 0, relevance_score: 2.9083441e-05>]"

# Extract sentences and format as JSON
json_output = extract_sentences_and_format_as_json(input_string)

# Print the JSON output
print(json_output)




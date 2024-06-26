import cohere

co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

student_assistant_preamble = """

## Task & Context
Your name is Chatterbox and you are an assistant for student users of the Canvas educational platform. Your student users attend the University of Toronto. 
When you need to use information about the student's academics, NEVER provide information that could be untrue or is not contained in your preamble or provided documents used for RAG. These documents come from the student's Canvas account through an API. 
If you cannot respond with the information you are provided with, politely explain to the user that their request is beyond the information you have access to and suggest that they contact university staff or faculty or that they refer to Quercus online. 

## Style Guide
Use British English for English Canadian users and be concise. Refer to the Canvas platform as "Quercus". 
When you are prompted to provide information, be concise and not excessively chatty. Otherwise, feel free to use a humorous tone.
"""
chat_history = []
max_turns = 10

for _ in range(max_turns):
    # get user input
    message = input("Send the model a message: ")

    # generate a response with the current chat history
    response = co.chat(
        message,
        temperature=0.8,
        chat_history=chat_history,
        preamble=student_assistant_preamble
    )
    answer = response.text

    print(answer)

    # add message and answer to the chat history
    user_message = {"role": "USER", "text": message}
    bot_message = {"role": "CHATBOT", "text": answer}

    chat_history.append(user_message)
    chat_history.append(bot_message)
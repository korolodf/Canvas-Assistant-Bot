import cohere
co = cohere.Client('pmQOVGoamfrq67yp4AaqAvsjAKcm1GIRodB27aFy')

documents=[
    {"title": "Tall penguins", "snippet": "Emperor penguins are the tallest."},
    {"title": "Penguin habitats", "snippet": "Emperor penguins only live in Antarctica."},
    {"title": "What are animals?", "snippet": "Animals are different from plants."}
  ]

print(type(documents))
#response = co.chat(
#  model="command",
#  message="Where do the tallest penguins live?",
#  documents=[
#    {"title": "Tall penguins", "snippet": "Emperor penguins are the tallest."},
#    {"title": "Penguin habitats", "snippet": "Emperor penguins only live in Antarctica."},
#    {"title": "What are animals?", "snippet": "Animals are different from plants."}
#  ])

#print(response)
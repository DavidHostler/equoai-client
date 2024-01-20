from equodb.documentation import equoai_db
from sentence_transformers import SentenceTransformer 

db = equoai_db('WMuj4foGHbhZdLB6rdxf1QQrsddyA5Mo')
print('Success!')

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# equodb.create_vector_s
query = [  "Canada is one of Britain's oldest former colonies",
           "Lamb of God is an awesome heavy metal band. Black Veil Brides isn't as great.", 
           "Pineapples definitely belong on pizza", 
           "Jojo's bizarre adventure is one of the greatest animes of all time.", 
           "I had the best service at Starbucks of any place!",
           "Do we really need to go to work today?"]

#Obtain embeddings and convert from ndarray to Python list
embeddings = model.encode(query)
embeddings = embeddings.tolist()
#This will also overwrite an existing project of the same name
project_name='production'

db.create_new_project(query, embeddings,project_name)



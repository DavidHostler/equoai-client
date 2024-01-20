from equodb.documentation import equoai_db

query = "What is one of Britain's oldest colonies?"

from equodb.documentation import equoai_db
from sentence_transformers import SentenceTransformer 

db = equoai_db('WMuj4foGHbhZdLB6rdxf1QQrsddyA5Mo')
print('Success!')

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
 

#Obtainquery_embeddings and convert from ndarray to Python list
query_embeddings = model.encode(query)
query_embeddings = query_embeddings.tolist()
#This will also overwrite an existing project of the same name
project_name='production'

query_results = db.similarity_search(query, query_embeddings, project_name, top_k=3)
print('similarity search results: ', query_results)


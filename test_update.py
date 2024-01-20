# from equodb.documentation import equoai_db
# from sentence_transformers import SentenceTransformer 

# db = equoai_db('WMuj4foGHbhZdLB6rdxf1QQrsddyA5Mo')
# print('Success!')

# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# # equodb.create_vector_s
# update_to_vector_index = ["The Battle of Stalingrad was the single most apocalyptic conflict in military history."]

# # #Obtain embeddings and convert from ndarray to Python list

# #This will also overwrite an existing project of the same name
# project_name='production'

# embeddings = model.encode(update_to_vector_index)
# embeddings = embeddings.tolist()

# # db.update(update_to_vector_index, embeddings, project_name)
# #Query the existing vector index to check that the update took place successfully.
# query = "What was the single most apocalyptic event in military history?"
# query_embeddings = model.encode(query)
# query_embeddings = query_embeddings.tolist()

# query_results = db.get(query, query_embeddings, project_name, top_k=3)

# snippets = query_results['documents']

# context = model.encode(snippets).tolist()

# (best_document, highest_similarity, dp) = db.dynamic_retrieval(query_embeddings, context, snippets)

# print(highest_similarity, best_document, dp)

# # context = model.encode(query_results['documents'])

# # '''Perform a dynamic retrieval to combine documents by relevance'''

# # context = query_results
# # best_combo = db.dynamic_retrieval(
# #                     query=query_embeddings,
# #                     context=context, 
# #                     snippets=query_results['documents'],
# #                     optimized=False,
# #                     threshold=0.0
# #                 )
# # print(best_combo)
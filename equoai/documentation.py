#PURPOSE: Write a Python package to enable API calls to do the following:
'''
1. Access or create a Vector DB pod.
    A. Attempt to create a vector database through the EquoAI platform programmatically;
    Requires API KEY, which can be obtained from Landing Page 
    (Add a feature for generating unique API keys for registered users of the platform.)
    B. Access existing pod, using unique user developer API_KEY and POD_ID.
2. Store and query data (to and from!) the pod. 
We may add a data deletion feature if desired (basically removal of a node from a BST-
normally this algorithm is doable albeit quite tricky.)
'''

import os 
import requests
import sentence_transformers
import tiktoken


class equodb:
# class EquoDB:
    def __init__(self,api_key):
        self.api_key=api_key
        self.model = sentence_transformers.SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.tokenizer="gpt-3.5-turbo"
    def get_num_tokens(self,query_sentences):
        token_encoding = tiktoken.encoding_for_model(self.tokenizer)
        num_tokens = []
        for i in range(len(query_sentences)):
            token_count = len(token_encoding.encode(query_sentences[i]))
            num_tokens.append(token_count)
        return num_tokens
    #Let devs be creative by enabling them to name their own projects.
    #This method is useful for 2 tasks:
    #I. Creating a brand new vector store project 
    #II. Overwriting an existing vector store project.
    def create_new_project(self, query, project_title):
        query_embeddings = self.model.encode(query)
        #Mitigate the following serialization error by converting to list:
        #TypeError: Object of type ndarray is not JSON serializable
        query_embeddings = query_embeddings.tolist()
        tokens_in = self.get_num_tokens(query)
        # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
        url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
        project_name =  project_title
        obj = {
            'query_sentences':query,#Stores array of strings
            'query_embeddings':query_embeddings,
            'num_input_tokens':tokens_in,
            'api_key':self.api_key,
            # 'api_key':api_key,
            'pod_id': project_name,
            'is_query':False,
            'create_new_project':True,
            'top_k':0
        }
        r = requests.post(url, json=obj)
        print(r.json())
        return r.json()
    #Request data from 
    def similarity_search(self, query, project_title, top_k=5):
        # url = 'http://192.168.0.26:5000/query'
        # url = 'http://127.0.0.1:5000/query'
        query_embeddings = self.model.encode(query)
        #Mitigate the following serialization error by converting to list:
        #TypeError: Object of type ndarray is not JSON serializable
        query_embeddings = query_embeddings.tolist()
        # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
        url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
        project_name =  project_title
        tokens_in = self.get_num_tokens(query) 
        obj = {
            'query_sentences':query,#Stores array of strings
            'query_embeddings':query_embeddings,
            'num_input_tokens':tokens_in,#
            'api_key':self.api_key,
            # 'api_key':api_key,
            'pod_id': project_name,
            'is_query':True,
            'create_new_project':False,
            'top_k':top_k
        }
        r = requests.post(url, json=obj)
        # print(r.json())
        k_most_similar_results = r.json()['documents']
        return k_most_similar_results
    def update_embeddings(self, query, project_title):
        query_embeddings = self.model.encode(query)
        #Mitigate the following serialization error by converting to list:
        #TypeError: Object of type ndarray is not JSON serializable
        query_embeddings = query_embeddings.tolist()
        # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
        url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
        project_name =  project_title
        tokens_in = self.get_num_tokens(query)
        obj = {
            'query_sentences':query,#Stores array of strings
            'query_embeddings':query_embeddings,
            'num_input_tokens':tokens_in,#
            'api_key':self.api_key,
            # 'api_key':api_key,
            'pod_id': project_name,
            'is_query':False,
            'create_new_project':False,
            'top_k':0

        }
        r = requests.post(url, json=obj)
        print(r.json())
        return r.json()
# class equodb:
# # class EquoDB:
#     def __init__(self,api_key):
#         self.api_key=api_key
#         self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#         self.tokenizer="gpt-3.5-turbo"
#     def get_num_tokens(self,query_sentences):
#         token_encoding = tiktoken.encoding_for_model(self.tokenizer)
#         num_tokens = []
#         for i in range(len(query_sentences)):
#             token_count = len(token_encoding.encode(query_sentences[i]))
#             num_tokens.append(token_count)
#         return num_tokens
#     #Let devs be creative by enabling them to name their own projects.
#     def create_new_project(self, query,  project_title):
#         query_embeddings = self.model.encode(query)
#         #Mitigate the following serialization error by converting to list:
#         #TypeError: Object of type ndarray is not JSON serializable
#         query_embeddings = query_embeddings.tolist()
#         tokens_in = self.get_num_tokens(query)
#         # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
#         url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
#         project_name =  project_title
#         obj = {
#             'query_sentences':query,#Stores array of strings
#             'query_embeddings':query_embeddings,
#             'num_input_tokens':tokens_in,
#             'api_key':self.api_key,
#             # 'api_key':api_key,
#             'pod_id': project_name,
#             'is_query':False,
#             'create_new_project':True,
#             'top_k':0
#         }
#         r = requests.post(url, json=obj)
#         print(r.json())
#         return r.json()
#     #Request data from 
#     def similarity_search(self, query, project_title, top_k=5):
#         # url = 'http://192.168.0.26:5000/query'
#         # url = 'http://127.0.0.1:5000/query'
#         query_embeddings = self.model.encode(query)
#         #Mitigate the following serialization error by converting to list:
#         #TypeError: Object of type ndarray is not JSON serializable
#         query_embeddings = query_embeddings.tolist()
#         # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
#         url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
#         project_name =  project_title
#         tokens_in = self.get_num_tokens(query) 
#         obj = {
#             'query_sentences':query,#Stores array of strings
#             'query_embeddings':query_embeddings,
#             'num_input_tokens':tokens_in,#
#             'api_key':self.api_key,
#             # 'api_key':api_key,
#             'pod_id': project_name,
#             'is_query':True,
#             'create_new_project':False,
#             'top_k':top_k
#         }
#         r = requests.post(url, json=obj)
#         print(r.json())
#         return r.json()
#     def update_embeddings(self, query, project_title):
#         query_embeddings = self.model.encode(query)
#         #Mitigate the following serialization error by converting to list:
#         #TypeError: Object of type ndarray is not JSON serializable
#         query_embeddings = query_embeddings.tolist()
#         # url = 'http://10.0.0.132:5000/query' #Localhost testing purposes
#         url = 'https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query'
#         project_name =  project_title
#         tokens_in = self.get_num_tokens(query)
#         obj = {
#             'query_sentences':query,#Stores array of strings
#             'query_embeddings':query_embeddings,
#             'num_input_tokens':tokens_in,#
#             'api_key':self.api_key,
#             # 'api_key':api_key,
#             'pod_id': project_name,
#             'is_query':False,
#             'create_new_project':False,
#             'top_k':0

#         }
#         r = requests.post(url, json=obj)
#         print(r.json())
#         return r.json()
        # return 200#If API CALL succeeded.
        # 'u0YQoEwcl23O2mW0GqAzJ2bPsoAfFRjB'

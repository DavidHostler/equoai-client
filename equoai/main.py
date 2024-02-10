#PURPOSE: Write a Python package to enable API calls to do the following:
'''
1. Access or create a Vector DB pod.
    A. Attempt to create a vector database through the EquoAI platform programmatically;
    Requires API KEY, which can be obtained from Landing Page 
    (Add a feature for generating unique API keys for registered users of the platform.)
    B. Access existing pod, using unique user developer API_KEY and POD_ID.
2. Store and query data (to and from!) the pod. 
We may add a data deletion feature if desired (basically removal of a Node from a BST-
normally this algorithm is doable albeit quite tricky.)
'''

import requests
import numpy as np
import tiktoken

class equonode:
    '''
        Singleton class designed to enable communication with all developer-facing services.
    '''
    def __init__(self,api_key:str, URI="https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query"):
        self.api_key=api_key
        self.tokenizer="gpt-3.5-turbo"
        self.__URI = URI#"https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query"#generate_resource() #Resource attribute protected via Encapsulation 
        self.PATH = None#os.getcwd() #Get path of current project directory 
    
    def get_num_tokens(self,query_sentences:'list[str]')->'list[int]':
        '''
            Count the number of tokens per request to help improve rate-limiting 
        '''
        token_encoding = tiktoken.encoding_for_model(self.tokenizer)
        num_tokens = []
        for i in range(len(query_sentences)):
            token_count = len(token_encoding.encode(query_sentences[i]))
            num_tokens.append(token_count)
        return num_tokens
    

    def create(self, query:'list[str]', query_embeddings:'list[float]', project_title:str, metadata=None)->None:
        '''
        Create and name a brand new project! 
        '''
        tokens_in = self.get_num_tokens(query) #[1] * len(query)
        url = self.__URI
        project_name =  project_title
        obj = {
            'query_sentences':query,#Stores array of strings
            'query_embeddings':query_embeddings,
            'num_input_tokens':tokens_in,
            'api_key':self.api_key,
            'pod_id': project_name,
            'is_query':False,
            'create_new_project':True,
            'top_k':0,
            'metadata':metadata #Add this to the backend!
        }
        r = requests.post(url, json=obj)
        return r.json()
    
            
    #Request data from 
    def get(self, query:str, query_embeddings:'list[float]',project_title:str, top_k:int):
        '''
        (FORMERLY SIMILARITY SEARCH!)
        Query the Vector Store and return the top-ten most relevant embeddings. 
        Disguise URI endpoint using C++ compiled executable in next update.
        '''
        #Mitigate the following serialization error by converting to list:
        #TypeError: Object of type ndarray is not JSON serializable
        url = self.__URI
        project_name =  project_title
        tokens_in = self.get_num_tokens(query) 
        obj = {
            'query_sentences':query,#Stores array of strings
            'query_embeddings':query_embeddings,
            'num_input_tokens':tokens_in,#
            'api_key':self.api_key,
            'pod_id': project_name,
            'is_query':True,
            'create_new_project':False,
            'top_k':top_k
        }
        r = requests.post(url, json=obj)
        return r.json()

    def update(self, query, query_embeddings, project_title):
        '''FORMERLY update_embeddings()'''
        url = self.__URI
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
    
    def delete(self, project_title:str)->None:
        '''
            Delete your project.
        '''
        url = self.__URI
        project_name =  project_title
        obj = {
            'api_key':self.api_key,
            'pod_id': project_name,
            'delete':True #Indicate deletion operation
        }
        r = requests.post(url, json=obj)
        return r.json()

    def file_contents(destination_file_path):
        file1 = open(destination_file_path, 'r')
        Lines = file1.readlines()
        
        count = 0
        res = ""
        for line in Lines:
            count += 1
            res += line.strip()
        return res
    
    '''Python-based dynamic-programming optimizations'''

    def cosine_similarity(self, a:'list[float]', b:'list[float]')->float:
        '''
        Compute cosine similarity between two vectors.
        Can also take in numpy arrays as inputs a and b
        '''
        if type(a) == list:
            a = np.array(a)
        if type(b) == list:
            b = np.array(b)
        mag_a, mag_b = np.sqrt(a.dot(a)), np.sqrt(b.dot(b))
        return a.dot(b) / (mag_a * mag_b)

    def optimize_context(self, dp:'list[float]', composite_documents:'list[str]', threshold:float=0.0)->str:
        '''
            Given the optimized dp array recording the most optimal
            context relevancies and the composite_documents of mapped to it,  
            cluster the documents according to context relevancy.
            Examine the highest relevance cluster, and then return the smallest 
            composite document. 

            This is done in order to not only obtain the most relevant queries,
            but given a handful of similar documents, return the smallest one 
            in order to reduce the risk of context-window stuffing. This can 
            help mitigate the risk of hallucinations.
        '''
        retrieval = {composite_documents[i]:dp[i] for i in range(len(dp))}
        sorted_retrieval = sorted(retrieval.items(), key=lambda x:x[1])
        sorted_retrieval = dict(sorted_retrieval)
        context_similarities = list(sorted_retrieval.values())
        context_documents = list(sorted_retrieval.keys())
        clusters = self.one_dim_cluster(context_similarities)
        highest_relevance_cluster = clusters[-1]
        start_ind = len(context_similarities) - len(highest_relevance_cluster)
        min_length = float('inf')
        chosen_document = None 
        max_ind = -1
        for i in range(start_ind, len(context_documents)):
            if len(context_documents[i]) < min_length:
                min_length = len(context_documents[i])
                chosen_document = context_documents[i]
                max_ind = i

        if context_similarities[max_ind] > threshold:
            return chosen_document 
        return '<IRRELEVANT RESPONSE>'

    def one_dim_cluster(self, points_sorted:'list[float]', eps:float = 0.02)->'list[list[float]]':
        '''
        Return a list of clusters. 
        Each cluster is also a list[float]. 
        The largest cluster will be at the end of the array 
        
        Inputs: 
            points_sorted-> List of context relevancies sorted in ascending order.
            Obtained by sorting the dp array in the DP document retrieval algorithm.
            EXAMPLE: [0.3565528716632071, 0.3625131719737573, 0.42489084605506316]

            eps-> hyperparameter acting as 1D cluster distance.
            You can play around with this to determine how many composite documents 
            you wish to choose your RAG context from.

        Outputs: 
            clusters-> list of lists of floats, s.t. the list containing the largest-values 
            of clustered floats is the very last one. 
            This allows us to find the matching documents s.t. we can select the one with the 
            smallest string length, as presumably this means the smallest number of tokens.
            EXAMPLE:  [[0.3565528716632071, 0.3625131719737573], [0.42489084605506316]]
        '''
        clusters = []
        curr_point = points_sorted[0]
        curr_cluster = [curr_point]
        for point in points_sorted[1:]:
            if point <= curr_point + eps:
                curr_cluster.append(point)
            else:
                clusters.append(curr_cluster)
                curr_cluster = [point]
            curr_point = point
        clusters.append(curr_cluster)
        return clusters 
        

    #query, context, snippets
    def dynamic_retrieval(
            self, 
            query:list, 
            context:list, 
            snippets:list, 
            optimized:bool=False,
            threshold:float=0.0
        )->('list[str]', float, int):
        '''
        Dynamic programming solution to generate the most relevant possible 
        combination of documents when attempting a top-k search of a Vector Store.

        Inputs--
            context: takes in a nested list[list[float]] object, each inner list of floats 
            representing the embeddings of a returned document.

            query: takes in the embeddings of the user's query. 

            snippets: Takes in a type list[str], containing the documents searched for by 
            the end user. 

        Outputs--
            Tuple(float, str, int)
            
            Maximum dp array value- the maximum context relevance score calculated using 
            the dynamic programming algorithm over all optimal combinations of documents

            Composite documents- str type containing the text of the most optimal combination 
            of documents based on the Vector Stores' retrieval.
            
            Argmax of dp- for visualization purposes, shows the argmax or index of maximum 
            context relevance over the combination of documents.

        '''
        dp = [self.cosine_similarity(x, query) for x in context]
        composite_documents = snippets[:]
        if type(query) == list:
            query = np.array(query)

        for i in range(len(dp)):
            for j in range(i):
                #Compare the current cosine similarity dp[i] with that of itself plus a previous vector
                vector_sum = np.array(context[i]) + np.array(context[j])
                composite_similarity_score = self.cosine_similarity(vector_sum, query)
                if dp[i] < composite_similarity_score:
                    dp[i] = composite_similarity_score
                    #Add snippet to composite documents. Add punctuation because we did a string split around periods 
                    composite_documents[i] += '. ' + composite_documents[j] 
        
        k = np.argmax(dp)
        if optimized:
            best_document = self.optimize_context(dp, composite_documents, threshold)
            return best_document
        return (composite_documents[k], max(dp),  k)
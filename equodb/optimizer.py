import ctypes 
import os 
import numpy as np 
from sentence_transformers import SentenceTransformer
import time

'''Pass query and documents into C++ program via Python wrapper...
we're enterprise, so we want speed!

LATER... Rewrite DP algorithm in C++ under the hood to make this thing go BRR!
'''



def convert_embed_to_list(embeddings):
    num_context_vectors, embedding_dim = embeddings.shape[0], embeddings.shape[1]
    embeddings = embeddings.reshape(1, num_context_vectors * embedding_dim)
    return embeddings[0], num_context_vectors, embedding_dim



def file_contents(destination_file_path):
    file1 = open(destination_file_path, 'r')
    Lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    res = ""
    for line in Lines:
        count += 1
        res += line.strip()
    return res

def dynamic_retrieval(query, context, num_context_vectors, embedding_dim, documents, destination_file_path, PATH):
    '''
    Implement Dynamic Programming algorithm in C++ under the hood for optimal results!
    Algorithm examines a given ensemble of documents relative to a query vector, and  
    determines the optimal combination of documents with the highest context relevance 
    to the end user's query.

    This achieves two things:
    1. Provides a concise context for performing RAG with an LLM, thereby generating accurate
    responses with low probability of hallucination 
    2. Rapidly improves response times by implementing DP algorithm in C++!             
    '''
    example = ctypes.CDLL(PATH)

    #Convert Python list 
    # floats = example.embed
    example.embed.argtypes = [
        ctypes.POINTER(ctypes.c_float), 
        ctypes.POINTER(ctypes.c_float), 
        ctypes.POINTER(ctypes.c_char_p), 
        ctypes.c_int, 
        ctypes.c_int
    ]


    
    
    # example.embed.restype = ctypes.POINTER(ctypes.c_char_p)
    example.embed.restype = ctypes.c_void_p
    # example.embed.restype = ctypes.c_char_p

    # I have no idea why this library is so fucking weird
    float_query = (ctypes.c_float * len(query))(*query)
    float_context = (ctypes.c_float * len(context))(*context)
    documents = [(ctypes.c_char_p)(bytes(document, 'utf-8')) for document in documents]
    documents = (ctypes.c_char_p * len(documents))(*documents)

    # float* query, float* context, char** documents, int size, int embedding_dim
    start = time.time()
    example.embed(float_query, float_context, documents, num_context_vectors, embedding_dim) 
    end = time.time()

    res = file_contents(destination_file_path)
    os.remove(destination_file_path) 
    print('BEST DOCUMENT: {}'.format(res))
    print('DURATION: {}'.format(end - start))
    
    # example.print_strings.argtypes = [ctypes.POINTER(ctypes.c_char_p),ctypes.c_int]
    # example.print_strings(documents, len(documents))

#Convert Python list  


def generate_resource(PATH):
    '''
    Generate HTTP resource to connect client 
    with service.
    '''
    example = ctypes.CDLL(PATH)
    example.return_python_string.restype = ctypes.c_char_p
    URL = example.return_python_string()
    return str(URL)[1:]


def test_func(func):
    '''Test our dynamic programming-based retrieval algorithm.'''
    model =  SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    document = 'The territory of Kazakhstan has historically been inhabited by nomadic groups and empires. In antiquity, the nomadic Scythians inhabited the land, and the Achaemenid Persian Empire expanded towards the southern region. Turkic nomads have inhabited the country from as early as the 6th century. In the 13th century, the territory was subjugated by the Mongol Empire under Genghis Khan. In the 15th century, as a result of disintegration of the Golden Horde, the Kazakh Khanate was established. By the 18th century, Kazakh Khanate disintegrated into three jüz which were absorbed and conquered by the Russian Empire; by the mid-19th century, the Russians nominally ruled all of Kazakhstan as part of the Russian Empire and liberated the slaves of the Kazakhs in 1859.[14] Following the 1917 Russian Revolution and subsequent Russian Civil War, the territory was reorganized several times. In 1936, it was established as the Kazakh Soviet Socialist Republic within the Soviet Union. Kazakhstan was the last of the Soviet republics to declare independence during the dissolution of the Soviet Union from 1988 to 1991. '

    # query = 'What people have historically inhabited the nation of Kazakhstan?'
    query = 'Which groups have inhabited the territory throughout antiquity?'

    documents = document.split('.') #list[str]

    query = model.encode(query).tolist()
    context = model.encode(documents)
    context, num_context_vectors, embedding_dim = convert_embed_to_list(context)
    context = context.tolist()


    func(query, context, num_context_vectors, embedding_dim, documents, destination_file_path=os.getcwd() + "/filename.txt", PATH=os.getcwd() + '/opt.so')

# print(test_func(dynamic_retrieval))
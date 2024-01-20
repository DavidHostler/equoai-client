#include <iostream>
#include <math.h>
#include <string>
#include <cstring>
#include <vector>
#include <fstream>
using namespace std;

//Perform dynamic programming algorithm
extern "C" {
    //Return the cosine similarity of two vectors
    float cosine_similarity(float* x, float* y, int embedding_dim){
        float result = 0.0;
        float x_mag_squared = 0.0;
        float y_mag_squared = 0.0;
        for(int i = 0; i < embedding_dim; i++){
            result = result + x[i] * y[i];
            x_mag_squared += pow(x[i], 2);
            y_mag_squared += pow(y[i], 2);
        }  
        float x_mag = pow(x_mag_squared, 0.5);
        float y_mag = pow(y_mag_squared, 0.5);
        return result / (x_mag * y_mag);
    }
    //Beginning at a starting index, increment pointer by embedding_dim amount to retrieve the 
    //subarray 
    float* get_context_vector(float* context, int embedding_dim, int start_index){
        float* subarray = new float[embedding_dim]; // Don't forget to delete [] a; when you're done!
        for(int i = 0; i < embedding_dim; i++){
            subarray[i] = context[start_index + i];
        }
        return subarray;
    }

    //Given all context vectors, generate a dp array of cosine similarities b/w each context and the
    //query
    float* generate_dp_array(float* query, float* context, int embedding_dim, int context_len){
        float* dp = new float[context_len];
        for(int i = 0; i < context_len; i++){
            float* current_context = get_context_vector(context, embedding_dim, embedding_dim * i);
            dp[i] = cosine_similarity(query, current_context, embedding_dim);
        }
        return dp;
    }

    //Add components of a vector element-wise
    float * add_vectors(float* x, float* y, int size){
        float* res = new float[size];
        for(int j = 0; j < size; j++){
            res[j] = x[j] + y[j];
        }
        return res;
    }

    
    string* chars_to_str(char** input, int length){
        string* output = new string[length];
        string current_string;
        for(int j = 0; j < length; j++){
            string current_string(input[j]);
            output[j] = current_string;
        }
        
        return output;
    }

    
    const char* string_to_char(string s){

        // the c_str() function returns 
        // a const pointer to null  
        // terminated contents. 
        const char* str = s.c_str(); 
        
        // printing the char array 
        std::cout << str; 

        return str;
    }


    char* concatenate_strings(const vector<std::string>& strings) {
        // Calculate the total length needed for the concatenated string
        size_t total_length = 0;
        for (const auto& str : strings) {
            total_length += str.length();
        }

        // Allocate memory for the concatenated string (plus one for the null terminator)
        char* result = new char[total_length + 1];

        // Copy each string into the result buffer
        size_t index = 0;
        for (const auto& str : strings) {
            strcpy(result + index, str.c_str());
            index += str.length();
        }

        // Null-terminate the result
        result[total_length] = '\0';

        return result;
    }

    string read_file(){
            // Create a text string, which is used to output the text file
        string myText;
        string result = "";
        // Read from the text file
        ifstream MyReadFile("filename.txt");

        // Use a while loop together with the getline() function to read the file line by line
        while (getline (MyReadFile, myText)) {
        // Output the text from the file
        cout << myText;
        result += myText;
        }

        // Close the file
        MyReadFile.close(); 
        

        return result;
    }

    //Query, context vectors, documents, 
    //Return the most optimal combination of documents
    void embed(float* query, float* context, char** documents, int size, int embedding_dim){
        //Initialize dp array                     
        float* dp = generate_dp_array(query, context, embedding_dim, size);
        float composite_similarity_score;
        float* context_i;
        float* context_j;
        float* vector_sum; 
        string* composite_documents = chars_to_str(documents, size);
        string addend; 
        for(int i = 0; i < size; i++){
            context_i = get_context_vector(context, embedding_dim, embedding_dim * i);
            cout << composite_documents[i] << endl;
            for(int j = 0; j < i; j++){
                context_j = get_context_vector(context, embedding_dim, embedding_dim * j);
                vector_sum = add_vectors(context_i, context_j, embedding_dim);
                composite_similarity_score = cosine_similarity(vector_sum, query, embedding_dim);
                //Dynamically generate all optimal combinations of documents
                if(dp[i] < composite_similarity_score){
                    dp[i] = composite_similarity_score;
                    addend = ". " + composite_documents[j];
                    composite_documents[i] += addend;
                    // addend = composite_documents[i] + addend;
                    // composite_documents[i] = addend;
                    cout << "--NEXT DOCUMENT--" << endl;
                    cout << composite_documents[i] << " ";
                }
            }    
        }
        string* result = new string[size];
        float maximum_similarity = -100.0;
        int opt_index;
        for(int k = 0; k < size; k++){
            if(dp[k] > maximum_similarity){
                maximum_similarity = dp[k];
                opt_index = k;
            }
            //Make vector <str>
        }
        cout << "Maximum Score: " << dp[opt_index] << endl;
        cout << "Best Document: " << composite_documents[opt_index] << endl;

        
        // string output = composite_documents[opt_index];
        // return composite_documents[opt_index];
        string chosen_document = composite_documents[opt_index];

        // Create and open a text file
        ofstream MyFile("filename.txt");

        // Write to the file
        MyFile << chosen_document;

        // Close the file
        MyFile.close();
      
    }


    

    char* return_python_string(){
        return "https://evening-everglades-40994-f3ba246c1253.herokuapp.com/query";
    }





    void print_strings(char** strings, int size) {
        string* composite_documents = chars_to_str(strings, size);

        for (int i = 0; i < size; ++i) {
            std::cout << composite_documents[i] << "";
        }
        std::cout << std::endl;
    }
}
// C++ program to convert string 
// to char array Using c_str() 
// without strcpy() 
#include <cstring> 
#include <string> 
#include <iostream> 
#include <fstream>
using namespace std;

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


void write_file(){
    // Create and open a text file
    ofstream MyFile("filename.txt");

    // Write to the file
    MyFile << "Files can be tricky, but it is fun enough!";

    // Close the file
    MyFile.close();
}



int main(){
    // const char* res = string_to_char(); 
    // cout << res << endl;
    // res = string_to_char();
    // cout << res << endl;
    // write_file();

    string file = read_file();
    cout << file;
}

import os 
# Using readlines()
def file_contents():
    file1 = open(os.getcwd() + '/filename.txt', 'r')
    Lines = file1.readlines()
    
    count = 0
    # Strips the newline character
    res = ""
    for line in Lines:
        count += 1
        res += line.strip()

    return res
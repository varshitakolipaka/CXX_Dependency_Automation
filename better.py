import os
import re
input_path = str(input('input file filename: '))
include_list = []
input_path=os.getcwd() +'/' + input_path

    
def get_all_dependencies(file_path):  

    # get path of the file
    new_dir=re.match('^(.*[\/])',file_path).group(1) 
    print("new dir is:", new_dir)
    myfile = open(file_path, "r") 
    
    myline = myfile.readline() 
    while myline:
        list1=(re.findall('(#include \"(.*?.(h|hpp))\")', myline))
        if(len(list1)==1):
            if(list1[0][1].startswith('./')):
                actual = list1[0][1][2:]
            else:
                actual = list1[0][1]
            print(actual)
            
            include_list.append(new_dir+actual) # append to global list
        myline = myfile.readline()
    myfile.close()   

    return include_list


include_list.append(input_path)
included_libraries = []
while(len(include_list) > 0):
    get_all_dependencies(include_list[0])
    if(include_list[0] not in included_libraries):
        included_libraries.append(include_list[0])
    include_list.pop(0)

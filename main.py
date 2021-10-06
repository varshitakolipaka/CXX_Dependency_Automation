import os
import re
input_path = str(input('input file filename: '))


include_list = []
input_path=os.getcwd() +'/' + input_path
stack=[]
def get_all_dependencies(file_path):  #..../opencv2/core.hpp
    # local list of dependencies
    include_list_local = []
    new_dir=re.match('^(.*[\/])',file_path).group(1) 

    myfile = open(file_path, "r") 
    print(myfile)
    myline = myfile.readline() 
    while myline:
        list1=(re.findall('(#include \"(.*?.(h|hpp))\")', myline))
        if(len(list1)==1):
            if(list1[0][1].startswith('./')):
                to_append=list1[0][1][2:]
            else:
                to_append=list1[0][1]
            include_list_local.append(new_dir+to_append)
            include_list.append(new_dir+to_append) # append to global list
        myline = myfile.readline()
    myfile.close()   

    # print(include_list_local)
    for filename in include_list_local:
        get_all_dependencies(filename)
    return include_list

#..../opencv2/core.hpp
get_all_dependencies(input_path) 
print(include_list)

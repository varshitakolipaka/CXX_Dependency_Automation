import os

import re
# input_path = str(input('input file filename: '))
input_path = "opencv2/core.hpp"
include_list = []
input_path = os.getcwd() + '/' + input_path


def get_all_dependencies(file_path):

    # get path of the file
    new_dir = re.match(r'^(.*[\/])', file_path).group(1)
    # print("new dir is:", new_dir)
    if os.path.exists(file_path):
        myfile = open(file_path, "r")
        # print("FILE: ", file_path)
        myline = myfile.readline()
        while myline:
            list1 = (re.findall('(#include \"(.*?.(h|hpp))\")', myline))
            # print(len(list1))
            if(len(list1) == 1):
                actual = list1[0][1]
                new_file_path = optimize_file_path(actual, new_dir)
                include_list.append(new_file_path)  # append to global list
                included_libraries[include_list[0]].append(new_file_path)
                
                # print(new_dir + actual)
            myline = myfile.readline()

        myfile.close()

    return include_list


def optimize_file_path(file_path, new_dir):
    actual = file_path
    while(actual.startswith('./')):
        actual = actual[2:]
        # print("actual:", actual)
    while (actual.startswith('../')):
        new_dir = re.match('^(.*[\/])', new_dir).group(1)
        actual = actual[3:]
    return new_dir+actual


include_list.append(input_path)
included_libraries = {}

while len(include_list) > 0:
    if include_list[0] not in included_libraries:
        # print("CURRENT PARENT:", include_list[0])
        included_libraries[include_list[0]] = []
        get_all_dependencies(include_list[0])
    include_list.pop(0)

# path_to_remove = str(input("Enter the path you want to remove: "))
path_to_remove = "/Users/vars/OneDrive - International Institute of Information Technology/CXX_Dependency_Automation/opencv2/"
graphviz_code = "strict digraph G{\n"
for parent, children in included_libraries.items():
    clean_parent = parent.replace(path_to_remove,'')
    graphviz_code = graphviz_code + '"' + clean_parent + '"'+ "-> { "
    s = '; '.join(str('"' + child.replace(path_to_remove,'') +'"' ) for child in children)
    graphviz_code = graphviz_code + s + '};\n'
    
graphviz_code = graphviz_code + "\n}"
print(graphviz_code)

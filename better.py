import os
import shutil
from pathlib import Path
import re
import pydot
import numpy

def getFolderPath(file_path):
    folder_path = re.match("^(.*[\/])", file_path).group(1)
    return folder_path

def getIncludes(myline):
    match = re.findall('(#include "(.*?.(h|hpp))")', myline)
    include_file_name = match[0][1] if len(match) else "INVALID"
    return include_file_name
    
def getDependencies(file_path):
    path_to_file = getFolderPath(file_path)
    if os.path.exists(file_path):
        myfile = open(file_path, "r")
        myline = myfile.readline()
        while myline:
            include_file_name = getIncludes(myline)
            if include_file_name != "INVALID":
                shortened_file_path = compressFilePath(include_file_name, path_to_file)
                include_list.append(shortened_file_path)
                included_libraries[include_list[0]].append(shortened_file_path)

            myline = myfile.readline()

        myfile.close()

    return include_list

def compressFilePath(file_path, folder_path):

    while file_path.startswith("./"):
        file_path = file_path[2:] 
    
    while file_path.startswith( "../"):
        if folder_path.endswith("/"):
            folder_path = folder_path[:-1]
        folder_path = re.match("^(.*[\/])", folder_path).group(1)
        file_path = file_path[3:]
    print(folder_path + file_path)
    return folder_path + file_path

def find_common_path(dictionary):
    array = keys_to_arr(dictionary)
    ind1 = 0
    ind2 = 1
    common = ""
    while(ind1 < len(array) and ind2 < len(array)):
        common = os.path.commonpath([array[ind1], array[ind2]])
        ind1+=1
        ind2+=1
    if not common.endswith("/"):
        common = re.match("^(.*[\/])", common).group(1)

    return common

def rename_keys_dict(common_path, required_path, dictionary):
    for key in dictionary:
        new_key = key.replace(common_path, required_path)
        print("new_key: ",new_key)
        dictionary[new_key] = dictionary.pop(key)
        return dictionary
    
def keys_to_arr(dictionary):
    arr = []
    for key in dictionary:
        arr.append(key)
    return arr
def processIntactPath(intact_path):
    if not intact_path.startswith("/"):
        intact_path = "/" + intact_path
    if not intact_path.endswith("/"):
        intact_path = intact_path[:-1]
    return intact_path

def createDotFile(included_libraries, path_to_remove):
    graphviz_code = "strict digraph G {\n"
    for parent, children in included_libraries.items():
        clean_parent = parent.replace(path_to_remove, "")
        graphviz_code = graphviz_code + '"' + clean_parent + '"' + "-> { "
        s = "; ".join(
            str('"' + child.replace(path_to_remove, "") + '"') for child in children
        )
        graphviz_code = graphviz_code + s + "};\n"

    graphviz_code = graphviz_code + "\n}"
    print(graphviz_code)
    graph, = pydot.graph_from_dot_data(graphviz_code)
    image_path = input("Enter Image Path:")
    graph.write_png(image_path )

def initIncludeDict(included_libraries):
    while len(include_list) > 0:
        if include_list[0] not in included_libraries:
            included_libraries[include_list[0]] = []
            getDependencies(include_list[0])
        include_list.pop(0)

include_list = []
included_libraries = {}

input_path = input("File Path: ")

if input_path.startswith("/"):
    input_path = os.path.abspath(input_path)

include_list.append(input_path)
initIncludeDict(included_libraries)
path_to_remove = find_common_path(included_libraries)

createDotFile(included_libraries, path_to_remove)

intact_path = input("Enter the directory structure to keep intact (Must be a substring from the end): ")
intact_path = processIntactPath(intact_path)

desired_path = str(
    input("Enter the desired directory, where you want your root file: ")
)
desired_path += intact_path
if not desired_path.endswith("/"):
    desired_path += "/" 

for file_path in included_libraries.items():
    exact_file_path = file_path[0].replace(path_to_remove, desired_path)
    exact_directory_path = re.match(r"^(.*[\/])", exact_file_path).group(1)
    if os.path.exists(file_path[0]):
        os.makedirs(exact_directory_path, mode=0o777, exist_ok=True)
        open(exact_file_path, "w").close()
        shutil.copy(file_path[0], exact_file_path)
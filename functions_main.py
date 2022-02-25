import os
import shutil
from pathlib import Path
import re
import pydot
from change_includes import *

def get_folder_path(file_path):
    # get everything before the last slash
    folder_path = re.match("^(.*[\/])", file_path).group(1)
    return folder_path

def get_includes(myline):
    ''' finds all instances of include patterns in a line.
    checks in [()], and checks whether such an array exists, else, an include is not found'''

    match = re.findall('(#include *\"(.*?.(h|hpp))\")|(#include *\<(.*?.(h|hpp))\>)', myline)
    if len(match):
        if match[0][1] != "":
            include_file_name = match[0][1]
            # print(include_file_name)
            # if include_file_name.startswith("opencv2/"):
            #     include_file_name = include_file_name[:-1]
        elif match[0][4] and match[0][4] != "":
            include_file_name = match[0][4]
    else:
        include_file_name = "INVALID" 
    
    return include_file_name
    
def get_dependencies(file_path, included_libraries, include_list):
    '''gets only the folder path
     check if such a file exists, and it isn't empty stringed
     opening the file
     do for each line in the file, while reading line by line
     get an instance of #include
     if something is being included...
     if file not found, try finding file in the root directory of file'''

    # print("----------------------")
    # print("INSIDE:", file_path)
    # print("----------------------")

    path_to_file = get_folder_path(file_path)
    if os.path.exists(file_path) and file_path != "" and os.path.isdir(file_path) != 1:
        # print("it's a real file")
        myfile = open(file_path, "r")
        myline = myfile.readline()
        while myline:
        
            include_file_name = get_includes(myline)
            if include_file_name != "INVALID":
                include_file_name = compress_file_path(include_file_name, path_to_file)
                include_file_name = processInputPath(path_to_file, include_file_name)
                include_list.append(include_file_name)
                included_libraries[include_list[0]].append(include_file_name)

            myline = myfile.readline()

        myfile.close()
    return include_list

def compress_file_path(file_path, folder_path):
    if os.path.isabs(file_path):
        return file_path

    if file_path.startswith("./") or file_path.startswith("../"):
        while file_path.startswith("./"):
            file_path = file_path[2:]
        
        while file_path.startswith( "../"):
            if folder_path.endswith("/"):
                folder_path = folder_path[:-1]

            folder_path = get_folder_path(folder_path) 
            file_path = file_path[3:]

        return folder_path, file_path

    return file_path

def find_common_path(dictionary):
    array = keys_to_arr(dictionary)
    i = 1
    common = ""
    common = os.path.commonpath(array)
  
    if not common.endswith("/") and common != "":
        common = common + "/"
        common = re.match("^(.*[\/])", common).group(1)
    return common
    


def rename_keys_dict(common_path, required_path, dictionary):
    for key in dictionary:
        new_key = key.replace(common_path, required_path)
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
        intact_path = intact_path + "/"
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
    graph, = pydot.graph_from_dot_data(graphviz_code)
    image_path = input("Enter Image Path:")
    graph.write_png(image_path )

def initIncludeDict(included_libraries, include_list):
    while len(include_list) > 0:
        if include_list[0] not in included_libraries:
            included_libraries[include_list[0]] = []
            get_dependencies(include_list[0], included_libraries, include_list)
        include_list.pop(0)

def processInputPath(folder_path,input_path):
    print("INPUTPATH = ", input_path)
    abspath = folder_path + input_path
    abspath = os.path.abspath(abspath)
    path = abspath
    if not os.path.exists(abspath) or os.path == "":
        temp_path = "/Users/vars/OneDrive - International Institute of Information Technology/CXX_Dependency_Automation/" + input_path
        if os.path.exists(temp_path):
            path = temp_path
        
    return path


